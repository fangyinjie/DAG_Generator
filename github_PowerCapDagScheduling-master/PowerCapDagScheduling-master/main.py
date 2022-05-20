import os
import argparse
import sys
import random
import time
import copy


import import_util
from PowDagSim import application, job, sim_log, dag, pace, task, divide_and_conquer, greedy_algorithms, plot#, scheduler

parser = argparse.ArgumentParser()
parser.add_argument('-m','--num-machines', help='Number of machines in the system', default=5, required=False, type=int)
parser.add_argument('-P','--power-cap', help='Global power cap (W)', default=200, required=False, type=int)
parser.add_argument('-a', '--num-apps', help='Number of applications to use to map to DAG', default=15, required=False, type=int)
parser.add_argument('-L', '--debug-level', help='Debug level [CRITICAL, ERROR, WARNING, INFO, DEBUG, TRACE]', default="TRACE", required=False)
parser.add_argument('-d', '--dag', help='Name of .dot file containing DAG structure', default="sample-dag2", required=False)
parser.add_argument('-A', '--algorithm', nargs='+', help='Algorithm to use [NAIVE, DIVIDECONQUER]', default="NAIVE", required=False)
parser.add_argument('-l', '--lookahead', help='Look Ahead Level for the naive algorithm: an integer from 1 to 100000', default=1, required=False, type=int, choices=range(1,100001))
parser.add_argument('-s', '--simulation-count', help='How many times to simulate: an integer', default=10, required=False, type=int, choices=range(1,200))

args = parser.parse_args()


num_machines = args.num_machines
power_cap = args.power_cap
num_apps = args.num_apps
dag_name = args.dag
lookahead_level = args.lookahead
simulation_count = args.simulation_count


sim_log.loglevel = args.debug_level

NAIVE = True
DIVIDECONQUER = True


if "NAIVE" in args.algorithm:
    NAIVE = True
if "DIVIDECONQUER" in args.algorithm:
    DIVIDECONQUER = True








sim_log.log("INFO", "Initializing all applications...")
applications = application.init_all_apps(num_apps, power_cap)

sim_log.log("INFO", "Getting dot dag...")

dot_dag_file = open(os.path.join("dag",dag_name+".dot"),"r")
dot_dag = dag.dot2dag.dot2dag(dot_dag_file)
dot_dag_file.close()

sim_log.log("DEBUG", "dot_dag: ", list(dot_dag.items()))

toposort_ordering = list(dag.dot2dag.order_dag(dot_dag))
sim_log.log("DEBUG", "toposort_ordering: ", toposort_ordering)

name_to_index = {}
for index, name in list(enumerate(toposort_ordering)):
        name_to_index[name] = index

dag_adj_list_by_index = {}
for index, name in list(enumerate(toposort_ordering)):
    dag_adj_list_by_index[index] = set([name_to_index[x] for x in dot_dag[name]]) if name in dot_dag else set([])


number_of_nodes_in_dag = len(toposort_ordering)

sim_log.log("INFO", "Number of Nodes: ", [number_of_nodes_in_dag])
sim_log.log("DEBUG", "This is adj list by index: ", list(dag_adj_list_by_index.items()))
sim_log.log("DEBUG", "This is the ordering of the DAG nodes:\n\t", toposort_ordering)



simulation_stats = [0, 0, 0, 0, 0]

simulation_results_exectime = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
simulation_results_makespan = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
simulation_results_energy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
simulation_results_makespan_percent = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
simulation_results_energy_percent = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for simulation_count_current in range(simulation_count):



    sim_log.log("INFO", "Extending the application with random perturbation from the original applications...")
    rand_wl_scale = [1] * number_of_nodes_in_dag
    rand_scale_mean = 2
    rand_scale_var = 0.5
    for i in range(number_of_nodes_in_dag):
        rand_workload_scale = random.gauss(rand_scale_mean, rand_scale_var)
        while rand_workload_scale <= 0 or rand_workload_scale >= 2*rand_scale_mean:
            rand_workload_scale = random.gauss(rand_scale_mean, rand_scale_var)
        rand_wl_scale[i] = rand_workload_scale
        #extended_applications[i] = application.Application(i)
        #extended_applications[i].tasks = copy.deepcopy(applications[random.randint(0, num_apps - 1)].tasks)
        #for task in extended_applications[i].tasks:
        #    task.workload = task.workload * rand_workload_scale
        #    if float(task.speed) > 0:
        #        task.time = task.workload / float(task.speed)
        #    else:
        #        task.time = 0



    sim_log.log("INFO", "Assigning applications to dag nodes...")
    node_to_application = [0] * number_of_nodes_in_dag
    for i in range(number_of_nodes_in_dag):
