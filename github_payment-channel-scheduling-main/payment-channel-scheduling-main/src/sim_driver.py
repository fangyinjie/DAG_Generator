from pathlib import Path

import pypet
from simulate_channel import *
import csv
from statsmodels.distributions.empirical_distribution import ECDF
from math import floor, ceil


def pypet_wrapper(traj):
    node_0_parameters = [traj.initial_balance_0, traj.total_transactions_0, traj.exp_mean_0, traj.amount_distribution_0,
                         traj.amount_distribution_parameters_0, traj.deadline_distribution_0]
    node_1_parameters = [traj.initial_balance_1, traj.total_transactions_1, traj.exp_mean_1, traj.amount_distribution_1,
                         traj.amount_distribution_parameters_1, traj.deadline_distribution_1]

    results, all_transactions_list = simulate_channel(
        node_0_parameters,
        node_1_parameters,
        traj.scheduling_policy,
        traj.buffer_discipline,
        traj.buffering_capability,
        traj.max_buffering_time,
        traj.deadline_fraction,
        traj.verbose,
        traj.seed
    )

    # traj.f_add_result('measurement_interval_length', results['measurement_interval_length'], comment='Measurement interval length')
    # traj.f_add_result('success_count_node_0', results['success_counts'][0], comment='Number of successful transactions (node 0)')
    # traj.f_add_result('success_count_node_1', results['success_counts'][1], comment='Number of successful transactions (node 1)')
    # traj.f_add_result('success_count_channel_total', results['success_counts'][2], comment='Number of successful transactions (channel total)')
    # traj.f_add_result('arrived_count_node_0', results['arrived_counts'][0], comment='Number of transactions that arrived (node 0)')
    # traj.f_add_result('arrived_count_node_1', results['arrived_counts'][1], comment='Number of transactions that arrived (node 1)')
    # traj.f_add_result('arrived_count_channel_total', results['arrived_counts'][2], comment='Number of transactions that arrived (channel total)')
    # traj.f_add_result('success_amount_node_0', results['success_amounts'][0], comment='Throughput (Amount of successful transactions) (node 0)')
    # traj.f_add_result('success_amount_node_1', results['success_amounts'][1], comment='Throughput (Amount of successful transactions) (node 1)')
    # traj.f_add_result('success_amount_channel_total', results['success_amounts'][2], comment='Throughput (Amount of successful transactions) (channel total)')
    # traj.f_add_result('arrived_amount_node_0', results['arrived_amounts'][0], comment='Amount of transactions that arrived (node 0)')
    # traj.f_add_result('arrived_amount_node_1', results['arrived_amounts'][1], comment='Amount of transactions that arrived (node 1)')
    # traj.f_add_result('arrived_amount_channel_total', results['arrived_amounts'][2], comment='Amount of transactions that arrived (channel total)')
    # traj.f_add_result('sacrificed_count_node_0', results['sacrificed_counts'][0], comment='Number of sacrificed transactions (node 0)')
    # traj.f_add_result('sacrificed_count_node_1', results['sacrificed_counts'][1], comment='Number of sacrificed transactions (node 1)')
    # traj.f_add_result('sacrificed_count_channel_total', results['sacrificed_counts'][2], comment='Number of sacrificed transactions (channel total)')
    # traj.f_add_result('sacrificed_amount_node_0', results['sacrificed_amounts'][0], comment='Amount of sacrificed transactions (node 0)')
    # traj.f_add_result('sacrificed_amount_node_1', results['sacrificed_amounts'][1], comment='Amount of sacrificed transactions (node 1)')
    # traj.f_add_result('sacrificed_amount_channel_total', results['sacrificed_amounts'][2], comment='Amount of sacrificed transactions (channel total)')
    # traj.f_add_result('success_rate_node_0', results['success_rates'][0], comment='Success rate (node 0)')
    # traj.f_add_result('success_rate_node_1', results['success_rates'][1], comment='Success rate (node 1)')
    traj.f_add_result('success_rate_channel_total', results['success_rates'][2], comment='Success rate (channel total)')
    # traj.f_add_result('normalized_throughput_node_0', results['normalized_throughputs'][0], comment='Normalized throughput (node 0)')
    # traj.f_add_result('normalized_throughput_node_1', results['normalized_throughputs'][1], comment='Normalized throughput (node 1)')
    traj.f_add_result('normalized_throughput_channel_total', results['normalized_throughputs'][2],
                      comment='Normalized throughput (channel total)')
    # traj.f_add_result('total_queueing_time_of_successful_transactions', results['total_queueing_times'][0], comment='Total queueing time of successful transactions')
    # traj.f_add_result('total_queueing_time_of_all_transactions', results['total_queueing_times'][1], comment='Total queueing time of all transactions')
    # traj.f_add_result('average_total_queueing_time_per_successful_unit_amount', results['total_queueing_times'][2], comment='Average queueing delay per successful unit amount')
    # traj.f_add_result('average_total_queueing_time_per_successful_transaction', results['total_queueing_times'][3], comment='Average queueing delay per transaction')

    # traj.f_add_result('all_transactions_list', all_transactions_list, 'All transactions')


