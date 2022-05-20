from PowDagSim.run import Run
from PowDagSim.greedy_algorithms import take_graph_transpose, get_next_finish, update_time, select_configuration
from PowDagSim import pace, sim_log
from random import uniform





def graham_list_scheduling(num_machines, task_graph_adj, node_to_application, rand_wl_scale, tasks):
    num_tasks = len(task_graph_adj)
    runs = []
    schedule = []
    ready_tasks = []
    machines = [0 for i in range(num_machines)] # machine[i] is the next time point machine i will be available
    tasks_on_machines = [None for i in range(num_machines)] # tasks_on_machines[i] the task running on machine i
    num_started_tasks = 0

    graph_transpose = take_graph_transpose(task_graph_adj)

    #print(task_graph_adj)
    #print(graph_transpose)
    # find ready tasks with 0 incoming edges
    for v in graph_transpose:
        if not graph_transpose[v]:
            ready_tasks.append(v)

    t = 0
    while num_started_tasks < num_tasks:

        (finished_time, finished_machine_index) = get_next_finish(machines, tasks_on_machines, t)
        finished_task = tasks_on_machines[finished_machine_index]
        #print("Finished tasks, f time, f machine: ", finished_task, finished_time, finished_machine_index)
        if finished_time > t:
            t = finished_time

        if finished_task is not None:
            runs.append([finished_task, finished_time - tasks[node_to_application[finished_task]].time*(rand_wl_scale[finished_task]), finished_time, finished_machine_index])
            #print("Runs: ", runs)
            for v in task_graph_adj[finished_task]:
                graph_transpose[v].remove(finished_task)
                if not graph_transpose[v]:
                    ready_tasks.append(v)
        #print("Ready tasks: ", ready_tasks)
        #there is a next task available to process
        if ready_tasks:
            machines[finished_machine_index] = max(t, finished_time) + tasks[node_to_application[ready_tasks[0]]].time*(rand_wl_scale[ready_tasks[0]])
            tasks_on_machines[finished_machine_index] = ready_tasks[0]
            num_started_tasks += 1
            #print("Next finish times of machines: ", machines)
            #print("Indices of tasks on machines: ", tasks_on_machines)
            del ready_tasks[0]
        #ready_tasks are all processed and it is turn for the next level in topo sort
        elif not ready_tasks :
            if finished_task is not None:
                tasks_on_machines[finished_machine_index] = None
            t = update_time(machines, tasks_on_machines, t)

    for i,m in enumerate(machines):
        if m>=t and tasks_on_machines[i] is not None:
            runs.append([tasks_on_machines[i], m - tasks[ node_to_application[tasks_on_machines[i]] ].time*(rand_wl_scale[tasks_on_machines[i]]), m, i])

    return sorted(runs, key= lambda x: (x[2], x[3]))












def next_fit_decreasing_height_experimental(num_machines, jobs, node_to_application, rand_wl_scale, applications, power_cap, pace_tasks):

    jobs_dec_height = sorted(jobs, key= lambda job: pace_tasks[ node_to_application[job] ].time*(rand_wl_scale[job]), reverse=True)
    current_time = 0
    current_power = 0
    current_machine = 0
    current_level = []
    resulting_schedule = []
    for job in jobs_dec_height:
        if pace_tasks[ node_to_application[job] ].power + current_power <= power_cap and current_machine <= num_machines:
            current_level.append(job)
            current_machine = current_machine + 1
            current_power = current_power + pace_tasks[ node_to_application[job] ].power
        else:
            #handle configuration selection for the current level then continue with a new level
            current_level_schedule, ignored_configs = select_configuration(current_level, current_time, node_to_application, rand_wl_scale, applications, pace_tasks, power_cap)
            resulting_schedule.extend(current_level_schedule)
            current_level = []
            current_time = max(run.end_time for run in current_level_schedule)
            current_machine = 0
            current_power = 0
            current_level.append(job)
            current_power = current_power + pace_tasks[ node_to_application[job] ].power
            current_machine = current_machine + 1

    if current_level:
        current_level_schedule, ignored_configs = select_configuration(current_level, current_time, node_to_application, rand_wl_scale, applications, pace_tasks, power_cap)
        resulting_schedule.extend(current_level_schedule)

    return resulting_schedule