#        node_to_application[i] = i
        node_to_application[i] = random.randint(0, num_apps - 1)


    sim_log.log("DEBUG", "===========")
    for node_index, app_index in enumerate(node_to_application):
        sim_log.log("DEBUG", "...")
        sim_log.log("DEBUG", "\t\tapp_index: ", printlist=[app_index, ", dag_index: ", node_index])
    sim_log.log("DEBUG", "===========")

    sim_log.log("DEBUG", "Pace Tasks ===========")
    pace_tasks = pace.get_pace_tasks_of_all_applications(applications, power_cap)
    for app_index, task in enumerate(pace_tasks):
        sim_log.log("DEBUG", "...")
        sim_log.log("DEBUG", "\tapp_index: ", printlist=[app_index, " \tconfigIndex: ", task.configIndex, " time: ", task.time, " speed: ", task.speed, " power: ", task.power, " workload: ", task.workload])
    sim_log.log("DEBUG", "Pace Tasks ===========")

#    sim_log.log("INFO", "Corresponding Tasks ===========")
#    corresponding_tasks = pace.get_corresponding_tasks_of_all_applications(applications, power_cap/num_machines)
#    for app_index, task in enumerate(corresponding_tasks):
#        sim_log.log("INFO", "...")
#        sim_log.log("INFO", "\tapp_index: ", printlist=[app_index, " \tconfigIndex: ", task.configIndex, " time: ", task.time, " speed: ", task.speed, " power: ", task.power, " workload: ", task.workload])
#    sim_log.log("INFO", "Corresponding Tasks ===========")

    dummy_diff = sum(pace_tasks[node_to_application[i]].power for i in range(number_of_nodes_in_dag))/number_of_nodes_in_dag
    simulation_stats[0] += dummy_diff
    sim_log.log("INFO", "Mean Pace Tasks Power:" + str(dummy_diff))

    dummy_diff = sum(pace_tasks[node_to_application[i]].power*pace_tasks[node_to_application[i]].time*rand_wl_scale[i] for i in range(number_of_nodes_in_dag))/sum(pace_tasks[node_to_application[i]].time*rand_wl_scale[i] for i in range(number_of_nodes_in_dag))
    simulation_stats[1] += dummy_diff
    sim_log.log("INFO", "Time Weighted Mean Pace Tasks Power:" + str(dummy_diff))

    dummy_diff = sorted(pace_tasks, key=lambda x: x.power)[int(len(pace_tasks)/2 +1)].power
    simulation_stats[2] += dummy_diff
    sim_log.log("INFO", "Median Pace Tasks Power:" + str(dummy_diff))

    dummy_diff = sum(pace_tasks[node_to_application[i]].time*rand_wl_scale[i] for i in range(number_of_nodes_in_dag))/number_of_nodes_in_dag
    simulation_stats[3] += dummy_diff
    sim_log.log("INFO", "Mean Pace Tasks Time:" + str(dummy_diff))

    dummy_diff = (sorted(pace_tasks, key=lambda x: x.time)[int(len(pace_tasks)/2 +1)].time )*rand_scale_mean
    simulation_stats[4] += dummy_diff
    sim_log.log("INFO", "Median Pace Tasks Time:" + str(dummy_diff))





    #sim_log.log("INFO", "Assigning power cap based on", printlist=[len(all_pace_tasks), "tasks..."])
    sim_log.log("INFO", "Power cap: " + str(power_cap) + " W")
    sim_log.log("INFO", "Number of DAG nodes:"+ str(number_of_nodes_in_dag))
    sim_log.log("INFO", "Simulation iteration: "+ str(simulation_count_current) + " out of "+ str(simulation_count))


    runs = []
    runs_op = []
    runs_dc = []
    runs_greedy = []
    runs_naive = []



    #if NAIVE:

    #if DIVIDECONQUER:





    outDir = "output"

    def runs2file(runs, fileName):
        outfile = open(os.path.join(outDir,fileName), "w")
        tab = "\t"
        nl = "\n"
        for run in runs:
            if run.config_index == -1:
                sim_log.log("CRITICAL", "Found an idle task in run file " + fileName + ", which is not supposed to happen.")
                outFile.close()
                sys.exit(1)
            line = str(run.start_time) + tab + str(run.end_time) + tab + str(run.power_start) + tab + str(run.power_end) + tab + str(run.power) + tab + str(run.speed) + tab + str(run.workload) + tab + str(run.app_id) + tab + str(run.config_index) + tab + str(run.dag_index) + nl
            outfile.write(line)
        outfile.close()


    #Theoretical possible
    sim_log.log("INFO", "Finish time and total energy, possible Optimal: \t\t\t" + str(int(sum(pace_tasks[node_to_application[job]].power*pace_tasks[node_to_application[job]].time*(rand_wl_scale[job]) for job in range(number_of_nodes_in_dag))/power_cap)) + ' \t' + str(int(sum(pace_tasks[node_to_application[job]].power*pace_tasks[node_to_application[job]].time*(rand_wl_scale[job]) for job in range(number_of_nodes_in_dag)))) )
    simulation_results_makespan[8] += sum(pace_tasks[node_to_application[job]].power*pace_tasks[node_to_application[job]].time*(rand_wl_scale[job]) for job in range(number_of_nodes_in_dag))/power_cap
    simulation_results_energy[8]  += sum(pace_tasks[node_to_application[job]].power*pace_tasks[node_to_application[job]].time*(rand_wl_scale[job]) for job in range(number_of_nodes_in_dag))
    simulation_results_makespan_last_sim = sum(pace_tasks[node_to_application[job]].power*pace_tasks[node_to_application[job]].time*(rand_wl_scale[job]) for job in range(number_of_nodes_in_dag))/power_cap
    simulation_results_energy_last_sim  = sum(pace_tasks[node_to_application[job]].power*pace_tasks[node_to_application[job]].time*(rand_wl_scale[job]) for job in range(number_of_nodes_in_dag))




    idle_pow = 90

    if NAIVE:


        time1 = time.clock()
        runs_naive = greedy_algorithms.naive_grab_all_run_all(num_machines, number_of_nodes_in_dag, dag_adj_list_by_index, node_to_application, rand_wl_scale, applications, power_cap)
        time2 = time.clock()
        runs_naive.sort(key=lambda x: x.end_time)
        #runs2file(runs_naive, "naive-greedy-" +dag_name+".txt")
        idle_energy_naive = runs_naive[-1].end_time * idle_pow * num_machines
        runtime_energy_naive = sum(run.power*(run.end_time - run.start_time) for run in runs_naive)
        sim_log.log("INFO", "Finish time and total power, time of naive : \t\t\t\t" + str(int(runs_naive[-1].end_time)) + ' \t' + str(int(idle_energy_naive + runtime_energy_naive))+' = '+str(int(idle_energy_naive)) +  ' + ' + str(int(runtime_energy_naive)) + ' \t\t' + str((time2-time1)))
        #plot.draw_pow_opt("naive-greedy-"+dag_name, ".txt", power_cap, True, False)
        simulation_results_makespan[9] += runs_naive[-1].end_time
        simulation_results_energy[9] += runtime_energy_naive
        simulation_results_makespan_percent[9] += 100*((runs_naive[-1].end_time - simulation_results_makespan_last_sim)/simulation_results_makespan_last_sim)
        simulation_results_energy_percent[9] += 100*((runtime_energy_naive-simulation_results_energy_last_sim)/simulation_results_energy_last_sim)
        simulation_results_exectime[9] += time2-time1



        time1 = time.clock()
        runs_greedy = greedy_algorithms.greedy_scheduling(num_machines, number_of_nodes_in_dag, dag_adj_list_by_index, node_to_application, rand_wl_scale, applications, power_cap, 1)
        time2 = time.clock()
        runs_greedy.sort(key=lambda x: x.end_time)
        #runs2file(runs_greedy, "greedy-level-1" + "-" +dag_name+".txt")
        idle_energy_greedy = runs_greedy[-1].end_time * idle_pow * num_machines
        runtime_energy_greedy = sum(run.power*(run.end_time - run.start_time) for run in runs_greedy)
        sim_log.log("INFO", "Finish time and total power, time of greedy lookahead " + str(1) + ' : \t\t' + str(int(runs_greedy[-1].end_time)) + ' \t' + str(int(idle_energy_greedy + runtime_energy_greedy))+' = '+str(int(idle_energy_greedy)) + ' + '+str(int(runtime_energy_greedy)) + ' \t\t' + str((time2-time1)))
        #plot.draw_pow_opt("greedy-level-1" + "-"+dag_name, ".txt", power_cap, True, False)
        simulation_results_makespan[0] += runs_greedy[-1].end_time
        simulation_results_energy[0] += runtime_energy_greedy
        simulation_results_makespan_percent[0] += 100*((runs_greedy[-1].end_time - simulation_results_makespan_last_sim)/simulation_results_makespan_last_sim)
        simulation_results_energy_percent[0] += 100*((runtime_energy_greedy-simulation_results_energy_last_sim)/simulation_results_energy_last_sim)
        simulation_results_exectime[0] += time2-time1


        time1 = time.clock()
        runs_greedy = greedy_algorithms.greedy_scheduling(num_machines, number_of_nodes_in_dag, dag_adj_list_by_index, node_to_application, rand_wl_scale, applications, power_cap, 10)
        time2 = time.clock()
        runs_greedy.sort(key=lambda x: x.end_time)
        #runs2file(runs_greedy, "greedy-level-" +lookahead_str+"-" +dag_name+".txt")
        idle_energy_greedy = runs_greedy[-1].end_time * idle_pow * num_machines
        runtime_energy_greedy = sum(run.power*(run.end_time - run.start_time) for run in runs_greedy)
        sim_log.log("INFO", "Finish time and total power, time of greedy lookahead " + str(10) + ' : \t\t' + str(int(runs_greedy[-1].end_time)) + ' \t' + str(int(idle_energy_greedy + runtime_energy_greedy))+' = '+str(int(idle_energy_greedy)) + ' + '+str(int(runtime_energy_greedy)) + ' \t\t' + str((time2-time1)))
        #plot.draw_pow_opt("greedy-level-" +lookahead_str+"-"+dag_name, ".txt", power_cap, True, False)
        simulation_results_makespan[1] += runs_greedy[-1].end_time
        simulation_results_energy[1] += runtime_energy_greedy
        simulation_results_makespan_percent[1] += 100*((runs_greedy[-1].end_time - simulation_results_makespan_last_sim)/simulation_results_makespan_last_sim)
        simulation_results_energy_percent[1] += 100*((runtime_energy_greedy-simulation_results_energy_last_sim)/simulation_results_energy_last_sim)
        simulation_results_exectime[1] += time2-time1


        time1 = time.clock()
        runs_greedy = greedy_algorithms.greedy_scheduling(num_machines, number_of_nodes_in_dag, dag_adj_list_by_index, node_to_application, rand_wl_scale, applications, power_cap, 20)
        time2 = time.clock()
        runs_greedy.sort(key=lambda x: x.end_time)
        #runs2file(runs_greedy, "greedy-level-" +lookahead_str+"-" +dag_name+".txt")
        idle_energy_greedy = runs_greedy[-1].end_time * idle_pow * num_machines
        runtime_energy_greedy = sum(run.power*(run.end_time - run.start_time) for run in runs_greedy)
        sim_log.log("INFO", "Finish time and total power, time of greedy lookahead " + str(20) + ' : \t\t' + str(int(runs_greedy[-1].end_time)) + ' \t' + str(int(idle_energy_greedy + runtime_energy_greedy))+' = '+str(int(idle_energy_greedy)) + ' + '+str(int(runtime_energy_greedy)) + ' \t\t' + str((time2-time1)))
        #plot.draw_pow_opt("greedy-level-" +lookahead_str+"-"+dag_name, ".txt", power_cap, True, False)
        simulation_results_makespan[2] += runs_greedy[-1].end_time
        simulation_results_energy[2] += runtime_energy_greedy
        simulation_results_makespan_percent[2] += 100*((runs_greedy[-1].end_time - simulation_results_makespan_last_sim)/simulation_results_makespan_last_sim)
        simulation_results_energy_percent[2] += 100*((runtime_energy_greedy-simulation_results_energy_last_sim)/simulation_results_energy_last_sim)
        simulation_results_exectime[2] += time2-time1

        '''

        time1 = time.clock()
        runs_greedy = greedy_algorithms.greedy_scheduling(num_machines, number_of_nodes_in_dag, dag_adj_list_by_index, node_to_application,  rand_wl_scale, applications, power_cap, 50)
        time2 = time.clock()
        runs_greedy.sort(key=lambda x: x.end_time)
        #runs2file(runs_greedy, "greedy-level-" +lookahead_str+"-" +dag_name+".txt")
        idle_energy_greedy = runs_greedy[-1].end_time * idle_pow * num_machines
        runtime_energy_greedy = sum(run.power*(run.end_time - run.start_time) for run in runs_greedy)
        sim_log.log("INFO", "Finish time and total power, time of greedy lookahead " + str(50) + ' : \t\t' + str(int(runs_greedy[-1].end_time)) + ' \t' + str(int(idle_energy_greedy + runtime_energy_greedy))+' = '+str(int(idle_energy_greedy)) + ' + '+str(int(runtime_energy_greedy)) + ' \t\t' + str((time2-time1)))
        #plot.draw_pow_opt("greedy-level-" +lookahead_str+"-"+dag_name, ".txt", power_cap, True, False)
        simulation_results_makespan[3] += runs_greedy[-1].end_time
        simulation_results_energy[3] += runtime_energy_greedy
        simulation_results_makespan_percent[3] += 100*((runs_greedy[-1].end_time - simulation_results_makespan_last_sim)/simulation_results_makespan_last_sim)
        simulation_results_energy_percent[3] += 100*((runtime_energy_greedy-simulation_results_energy_last_sim)/simulation_results_energy_last_sim)
        simulation_results_exectime[3] += time2-time1

        time1 = time.clock()
        runs_greedy = greedy_algorithms.greedy_scheduling(num_machines, number_of_nodes_in_dag, dag_adj_list_by_index, node_to_application, rand_wl_scale, applications, power_cap, 100)
        time2 = time.clock()
        runs_greedy.sort(key=lambda x: x.end_time)
        #runs2file(runs_greedy, "greedy-level-" +lookahead_str+"-" +dag_name+".txt")
        idle_energy_greedy = runs_greedy[-1].end_time * idle_pow * num_machines
        runtime_energy_greedy = sum(run.power*(run.end_time - run.start_time) for run in runs_greedy)
        sim_log.log("INFO", "Finish time and total power, time of greedy lookahead " + str(100) + ' : \t\t' + str(int(runs_greedy[-1].end_time)) + ' \t' + str(int(idle_energy_greedy + runtime_energy_greedy))+' = '+str(int(idle_energy_greedy)) + ' + '+str(int(runtime_energy_greedy)) + ' \t\t' + str((time2-time1)))
        #plot.draw_pow_opt("greedy-level-" +lookahead_str+"-"+dag_name, ".txt", power_cap, True, False)
        simulation_results_makespan[4] += runs_greedy[-1].end_time
        simulation_results_energy[4] += runtime_energy_greedy
        simulation_results_makespan_percent[4] += 100*((runs_greedy[-1].end_time - simulation_results_makespan_last_sim)/simulation_results_makespan_last_sim)
        simulation_results_energy_percent[4] += 100*((runtime_energy_greedy-simulation_results_energy_last_sim)/simulation_results_energy_last_sim)
        simulation_results_exectime[4] += time2-time1
        '''

    if DIVIDECONQUER:
        time3 = time.clock()
        runs_dc = divide_and_conquer.divide_and_conquer_scheduler(num_machines, 20, number_of_nodes_in_dag, dag_adj_list_by_index, node_to_application, rand_wl_scale, applications, power_cap, random_mid_point  = False)
        time4 = time.clock()
        runs_dc.sort(key=lambda x: x.end_time)
        #runs2file(runs_dc, "d&c-"+dag_name+".txt")
        idle_energy_dc = runs_dc[-1].end_time * idle_pow * num_machines
        runtime_energy_dc = sum(run.power*(run.end_time - run.start_time) for run in runs_dc)
        sim_log.log("INFO", "Finish time and total energy (idle+active), time of D&C:  \t\t" + str(int(runs_dc[-1].end_time)) + ' \t' + str(int(idle_energy_dc + runtime_energy_dc))+' = '+str(int(idle_energy_dc)) + ' + '+str(int(runtime_energy_dc)) + ' \t\t' + str((time4-time3)))
        #plot.draw_pow_opt("d&c-"+dag_name, ".txt", power_cap, True, False)
        simulation_results_makespan[5] += runs_dc[-1].end_time
        simulation_results_energy[5] += runtime_energy_dc
        simulation_results_makespan_percent[5] += 100*((runs_dc[-1].end_time - simulation_results_makespan_last_sim)/simulation_results_makespan_last_sim)
        simulation_results_energy_percent[5] += 100*((runtime_energy_dc-simulation_results_energy_last_sim)/simulation_results_energy_last_sim)
        simulation_results_exectime[5] += time4-time3


        # DC random
        time3 = time.clock()
        random_dc_runtime = float('Inf')
        random_dc_energy = float('Inf')
        for random_tries in range(3):
            runs_dc_random = divide_and_conquer.divide_and_conquer_scheduler(num_machines, 20, number_of_nodes_in_dag, dag_adj_list_by_index, node_to_application, rand_wl_scale, applications, power_cap, random_mid_point = True)
            runs_dc_random.sort(key=lambda x: x.end_time)
            idle_energy_dc_random = runs_dc_random[-1].end_time * idle_pow * num_machines
            runtime_energy_dc_random = sum(run.power*(run.end_time - run.start_time) for run in runs_dc_random)
            if random_dc_runtime > runs_dc_random[-1].end_time:
                random_dc_runtime = runs_dc_random[-1].end_time
                random_dc_energy = runtime_energy_dc_random
        time4 = time.clock()

        #runs2file(runs_dc_random, "d&c-random-"+dag_name+".txt")
        sim_log.log("INFO", "Finish time and total energy (idle+active), time of D&C Random:  \t" + str(int(random_dc_runtime)) + ' \t' + str(int(random_dc_runtime* idle_pow * num_machines + random_dc_energy))+' = '+str(int(random_dc_runtime* idle_pow * num_machines)) + ' + '+str(int(random_dc_energy))+ ' \t\t' + str((time4-time3)))
        #plot.draw_pow_opt("d&c-random-"+dag_name, ".txt", power_cap, True, False)
        simulation_results_makespan[6] += random_dc_runtime
        simulation_results_energy[6] += random_dc_energy
        simulation_results_makespan_percent[6] += 100*((random_dc_runtime - simulation_results_makespan_last_sim)/simulation_results_makespan_last_sim)
        simulation_results_energy_percent[6] += 100*((random_dc_energy - simulation_results_energy_last_sim)/simulation_results_energy_last_sim)
        simulation_results_exectime[6] += time4-time3


        '''
        #DC Experimental
        time3 = time.clock()
        runs_dc_exp = divide_and_conquer.divide_and_conquer_scheduler(num_machines, int(number_of_nodes_in_dag/num_machines)+1, number_of_nodes_in_dag, dag_adj_list_by_index, node_to_application, rand_wl_scale, applications, power_cap, random_mid_point  = False)
        time4 = time.clock()
        runs_dc_exp.sort(key=lambda x: x.end_time)
        #runs2file(runs_dc, "d&c-"+dag_name+".txt")
        idle_energy_dc = runs_dc_exp[-1].end_time * idle_pow * num_machines
        runtime_energy_dc = sum(run.power*(run.end_time - run.start_time) for run in runs_dc_exp)
        sim_log.log("INFO", "Finish time and total energy (idle+active), time of D&C EXPERIMENTAL:  " + str(int(runs_dc_exp[-1].end_time)) + ' \t' + str(int(idle_energy_dc + runtime_energy_dc))+' = '+str(int(idle_energy_dc)) + ' + '+str(int(runtime_energy_dc)) + ' \t\t' + str((time4-time3)))
        #plot.draw_pow_opt("d&c-"+dag_name, ".txt", power_cap, True, False)
        simulation_results_makespan[7] += runs_dc_exp[-1].end_time
        simulation_results_energy[7] += runtime_energy_dc
        simulation_results_makespan_percent[7] += 100*((runs_dc_exp[-1].end_time - simulation_results_makespan_last_sim)/simulation_results_makespan_last_sim)
        simulation_results_energy_percent[7] += 100*((runtime_energy_dc - simulation_results_energy_last_sim)/simulation_results_energy_last_sim)
        simulation_results_exectime[7] += time4-time3
        '''




