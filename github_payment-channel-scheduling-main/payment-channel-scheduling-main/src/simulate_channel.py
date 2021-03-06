"""
This script uses Discrete Event Simulation via SimPy to simulate a single payment channel.

Transactions are generated from both sides according to customizable distributions of amounts and arrival times.

Input parameters:
    - node_0_parameters:    :   [initial_balance_0, total_transactions_0, exp_mean_0, amount_distribution_0, amount_distribution_parameters_0, deadline_distribution_0]
    - node_1_parameters     :   [initial_balance_1, total_transactions_1, exp_mean_1, amount_distribution_1, amount_distribution_parameters_1, deadline_distribution_1]
    - scheduling_policy
    - buffer_discipline
    - buffering_capability
    - max_buffering_time
    - verbose
    - seed

Output:
- results = {
        'measurement_interval_length': measurement_interval[1] - measurement_interval[0],
        'success_counts': [success_count_node_0, success_count_node_1, success_count_channel_total],
        'arrived_counts': [arrived_count_node_0, arrived_count_node_1, arrived_count_channel_total],
        'success_amounts': [success_amount_node_0, success_amount_node_1, success_amount_channel_total],
        'arrived_amounts': [arrived_amount_node_0, arrived_amount_node_1, arrived_amount_channel_total],
        'sacrificed_counts': [sacrificed_count_node_0, sacrificed_count_node_1, sacrificed_count_channel_total],
        'sacrificed_amounts': [sacrificed_amount_node_0, sacrificed_amount_node_1, sacrificed_amount_channel_total],
        'success_rates': [success_rate_node_0, success_rate_node_1, success_rate_channel_total],
        'normalized_throughputs': [normalized_throughput_node_0, normalized_throughput_node_1, normalized_throughput_channel_total],
        'total_queueing_times': [total_queueing_time_of_successful_transactions, total_queueing_time_of_all_transactions, average_total_queueing_time_per_successful_unit_amount, average_total_queueing_time_per_successful_transaction]
    }
- all_transactions_list

Hardcoded parameters: checkInterval

"""


from numpy import random, recfromcsv
import simpy
import sys
# import powerlaw
import pandas as pd
import sortedcontainers as sc
from fractions import Fraction
from math import inf


class Transaction:
    def __init__(self, env, channel, time_of_arrival, from_node, to_node, amount, max_buffering_time, verbose):
        self.env = env
        self.channel = channel
        self.time_of_arrival = time_of_arrival
        self.from_node = from_node
        self.to_node = to_node
        self.amount = amount
        self.max_buffering_time = max_buffering_time
        self.verbose = verbose
        self.buffered = False
        self.status = "PENDING"     # Other statuses: "SUCCEEDED", "REJECTED", "EXPIRED"
        # self.initially_feasible = None
        self.request = None
        self.preemptied = self.env.event()
        self.time_of_departure = - 1.0  # initialization meaning transaction has not departed the channel yet

        if self.verbose:
            print("Time {:.2f}: Transaction {} generated.".format(self.env.now, self))

        # Start the run process every time an instance is created.
        # env.process(self.run())

    def run(self):
        if self.status == "PENDING":
            with self.channel.channel_link.request() as request:    # Generate a request event
                yield request                                       # Wait for access to the channel
                self.request = request
                yield self.env.process(self.channel.process_transaction(self))              # Once the channel belongs to the transaction, try to process it.

    def __repr__(self):
        return "%d->%d t=%.2f D=%.2f a=%d" % (self.from_node, self.to_node, self.time_of_arrival, self.max_buffering_time, self.amount)