def divide_and_conquer_scheduler_recursive_experimental(num_machines, pseudo_machine_coeff, graph_adj, node_to_application, rand_wl_scale, applications, graham_schedule, start_time, finish_time, power_cap, pace_tasks, random_mid_point):
    random_mid = start_time + (finish_time - start_time)*uniform(0.35, 0.65)
    mid_time = (start_time + finish_time)/2.0 if not random_mid_point else random_mid
    mid_jobs = []
    before_jobs = []
    after_jobs = []
    for run in graham_schedule:
        if start_time <= run[1] < mid_time <= run[2] <= finish_time:
            mid_jobs.append(run[0])
        elif start_time <= run[1] <= run[2] < mid_time:
            before_jobs.append(run[0])
        elif finish_time >= run[2] >= run[1] >= mid_time:
            after_jobs.append(run[0])



    if before_jobs:
        before_graph_adj = {}
        for job in before_jobs:
            before_graph_adj[job] = set([x for x in graph_adj[job] if x in before_jobs])
        before_graham_schedule = graham_list_scheduling(num_machines*pseudo_machine_coeff, before_graph_adj, node_to_application, rand_wl_scale, pace_tasks)
        before_graham_finish_time = before_graham_schedule[-1][2]
        before = divide_and_conquer_scheduler_recursive_experimental(num_machines, pseudo_machine_coeff, before_graph_adj, node_to_application, rand_wl_scale, applications, before_graham_schedule, 0, before_graham_finish_time, power_cap, pace_tasks, random_mid_point)
    else:
        before = []

    if mid_jobs:
        mid = next_fit_decreasing_height_experimental(num_machines, mid_jobs, node_to_application, rand_wl_scale, applications, power_cap, pace_tasks)
    else:
        mid = []

    if after_jobs:
        after_graph_adj = {}
        for job in after_jobs:
            after_graph_adj[job] = set([x for x in graph_adj[job] if x in after_jobs])
        after_graham_schedule = graham_list_scheduling(num_machines*pseudo_machine_coeff, after_graph_adj, node_to_application, rand_wl_scale, pace_tasks)
        after_graham_finish_time = after_graham_schedule[-1][2]
        after = divide_and_conquer_scheduler_recursive_experimental(num_machines, pseudo_machine_coeff, after_graph_adj, node_to_application, rand_wl_scale, applications, after_graham_schedule, 0, after_graham_finish_time, power_cap, pace_tasks, random_mid_point)
    else:
        after = []


    if before:
        before_finish = max(run.end_time for run in before)
    else:
        before_finish = 0

    if mid:
        mid_finish = max(run.end_time for run in mid)
    else:
        mid_finish = 0

    result = before[:]
    for run in mid:
        run.start_time += before_finish
        run.end_time   += before_finish
        #result.append([run[0], run[1] + before_finish, run[2] + before_finish, run[3], run[4], run[5]])
    result.extend(mid)

    for run in after:
        run.start_time += before_finish + mid_finish
        run.end_time   += before_finish + mid_finish
        #result.append([run[0], run[1] + before_finish + mid_finish, run[2] + before_finish + mid_finish, run[3], run[4], run[5]])
    result.extend(after)

    return result






def divide_and_conquer_scheduler_experimental(num_machines, pseudo_machine_coeff, number_of_nodes_in_dag, graph_adj, node_to_application, rand_wl_scale, applications, power_cap, random_mid_point = False):
    # Get pace tasks and run Graham's List Scheduling using "time" values of the pace tasks
    pace_tasks = pace.get_pace_tasks_of_all_applications(applications, power_cap)
    graham_schedule = graham_list_scheduling(num_machines*pseudo_machine_coeff, graph_adj, node_to_application, rand_wl_scale, pace_tasks)


    finish_time = graham_schedule[-1][2]
    returned_schedule = divide_and_conquer_scheduler_recursive_experimental(num_machines, pseudo_machine_coeff, graph_adj, node_to_application, rand_wl_scale, applications, graham_schedule, 0, finish_time, power_cap, pace_tasks, random_mid_point)

    return returned_schedule




