def main():
    outputs_directory = str(Path("outputs").resolve())

    # Create the environment
    env = pypet.Environment(trajectory='single_payment_channel_scheduling',
                            filename=outputs_directory + '/HDF5/results_100.hdf5',
                            overwrite_file=True)
    traj = env.traj
    EMPIRICAL_DATA_FILEPATH = "../inputs/creditcard-non-fraudulent-only-amounts-only.csv"

    # SIMULATION PARAMETERS

    verbose = False
    num_of_experiments = 1

    # Node 0
    initial_balance_0 = 0
    total_transactions_0 = 500
    exp_mean_0 = 1 / 3
    amount_distribution_0 = "constant"
    amount_distribution_parameters_0 = [100]  # value of all transactions
    # amount_distribution_0 = "uniform"
    # amount_distribution_parameters_0 = [100]                # max_transaction_amount
    # amount_distribution_0 = "gaussian"
    # amount_distribution_parameters_0 = [300, 100, 50]       # max_transaction_amount, gaussian_mean, gaussian_variance. E.g.: [capacity, capacity / 2, capacity / 6]
    # amount_distribution_0 = "empirical_from_csv_file"
    # amount_distribution_parameters_0 = [EMPIRICAL_DATA_FILEPATH]
    # amount_distribution_0 = "pareto"
    # amount_distribution_parameters_0 = [1, 1.16, 1]         # lower, shape, size

    # deadline_distribution_0 = "constant"
    deadline_distribution_0 = "uniform"

    # Node 1
    initial_balance_1 = 300  # Capacity = 300
    total_transactions_1 = 500
    exp_mean_1 = 1 / 3
    amount_distribution_1 = "constant"
    amount_distribution_parameters_1 = [100]  # value of all transactions
    # amount_distribution_1 = "uniform"
    # amount_distribution_parameters_1 = [100]                # max_transaction_amount
    # amount_distribution_1 = "gaussian"
    # amount_distribution_parameters_1 = [300, 100, 50]       # max_transaction_amount, gaussian_mean, gaussian_variance. E.g.: [capacity, capacity / 2, capacity / 6]
    # amount_distribution_1 = "empirical_from_csv_file"
    # amount_distribution_parameters_1 = [EMPIRICAL_DATA_FILEPATH]
    # amount_distribution_1 = "pareto"
    # amount_distribution_parameters_1 = [1, 1.16, 1]                             # lower, shape, size

    # deadline_distribution_1 = "constant"
    deadline_distribution_1 = "uniform"

    # Process empirical dataset if requested

    capacity = initial_balance_0 + initial_balance_1
    if amount_distribution_0 == "empirical_from_csv_file" or amount_distribution_1 == "empirical_from_csv_file":
        EMPIRICAL_DATA_FILEPATH = amount_distribution_parameters_0[
            0] if amount_distribution_0 == "empirical_from_csv_file" else amount_distribution_parameters_1[0]
        # empirical_data = recfromcsv(EMPIRICAL_DATA_FILEPATH, dtype=float, delimiter=',')
        with open(EMPIRICAL_DATA_FILEPATH, newline='') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            empirical_data = list(reader)
            empirical_data = [ceil(x[0]) for x in empirical_data if
                              (0 < x[0] <= capacity)]  # Convert to float from list
        if amount_distribution_0 == "empirical_from_csv_file":
            amount_distribution_parameters_0 = empirical_data
        if amount_distribution_1 == "empirical_from_csv_file":
            amount_distribution_parameters_1 = empirical_data

    # Encode parameters for pypet

    traj.f_add_parameter('initial_balance_0', initial_balance_0, comment='Initial balance of node 0')
    traj.f_add_parameter('total_transactions_0', total_transactions_0, comment='Total transactions arriving at node 0')
    traj.f_add_parameter('exp_mean_0', exp_mean_0, comment='Rate of exponentially distributed arrivals at node 0')
    # traj.f_add_parameter('max_transaction_amount_0', traj.initial_balance_0 + traj.initial_balance_1,
    #                      comment='Maximum possible amount for incoming transactions at node 0')
    traj.f_add_parameter('amount_distribution_0', amount_distribution_0,
                         comment='The distribution of the transaction amounts at node 0')
    traj.f_add_parameter('amount_distribution_parameters_0', amount_distribution_parameters_0,
                         comment='Parameters of the distribution of the transaction amounts at node 0')
    traj.f_add_parameter('deadline_distribution_0', deadline_distribution_0,
                         comment='The distribution of the transaction deadlines at node 0')
    # traj.f_add_parameter('deadline_distribution_0_parameters', deadline_distribution_0_parameters, comment='Parameters of the distribution of the transaction deadlines at node 0')

    traj.f_add_parameter('initial_balance_1', initial_balance_1, comment='Initial balance of node 1')
    traj.f_add_parameter('total_transactions_1', total_transactions_1, comment='Total transactions arriving at node 1')
    traj.f_add_parameter('exp_mean_1', exp_mean_1, comment='Rate of exponentially distributed arrivals at node 1')
    # traj.f_add_parameter('max_transaction_amount_1', traj.initial_balance_0 + traj.initial_balance_1,
    #                      comment='Maximum possible amount for incoming transactions at node 1')
    traj.f_add_parameter('amount_distribution_1', amount_distribution_1,
                         comment='The distribution of the transaction amounts at node 1')
    traj.f_add_parameter('amount_distribution_parameters_1', amount_distribution_parameters_1,
                         comment='Parameters of the distribution of the transaction amounts at node 1')
    traj.f_add_parameter('deadline_distribution_1', deadline_distribution_1,
                         comment='The distribution of the transaction deadlines at node 1')
    # traj.f_add_parameter('deadline_distribution_1_parameters', deadline_distribution_1_parameters, comment='Parameters of the distribution of the transaction deadlines at node 1')

    traj.f_add_parameter('scheduling_policy', "PMDE", comment='Scheduling policy')
    traj.f_add_parameter('buffer_discipline', "oldest_first", comment='Order of processing transactions in the buffer')
    traj.f_add_parameter('buffering_capability', "neither_node", comment='Which node has a buffer')
    traj.f_add_parameter('max_buffering_time', 0, comment='Maximum time before a transaction expires')

    traj.f_add_parameter('capacity', capacity, comment='Channel capacity')
    traj.f_add_parameter('verbose', verbose, comment='Verbose output')
    traj.f_add_parameter('num_of_experiments', num_of_experiments, comment='Repetitions of every experiment')
    traj.f_add_parameter('seed', 0, comment='Randomness seed')
    traj.f_add_parameter('deadline_fraction', 1.0,
                         comment='Fraction of deadline at which PMDE will be applied (applicable to PMDE only)')

    seeds = [63621, 87563, 24240, 14020, 84331, 60917, 48692, 73114, 90695, 62302, 52578, 43760, 84941, 30804, 40434,
             63664, 25704, 38368, 45271, 34425]

    traj.f_explore(pypet.cartesian_product({
        'scheduling_policy': ["PMDE", "PRI-IP", "PRI-NIP", "PFI"],
        # 'scheduling_policy': ["PMDE"],
        # 'buffer_discipline': ["oldest_first", "youngest_first", "closest_deadline_first", "largest_amount_first", "smallest_amount_first"],
        'buffer_discipline': ["oldest_first"],
        # 'buffering_capability': ["neither_node", "only_node_0", "only_node_1", "both_separate", "both_shared"],
        # 'buffering_capability': ["neither_node"],
        'buffering_capability': ["both_shared"],
        # 'max_buffering_time': [60],
        # 'max_buffering_time': [10],
        # 'max_buffering_time': [5],
        'max_buffering_time': list(range(1, 10, 1)) + list(range(10, 120, 10)),
        'seed': seeds[1:traj.num_of_experiments + 1],
        # 'deadline_fraction': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    }))

    # Run wrapping function instead of simulator directly
    env.run(pypet_wrapper)


if __name__ == '__main__':
    main()