class Channel:

    def __init__(self, env, node0, node1, balances, buffering_capability, scheduling_policy, buffer_discipline, deadline_fraction,
                 verbose, total_simulation_time_estimation):
        self.env = env
        self.node0 = node0
        self.node1 = node1
        self.capacity = balances[0] + balances[1]
        self.balances = balances
        self.scheduling_policy = scheduling_policy
        self.buffer_discipline = buffer_discipline
        self.deadline_fraction = deadline_fraction
        self.immediate_processing = True if (scheduling_policy == "PRI-IP") else False
        self.verbose = verbose
        self.channel_link = simpy.Resource(env, capacity=1)
        self.successful_transactions = [0, 0]
        self.successful_amounts = [0, 0]
        self.balance_history_node_0_times = []
        self.balance_history_node_0_values = []

        if buffering_capability == "neither_node":
            self.buffers = [None, None]
        elif buffering_capability == "only_node_0":
            self.buffers = [Buffer(env, node0, self, self.scheduling_policy, self.buffer_discipline, verbose, total_simulation_time_estimation), None]
            self.env.process(self.buffers[0].run())
        elif buffering_capability == "only_node_1":
            self.buffers = [None, Buffer(env, node1, self, self.scheduling_policy, self.buffer_discipline, verbose, total_simulation_time_estimation)]
            self.env.process(self.buffers[1].run())
        elif (buffering_capability == "both_separate") or (buffering_capability == "both_shared" and self.scheduling_policy == "PMDE"):
            self.buffers = [Buffer(env, node0, self, self.scheduling_policy, self.buffer_discipline, verbose, total_simulation_time_estimation),
                            Buffer(env, node1, self, self.scheduling_policy, self.buffer_discipline, verbose, total_simulation_time_estimation)]
            self.env.process(self.buffers[0].run())
            self.env.process(self.buffers[1].run())
        elif (buffering_capability == "both_shared") and (self.scheduling_policy != "PMDE"):
            shared_buffer = Buffer(env, node0, self, self.scheduling_policy, self.buffer_discipline, verbose, total_simulation_time_estimation)
            self.buffers = [shared_buffer, shared_buffer]
            self.env.process(self.buffers[0].run())
        else:
            print("Input error: {} is not a valid 'buffering_capability' value.".format(buffering_capability))
            sys.exit(1)

    def execute_feasible_transaction(self, t):
        # Calling this function requires checking for transaction feasibility beforehand. The function itself does not perform any checks, and this could lead to negative balances if misused.

        FT = t.buffered is False  # First Time

        self.balances[t.from_node] -= t.amount
        self.balances[t.to_node] += t.amount
        self.successful_transactions[t.from_node] += 1
        self.successful_amounts[t.from_node] += t.amount
        self.balance_history_node_0_times.append(self.env.now)
        self.balance_history_node_0_values.append(self.balances[0])

        if self.verbose:
            if FT:
                print("Time {:.2f}: SUCCESS: Transaction {} processed.".format(self.env.now, t))
            else:
                print("Time {:.2f}: SUCCESS: Transaction {} was processed and removed from buffer.".format(self.env.now, t))
            print("Time {:.2f}: New balances are {}.".format(self.env.now, self.balances))

        t.status = "SUCCEEDED"
        t.time_of_departure = self.env.now

    def reject_transaction(self, t):
        FT = t.buffered is False  # First Time

        if self.verbose:
            if FT:
                print("Time {:.2f}: FAILURE: Transaction {} rejected.".format(self.env.now, t))
                print("Time {:.2f}: Unchanged balances are {}.".format(self.env.now, self.balances))
            else:
                print("Time {:.2f}: FAILURE: Transaction {} expired and was removed from buffer.".format(self.env.now, t))
        t.status = "REJECTED"
        t.time_of_departure = self.env.now

    def add_transaction_to_buffer(self, t):

        self.buffers[t.from_node].transaction_list.add(t)

        t.buffered = True
        if self.verbose:
            print("Time {:.2f}: Transaction {} added to buffer of node {}.".format(self.env.now, t, t.from_node))
            print("Time {:.2f}: Unchanged balances are {}.".format(self.env.now, self.balances))
            self.print_buffers()
        # t.status = "PENDING"  # t.status is "PENDING" already

    def process_transaction(self, t):

        if t.status != "PENDING":
            print("Time {:.2f}: Error in process_transaction(): attempt to process non-pending transaction (of status \"{}\").".format(self.env.now, t.status))
            sys.exit(1)

        IP = self.immediate_processing                  # Immediate Processing
        BE = self.buffers[t.from_node] is not None      # Buffer Exists
        FT = t.buffered is False                        # First Time
        FE = t.amount <= self.balances[t.from_node]     # FEasible
        # Configurations "not BE and not FT" are not reachable. The remaining 12 of the 16 configurations are covered below.
        oppositeBE = self.buffers[t.to_node] is not None    # Opposite Buffer Exists

        if FT and FE:
            t.initially_feasible = True
        else:
            t.initially_feasible = False

        if self.scheduling_policy == "PFI":
            if FE:
                self.execute_feasible_transaction(t)
            else:
                self.reject_transaction(t)

        elif self.scheduling_policy == "PMDE":
            if not BE and FE:   # process
                self.execute_feasible_transaction(t)
            elif BE:
                self.add_transaction_to_buffer(t)
                deadline = t.time_of_arrival + t.max_buffering_time - self.env.now
                self.channel_link.release(t.request)
                resume_reason = yield self.env.timeout(self.deadline_fraction * deadline) | t.preemptied
                if t.preemptied in resume_reason:
                    return True
                else:
                    with self.channel_link.request() as request:
                        resume_reason = yield request | t.preemptied
                        if request not in resume_reason:
                            return True
                        else:
                            t.request = request
                            if self.verbose:
                                fraction_string = (str(Fraction(self.deadline_fraction)) + " of deadline") if self.deadline_fraction < 1 else "Deadline"
                                print("Time {:.2f}: {} of {} is expiring.".format(self.env.now, fraction_string, t))
                            FE_upon_expiration = t.amount <= self.balances[t.from_node]
                            if FE_upon_expiration:
                                self.buffers[t.from_node].transaction_list.remove(t)
                                self.execute_feasible_transaction(t)
                                if self.verbose: self.print_buffers()
                                return True
                            else:
                                if t.amount <= self.balances[t.to_node] and oppositeBE and self.buffers[t.to_node].transaction_list:
                                    # # Version 1: policy for all transaction amounts equal
                                    # opposite_tx = self.buffers[t.to_node].transaction_list.pop(index=0)
                                    # opposite_tx.preemptied.succeed()
                                    # if self.verbose:
                                    #     print("Time {:.2f}: PREEMPTION FOLLOWING:".format(self.env.now))
                                    # self.execute_feasible_transaction(opposite_tx)
                                    # self.buffers[t.from_node].transaction_list.remove(t)
                                    # self.execute_feasible_transaction(t)
                                    # if self.verbose:
                                    #     if self.buffers[0] is not None: print("Buffer 0:", list(self.buffers[0].transaction_list))
                                    #     if self.buffers[1] is not None: print("Buffer 1:", list(self.buffers[1].transaction_list))
                                    # return True

                                    # Version 2: policy for general (possibly unequal) amounts
                                    needed_difference = t.amount - self.balances[t.from_node]
                                    opposite_buffer_index = 0
                                    total_opposite_amount = 0
                                    opposite_txs_to_use = []
                                    while total_opposite_amount < needed_difference and total_opposite_amount < self.balances[t.to_node] and opposite_buffer_index < len(self.buffers[t.to_node].transaction_list):
                                        next_opposite_tx = self.buffers[t.to_node].transaction_list[opposite_buffer_index]
                                        if total_opposite_amount + next_opposite_tx.amount < self.balances[t.to_node]:
                                            total_opposite_amount += next_opposite_tx.amount
                                            opposite_txs_to_use.append(opposite_buffer_index)
                                        opposite_buffer_index += 1

                                    if total_opposite_amount >= needed_difference:
                                        if self.verbose:
                                            print("Time {:.2f}: PREEMPTION FOLLOWING:".format(self.env.now))
                                        while len(opposite_txs_to_use) > 0:
                                            opposite_tx_index = opposite_txs_to_use.pop(0)
                                            opposite_txs_to_use = [x-1 for x in opposite_txs_to_use]
                                            next_opposite_tx = self.buffers[t.to_node].transaction_list.pop(index=opposite_tx_index)
                                            next_opposite_tx.preemptied.succeed()
                                            self.execute_feasible_transaction(next_opposite_tx)
                                        self.buffers[t.from_node].transaction_list.remove(t)
                                        self.execute_feasible_transaction(t)
                                        if self.verbose: self.print_buffers()
                                        return True
                                    else:
                                        self.buffers[t.from_node].transaction_list.remove(t)
                                        self.reject_transaction(t)
                                        if self.verbose: self.print_buffers()
                                        return False
                                else:
                                    self.buffers[t.from_node].transaction_list.remove(t)
                                    self.reject_transaction(t)
                                    if self.verbose: self.print_buffers()
                                    return False

            else:   # reject
                self.reject_transaction(t)
                return False

        elif (self.scheduling_policy == "PRI-IP") or (self.scheduling_policy == "PRI-NIP"):
            if (IP and BE and FT and FE) or (IP and BE and not FT and FE) or (IP and not BE and FT and FE) or (
                    not IP and BE and not FT and FE):  # process
                    # Once the channel belongs to the transaction, then if the deadline has not expired, try to process it.
                    if t.time_of_arrival + t.max_buffering_time >= t.env.now:
                        self.execute_feasible_transaction(t)
                        return True
                    else:   # Transaction expired and will be handled in the next processing of the buffer.
                        return False
            elif (IP and BE and FT and not FE) or (not IP and BE and FT):  # add to buffer
                self.add_transaction_to_buffer(t)
                return False
            elif (IP and not BE and FT and not FE) or (not IP and not BE and FT):  # reject
                self.reject_transaction(t)
                return False
            elif BE and not FT and not FE:  # skip
                pass
                # t.status = "PENDING"  # t.status is "PENDING" already
                return False
            else:
                print("Unreachable state reached. Exiting.")
                # self.channel_link.release(request)
                sys.exit(1)
        else:
            print("Input error: {} is not a valid scheduling policy. Exiting.".format(self.scheduling_policy))
            # self.channel_link.release(request)
            sys.exit(1)

    def print_buffers(self):
        if self.buffers[0] is not None: print("Time {:.2f}: Buffer 0: {}".format(self.env.now, list(self.buffers[0].transaction_list)))
        if self.buffers[1] is not None: print("Time {:.2f}: Buffer 1: {}".format(self.env.now, list(self.buffers[1].transaction_list)))