def next_fit_decreasing_height(num_machines, jobs, node_to_application, rand_wl_scale, applications, power_cap, pace_tasks):

    jobs_dec_height = sorted(jobs, key= lambda job: pace_tasks[ node_to_application[job] ].time*(rand_wl_scale[job]), reverse=True)
    current_time = 0
    current_power = 0
    current_machine = 0
    current_level = []
    resulting_schedule = []
    for job in jobs_dec_height:
        if pace_tasks[ node_to_application[job] ].power + current_power <= power_cap and current_machine <= num_machines:
            current_level.append(job)
            current_machine = current_machine + 1
            current_power = current_power + pace_tasks[ node_to_application[job] ].power
        else:
            #handle configuration selection for the current level then continue with a new level
            current_level_schedule, ignored_configs = select_configuration(current_level, current_time, node_to_application, rand_wl_scale, applications, pace_tasks, power_cap)
            resulting_schedule.extend(current_level_schedule)
            current_level = []
            current_time = max(run.end_time for run in current_level_schedule)
            current_machine = 0
            current_power = 0
            current_level.append(job)
            current_power = current_power + pace_tasks[ node_to_application[job] ].power
            current_machine = current_machine + 1

    if current_level:
        current_level_schedule, ignored_configs = select_configuration(current_level, current_time, node_to_application, rand_wl_scale, applications, pace_tasks, power_cap)
        resulting_schedule.extend(current_level_schedule)

    return resulting_schedule





def divide_and_conquer_scheduler_recursive(num_machines, node_to_application, rand_wl_scale, applications, graham_schedule, start_time, finish_time, power_cap, pace_tasks, random_mid_point):
    random_mid = start_time + (finish_time - start_time)*uniform(0.35, 0.65)
    mid_time = (start_time + finish_time)/2.0 if not random_mid_point else random_mid
    mid_jobs = []
    before_jobs = []
    after_jobs = []
    rec_before_finish_time = start_time
    rec_before_start_time = mid_time
    rec_after_finish_time = mid_time
    rec_after_start_time = finish_time
    for run in graham_schedule:
        if start_time <= run[1] < mid_time <= run[2] <= finish_time:
            mid_jobs.append(run[0])
        elif start_time <= run[1] <= run[2] < mid_time:
            before_jobs.append(run[0])
            rec_before_finish_time = max(rec_before_finish_time, run[2])
            rec_before_start_time = min(rec_before_start_time, run[1])
        elif finish_time >= run[2] >= run[1] >= mid_time:
            after_jobs.append(run[0])
            rec_after_finish_time = max(rec_after_finish_time, run[2])
            rec_after_start_time = min(rec_after_start_time, run[1])


    #print("S: ", start_time,  "E: ", finish_time, "Mid T: ", mid_time, "bef_st", rec_before_start_time ,"bef_fin", rec_before_finish_time, "af_st", rec_after_start_time , "af_fin", rec_after_finish_time , 'MidJobs: ', mid_jobs)


    if before_jobs:
        before = divide_and_conquer_scheduler_recursive(num_machines, node_to_application, rand_wl_scale, applications, graham_schedule, rec_before_start_time, rec_before_finish_time, power_cap, pace_tasks, random_mid_point)
    else:
        before = []

    if mid_jobs:
        mid = next_fit_decreasing_height(num_machines, mid_jobs, node_to_application, rand_wl_scale, applications, power_cap, pace_tasks)
    else:
        mid = []

    if after_jobs:
        after = divide_and_conquer_scheduler_recursive(num_machines, node_to_application, rand_wl_scale, applications, graham_schedule, rec_after_start_time, rec_after_finish_time, power_cap, pace_tasks, random_mid_point)
    else:
        after = []


    if before:
        before_finish = max(run.end_time for run in before)
    else:
        before_finish = 0

    if mid:
        mid_finish = max(run.end_time for run in mid)
    else:
        mid_finish = 0

    result = before[:]
    for run in mid:
        run.start_time += before_finish
        run.end_time   += before_finish
        #result.append([run[0], run[1] + before_finish, run[2] + before_finish, run[3], run[4], run[5]])
    result.extend(mid)

    for run in after:
        run.start_time += before_finish + mid_finish
        run.end_time   += before_finish + mid_finish
        #result.append([run[0], run[1] + before_finish + mid_finish, run[2] + before_finish + mid_finish, run[3], run[4], run[5]])
    result.extend(after)

    return result



def divide_and_conquer_scheduler(num_machines, pseudo_machine_coeff, number_of_nodes_in_dag, graph_adj, node_to_application, rand_wl_scale, applications, power_cap, random_mid_point = False):
    # Get pace tasks and run Graham's List Scheduling using "time" values of the pace tasks
    pace_tasks = pace.get_pace_tasks_of_all_applications(applications, power_cap)
    graham_schedule = graham_list_scheduling(num_machines*pseudo_machine_coeff, graph_adj, node_to_application, rand_wl_scale, pace_tasks)


    finish_time = graham_schedule[-1][2]
    returned_schedule = divide_and_conquer_scheduler_recursive(num_machines, node_to_application, rand_wl_scale, applications, graham_schedule, 0, finish_time, power_cap, pace_tasks, random_mid_point)

    return returned_schedule