sim_log.log("INFO", "***************************************")
sim_log.log("INFO", "***************************************")
sim_log.log("INFO", "Simulation Stats, (mean) Mean Pace Tasks Power:" + str(int(simulation_stats[0]/simulation_count)))
sim_log.log("INFO", "Simulation Stats, (mean) Time Weighted Mean Pace Tasks Power:" + str(int(simulation_stats[1]/simulation_count)))
sim_log.log("INFO", "Simulation Stats, (mean) Median Pace Tasks Power:" + str(int(simulation_stats[2]/simulation_count)))
sim_log.log("INFO", "Simulation Stats, (mean) Mean Pace Tasks Time:" + str(int(simulation_stats[3]/simulation_count)))
sim_log.log("INFO", "Simulation Stats, (mean) Median Pace Tasks Time:" + str(int(simulation_stats[4]/simulation_count)))
sim_log.log("INFO", "***************************************")
sim_log.log("INFO", "Simulation Stats, Final Results with num_machines: " + str(num_machines) + ' Power cap: ' + str(power_cap) + ' DAG: ' + str(dag_name) + ' simulation count: ' + str(simulation_count)  )
sim_log.log("INFO", "Finish time and total energy, possible Optimal: \t\t\t\t" + str(int(simulation_results_makespan[8])) + ' \t\t' + str(int(simulation_results_energy[8])) )
sim_log.log("INFO", "Finish time and total energy, time of Naive Grab all Run all, makespan:  \t" + str(int(simulation_results_makespan_percent[9]/simulation_count)) +'%' + '('+ str(int(simulation_results_makespan[9])) +')'+ ' \t Energy (excluding idle) used: ' + str(int(simulation_results_energy_percent[9]/simulation_count)) +'%' + ' ('+ str(int(simulation_results_energy[9])) +')' + ' \t Energy not utilized, permille: ' + str(int(simulation_results_makespan[9]*power_cap - simulation_results_energy[9])) + ' ‰' + str(int(1000*(simulation_results_makespan[9]*power_cap - simulation_results_energy[9])/(simulation_results_makespan[9]*power_cap))) + ' \t in run time: ' + str(int(10*simulation_results_exectime[9])))
sim_log.log("INFO", "Finish time and total energy, time of Greedy lookahead " + str(1) + ' makepsan: \t\t' + str(int(simulation_results_makespan_percent[0]/simulation_count)) +'%' + '('+ str(int(simulation_results_makespan[0])) +')'+ ' \t Energy (excluding idle) used: ' + str(int(simulation_results_energy_percent[0]/simulation_count)) +'%' + ' ('+ str(int(simulation_results_energy[0])) +')'+ ' \t Energy not utilized, permille: ' + str(int(simulation_results_makespan[0]*power_cap - simulation_results_energy[0])) + ' ‰' + str(int(1000*(simulation_results_makespan[0]*power_cap - simulation_results_energy[0])/(simulation_results_makespan[0]*power_cap))) + ' \t in run time: ' + str(int(10*simulation_results_exectime[0])))
sim_log.log("INFO", "Finish time and total energy, time of Greedy lookahead " + str(10) + ' makepsan: \t\t' + str(int(simulation_results_makespan_percent[1]/simulation_count)) +'%' + '('+ str(int(simulation_results_makespan[1])) +')'+ ' \t Energy (excluding idle) used: ' + str(int(simulation_results_energy_percent[1]/simulation_count)) +'%' + ' ('+ str(int(simulation_results_energy[1])) +')'+ ' \t Energy not utilized, permille: ' + str(int(simulation_results_makespan[1]*power_cap - simulation_results_energy[1])) + ' ‰' + str(int(1000*(simulation_results_makespan[1]*power_cap - simulation_results_energy[1])/(simulation_results_makespan[1]*power_cap))) + ' \t in run time: ' + str(int(10*simulation_results_exectime[1])))
sim_log.log("INFO", "Finish time and total energy, time of Greedy lookahead " + str(20) + ' makepsan: \t\t' + str(int(simulation_results_makespan_percent[2]/simulation_count)) +'%' + '('+ str(int(simulation_results_makespan[2])) +')'+ ' \t Energy (excluding idle) used: ' + str(int(simulation_results_energy_percent[2]/simulation_count)) +'%' + ' ('+ str(int(simulation_results_energy[2])) +')'+ ' \t Energy not utilized, permille: ' + str(int(simulation_results_makespan[2]*power_cap - simulation_results_energy[2])) + ' ‰' + str(int(1000*(simulation_results_makespan[2]*power_cap - simulation_results_energy[2])/(simulation_results_makespan[2]*power_cap))) + ' \t in run time: ' + str(int(10*simulation_results_exectime[2])))
#sim_log.log("INFO", "Finish time and total energy, time of Greedy lookahead " + str(50) + ' makepsan: \t\t' + str(int(simulation_results_makespan_percent[3]/simulation_count)) +'%' + '('+ str(int(simulation_results_makespan[3])) +')'+ ' \t Energy (excluding idle) used: ' + str(int(simulation_results_energy_percent[3]/simulation_count)) +'%' + ' ('+ str(int(simulation_results_energy[3])) +')'+ ' \t Energy not utilized, permille: ' + str(int(simulation_results_makespan[3]*power_cap - simulation_results_energy[3])) + ' ‰' + str(int(1000*(simulation_results_makespan[3]*power_cap - simulation_results_energy[3])/(simulation_results_makespan[3]*power_cap))) + ' \t in run time: ' + str(int(10*simulation_results_exectime[3])))
#sim_log.log("INFO", "Finish time and total energy, time of Greedy lookahead " + str(100) + ' makepsan: \t\t' + str(int(simulation_results_makespan_percent[4]/simulation_count)) +'%' + '('+ str(int(simulation_results_makespan[4])) +')'+ ' \t Energy (excluding idle) used: ' + str(int(simulation_results_energy_percent[4]/simulation_count)) +'%' + ' ('+ str(int(simulation_results_energy[4])) +')'+ ' \t Energy not utilized, permille: ' + str(int(simulation_results_makespan[4]*power_cap - simulation_results_energy[4])) + ' ‰' + str(int(1000*(simulation_results_makespan[4]*power_cap - simulation_results_energy[4])/(simulation_results_makespan[4]*power_cap))) + ' \t in run time: ' + str(int(10*simulation_results_exectime[4])))
sim_log.log("INFO", "Finish time and total energy, time of D&C makepsan:  \t\t\t\t" + str(int(simulation_results_makespan_percent[5]/simulation_count)) +'%' + '('+ str(int(simulation_results_makespan[5])) +')'+ ' \t Energy (excluding idle) used: ' + str(int(simulation_results_energy_percent[5]/simulation_count)) +'%' + ' ('+ str(int(simulation_results_energy[5])) +')' + ' \t Energy not utilized, permille: ' + str(int(simulation_results_makespan[5]*power_cap - simulation_results_energy[5])) + ' ‰' + str(int(1000*(simulation_results_makespan[5]*power_cap - simulation_results_energy[5])/(simulation_results_makespan[5]*power_cap))) + ' \t in run time: ' + str(int(10*simulation_results_exectime[5])))
sim_log.log("INFO", "Finish time and total energy, time of D&C RANDOM makepsan:  \t\t\t" + str(int(simulation_results_makespan_percent[6]/simulation_count)) +'%' + '('+ str(int(simulation_results_makespan[6])) +')'+ ' \t Energy (excluding idle) used: ' + str(int(simulation_results_energy_percent[6]/simulation_count)) +'%' + ' ('+ str(int(simulation_results_energy[6])) + ')' + ' \t Energy not utilized, permille: ' + str(int(simulation_results_makespan[6]*power_cap - simulation_results_energy[6])) + ' ‰' + str(int(1000*(simulation_results_makespan[6]*power_cap - simulation_results_energy[6])/(simulation_results_makespan[6]*power_cap))) + ' \t in run time: ' + str(int(10*simulation_results_exectime[6])))
#sim_log.log("INFO", "Finish time and total energy, time of D&C EXPERIMENTAL makepsan:  \t\t" + str(int(simulation_results_makespan_percent[7]/simulation_count)) +'%' + '('+ str(int(simulation_results_makespan[7])) +')'+ ' \t Energy (excluding idle) used: ' + str(int(simulation_results_energy_percent[7]/simulation_count)) +'%' + ' ('+ str(int(simulation_results_energy[7])) + ')' + ' \t Energy not utilized, permille: ' + str(int(simulation_results_makespan[7]*power_cap - simulation_results_energy[7])) + ' ‰' + str(int(1000*(simulation_results_makespan[7]*power_cap - simulation_results_energy[7])/(simulation_results_makespan[7]*power_cap))) + ' \t in run time: ' + str(int(10*simulation_results_exectime[7])))
sim_log.log("INFO", "***************************************")
sim_log.log("INFO", "***************************************")