class Buffer:
    def __init__(self, env, node, channel, scheduling_policy, buffer_discipline, verbose, total_simulation_time_estimation):
        self.env = env
        self.node = node
        self.channel = channel
        # self.max_buffering_time = max_buffering_time
        self.scheduling_policy = scheduling_policy
        self.buffer_discipline = buffer_discipline
        self.verbose = verbose
        self.total_simulation_time_estimation = total_simulation_time_estimation
        # self.total_successes = 0
        self.check_interval = 3

        if self.buffer_discipline == "oldest_first":
            key = lambda t: t.time_of_arrival
        elif self.buffer_discipline == "youngest_first":
            key = lambda t: - t.time_of_arrival
        elif self.buffer_discipline == "closest_deadline_first":
            key = lambda t: t.time_of_arrival + t.max_buffering_time
        elif self.buffer_discipline == "largest_amount_first":
            key = lambda t: t.amount
        elif self.buffer_discipline == "smallest_amount_first":
            key = lambda t: - t.amount
        # elif optimal....
        else:
            print("Input error: {} is not a valid 'buffer_discipline' value.".format(self.buffer_discipline))
            sys.exit(1)

        self.transaction_list = sc.SortedKeyList(key=key)
        # self.transaction_list.__repr__ = lambda skl: list(skl)

    def run(self):
        if self.scheduling_policy in ["PRI-IP", "PRI-NIP"]:
            # while True:
            while self.env.now <= self.total_simulation_time_estimation:
                # s = self.process_buffer()
                # s = self.process_buffer_greedy()
                yield self.env.process(self.process_buffer_greedy())
                # self.total_successes = self.total_successes + s
                yield self.env.timeout(self.check_interval)

    def process_buffer_greedy(self):
        # Processes all transactions that are possible now and returns total successful transactions.
        total_successes_this_time = 0

        for t in self.transaction_list:
            if t.time_of_arrival + t.max_buffering_time < self.env.now:  # if t is too old, reject it and remove it from buffer
                t.status = "EXPIRED"
                t.time_of_departure = self.env.now
                self.transaction_list.remove(t)
                if self.verbose:
                    print("Time {:.2f}: FAILURE: Transaction {} expired and was removed from buffer.".format(self.env.now, t, self.env.now))
                    self.channel.print_buffers()
            else:  # if t is not too old and can be processed, process it
                yield self.env.process(t.run())
                if t.status == "SUCCEEDED":
                    self.transaction_list.remove(t)
                    if self.verbose:
                        self.channel.print_buffers()
                    total_successes_this_time += 1
                else:
                    pass

        return total_successes_this_time


def transaction_generator(env, channel, from_node, total_transactions, exp_mean, amount_distribution, amount_distribution_parameters,
                                      deadline_distribution, max_buffering_time, all_transactions_list, verbose):
    time_to_next_arrival = random.exponential(1.0 / exp_mean)
    yield env.timeout(time_to_next_arrival)

    for _ in range(total_transactions):
        to_node = 1 if (from_node == 0) else 0

        if amount_distribution == "constant":
            amount = amount_distribution_parameters[0]
        elif amount_distribution == "uniform":
            max_transaction_amount = amount_distribution_parameters[0]
            amount = random.randint(1, max_transaction_amount)
        elif amount_distribution == "gaussian":
            max_transaction_amount = amount_distribution_parameters[0]
            gaussian_mean = amount_distribution_parameters[1]
            gaussian_variance = amount_distribution_parameters[2]
            amount = round(max(1, min(max_transaction_amount, random.normal(gaussian_mean, gaussian_variance))))
        # elif amount_distribution == "pareto":
        #     lower = amount_distribution_parameters[0]  # the lower end of the support
        #     shape = amount_distribution_parameters[1]  # the distribution shape parameter, also known as `a` or `alpha`
        #     size = amount_distribution_parameters[2]  # the size of your sample (number of random values)
        #     amount = random.pareto(shape, size) + lower
        # elif amount_distribution == "powerlaw":
            # powerlaw.Power_Law(xmin=1, xmax=2, discrete=True, parameters=[1.16]).generate_random(n=10)
        elif amount_distribution == "empirical_from_csv_file":
            dataset = amount_distribution_parameters[0]
            data_size = amount_distribution_parameters[1]
            amount = dataset[random.randint(0, data_size)]
        else:
            print("Input error: {} is not a supported amount distribution or the parameters {} given are invalid.".format(amount_distribution, amount_distribution_parameters))
            sys.exit(1)

        # Distribution for max_buffering_time
        if deadline_distribution == "constant":
            # max_buffering_time = deadline_distribution_parameters[0]
            t = Transaction(env, channel, env.now, from_node, to_node, amount, max_buffering_time, verbose)
        elif deadline_distribution == "uniform":
            # max_buffering_time = deadline_distribution_parameters[0]
            initial_deadline = random.uniform(0, max_buffering_time) if max_buffering_time > 0 else 0
            t = Transaction(env, channel, env.now, from_node, to_node, amount, initial_deadline, verbose)
        else:
            # print("Input error: {} is not a supported deadline distribution or the parameters {} given are invalid.".format(deadline_distribution, deadline_distribution_parameters))
            print("Input error: {} is not a supported deadline distribution.".format(deadline_distribution))
            sys.exit(1)

        all_transactions_list.append(t)

        env.process(t.run())

        time_to_next_arrival = random.exponential(1.0 / exp_mean)
        yield env.timeout(time_to_next_arrival)


def simulate_channel(node_0_parameters, node_1_parameters, scheduling_policy, buffer_discipline, buffering_capability, max_buffering_time, deadline_fraction, verbose, seed):

    initial_balance_0 = node_0_parameters[0]
    total_transactions_0 = node_0_parameters[1]
    exp_mean_0 = node_0_parameters[2]
    amount_distribution_0 = node_0_parameters[3]
    amount_distribution_parameters_0 = node_0_parameters[4]
    deadline_distribution_0 = node_0_parameters[5]

    initial_balance_1 = node_1_parameters[0]
    total_transactions_1 = node_1_parameters[1]
    exp_mean_1 = node_1_parameters[2]
    amount_distribution_1 = node_1_parameters[3]
    amount_distribution_parameters_1 = node_1_parameters[4]
    deadline_distribution_1 = node_1_parameters[5]

    if amount_distribution_0 == "empirical_from_csv_file":
        amount_distribution_parameters_0 = [amount_distribution_parameters_0, len(amount_distribution_parameters_0)]
    if amount_distribution_1 == "empirical_from_csv_file":
        amount_distribution_parameters_1 = [amount_distribution_parameters_1, len(amount_distribution_parameters_1)]

    total_simulation_time_estimation = max(total_transactions_0 * 1 / exp_mean_0, total_transactions_1 * 1 / exp_mean_1)
    random.seed(seed)

    env = simpy.Environment()

    channel = Channel(env, 0, 1, [initial_balance_0, initial_balance_1], buffering_capability, scheduling_policy, buffer_discipline, deadline_fraction, verbose,
                      total_simulation_time_estimation)

    all_transactions_list = []
    env.process(transaction_generator(env, channel, 0, total_transactions_0, exp_mean_0, amount_distribution_0, amount_distribution_parameters_0,
                                      deadline_distribution_0, max_buffering_time, all_transactions_list, verbose))
    env.process(transaction_generator(env, channel, 1, total_transactions_1, exp_mean_1, amount_distribution_1, amount_distribution_parameters_1,
                                      deadline_distribution_1, max_buffering_time, all_transactions_list, verbose))

    env.run()

    # Calculate results

    measurement_interval = [total_simulation_time_estimation*0.1, total_simulation_time_estimation*0.9]

    success_count_node_0 = sum(1 for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 0) and (t.status == "SUCCEEDED")))
    success_count_node_1 = sum(1 for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 1) and (t.status == "SUCCEEDED")))
    success_count_channel_total = sum(1 for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.status == "SUCCEEDED")))
    arrived_count_node_0 = sum(1 for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 0) and (t.status != "PENDING")))
    arrived_count_node_1 = sum(1 for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 1) and (t.status != "PENDING")))
    arrived_count_channel_total = sum(1 for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.status != "PENDING")))
    success_amount_node_0 = sum(t.amount for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 0) and (t.status == "SUCCEEDED")))
    success_amount_node_1 = sum(t.amount for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 1) and (t.status == "SUCCEEDED")))
    success_amount_channel_total = sum(t.amount for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.status == "SUCCEEDED")))
    arrived_amount_node_0 = sum(t.amount for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 0) and (t.status != "PENDING")))
    arrived_amount_node_1 = sum(t.amount for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 1) and (t.status != "PENDING")))
    arrived_amount_channel_total = sum(t.amount for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.status != "PENDING")))
    sacrificed_count_node_0 = sum(1 for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 0) and (t.initially_feasible is True) and (t.status in ["REJECTED", "EXPIRED"])))
    sacrificed_count_node_1 = sum(1 for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 1) and (t.initially_feasible is True) and (t.status in ["REJECTED", "EXPIRED"])))
    sacrificed_count_channel_total = sum(1 for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.initially_feasible is True) and (t.status in ["REJECTED", "EXPIRED"])))
    sacrificed_amount_node_0 = sum(t.amount for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 0) and (t.initially_feasible is True) and (t.status in ["REJECTED", "EXPIRED"])))
    sacrificed_amount_node_1 = sum(t.amount for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.from_node == 1) and (t.initially_feasible is True) and (t.status in ["REJECTED", "EXPIRED"])))
    sacrificed_amount_channel_total = sum(t.amount for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.initially_feasible is True) and (t.status in ["REJECTED", "EXPIRED"])))
    success_rate_node_0 = success_count_node_0/arrived_count_node_0
    success_rate_node_1 = success_count_node_1/arrived_count_node_1
    success_rate_channel_total = success_count_channel_total / arrived_count_channel_total
    normalized_throughput_node_0 = success_amount_node_0/arrived_amount_node_0      # should be divided by duration of measurement_interval in both numerator and denominator, but these terms cancel out
    normalized_throughput_node_1 = success_amount_node_1/arrived_amount_node_1      # should be divided by duration of measurement_interval in both numerator and denominator, but these terms cancel out
    normalized_throughput_channel_total = success_amount_channel_total/arrived_amount_channel_total     # should be divided by duration of measurement_interval in both numerator and denominator, but these terms cancel out
    total_queueing_time_of_successful_transactions = sum((t.time_of_departure - t.time_of_arrival) for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.status == "SUCCEEDED")))
    total_queueing_time_of_all_transactions = sum((t.time_of_departure - t.time_of_arrival) for t in all_transactions_list if ((t.time_of_arrival >= measurement_interval[0]) and (t.time_of_arrival < measurement_interval[1]) and (t.status != "PENDING")))
    average_total_queueing_time_per_successful_unit_amount = total_queueing_time_of_all_transactions/success_amount_channel_total if success_amount_channel_total > 0 else inf
    average_total_queueing_time_per_successful_transaction = total_queueing_time_of_all_transactions/success_count_channel_total if success_amount_channel_total > 0 else inf

    results = {
        'measurement_interval_length': measurement_interval[1] - measurement_interval[0],
        'success_counts': [success_count_node_0, success_count_node_1, success_count_channel_total],
        'arrived_counts': [arrived_count_node_0, arrived_count_node_1, arrived_count_channel_total],
        'success_amounts': [success_amount_node_0, success_amount_node_1, success_amount_channel_total],
        'arrived_amounts': [arrived_amount_node_0, arrived_amount_node_1, arrived_amount_channel_total],
        'sacrificed_counts': [sacrificed_count_node_0, sacrificed_count_node_1, sacrificed_count_channel_total],
        'sacrificed_amounts': [sacrificed_amount_node_0, sacrificed_amount_node_1, sacrificed_amount_channel_total],
        'success_rates': [success_rate_node_0, success_rate_node_1, success_rate_channel_total],
        'normalized_throughputs': [normalized_throughput_node_0, normalized_throughput_node_1, normalized_throughput_channel_total],
        'total_queueing_times': [total_queueing_time_of_successful_transactions, total_queueing_time_of_all_transactions, average_total_queueing_time_per_successful_unit_amount, average_total_queueing_time_per_successful_transaction]
    }

    print("Total success rate: {:.2f}".format(success_count_channel_total/arrived_count_channel_total))
    print("Total normalized throughput: {:.2f}".format(success_amount_channel_total/arrived_amount_channel_total))
    print("Number of sacrificed transactions (node 0, node 1, total): {}, {}, {}".format(sacrificed_count_node_0, sacrificed_count_node_1, sacrificed_count_channel_total))

    for t in all_transactions_list:
        del t.env
        del t.channel
        del t.request
        del t.preemptied
    all_transactions_list = pd.DataFrame([vars(t) for t in all_transactions_list])

    return results, all_transactions_list


# if __name__ == '__main__':
#     simulate_channel()
