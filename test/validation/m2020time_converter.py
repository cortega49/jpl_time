"""
This script runs m2020time on the m2020 machines
for each of the input times.
"""

import __init__
import os
import time
import multiprocessing
from m2020time_comparison_inputs.input_times import SCET_TIMES, LMST_TIMES, LTST_TIMES, SCLK_TIMES, SCLKD_TIMES, ET_TIMES

try:
    import m2020time
except ImportError:
    raise ImportError('Could not import m2020time. Needed for sclk-scet converstions.')

CHRONOS_CONFIG_FILE = '/ods/cedl/strategic/naif/misc/chronos/chronos.m2020_jez_v3'
CHRONOS_LMST_CONFIG_FILE = '/ods/cedl/strategic/naif/misc/chronos/chronos_lmst.m2020_jez_v3'


def run_m2020time_batch(input_times, input_time_type, return_time_type):
    """
    Runs m2020time using the imported methods to do a batch time conversions.

    :param input_times: input time list
    :type input_times: list
    :param input_time_type: the type of the input time as a lowercase string
    :param return_time_type: the type of the output you want as a lowercase string
    :return:
    :rtype: str
    """
    # if the list has floats then we need to convert each to a string
    updated_times = []
    if isinstance(input_times[0], float):
        for input_time in input_times:
            updated_times.append(repr(input_time))
    else:
        updated_times = input_times

    start = time.time()
    results = m2020time.convert(updated_times, input_time_type.lower(), return_time_type.upper(),
                                config_file=CHRONOS_CONFIG_FILE,
                                lmst_config_file=CHRONOS_LMST_CONFIG_FILE)
    total_runtime = time.time() - start

    return results, total_runtime


def run_m2020_test(input_time_list, input_type, output_type):
    m2020time_results, total_runtime = run_m2020time_batch(input_time_list, input_type, output_type)

    output_string = 'input_time,m2020time_result,m2020time_speed\n'
    for index, result in enumerate(m2020time_results):
        if isinstance(input_time_list[index], float):
            input_time = repr(input_time_list[index])
        else:
            input_time = str(input_time_list[index])

        if isinstance(result, float):
            result_string = repr(result)

        else:
            result_string = str(result)

        # use the average runtime for each
        output_string += input_time + ',' + result_string + ',' + str(
            total_runtime/len(m2020time_results)) + '\n'

    with open('m2020time_{}_to_{}_results.csv'.format(input_type, output_type), 'w') as f:
        f.write(output_string)


def run_parallel_tests():
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.apply_async(run_m2020_test, args=(SCET_TIMES, 'scet', 'lmst'))
    pool.apply_async(run_m2020_test, args=(SCET_TIMES, 'scet', 'ltst'))
    pool.apply_async(run_m2020_test, args=(SCET_TIMES, 'scet', 'et'))
    pool.apply_async(run_m2020_test, args=(SCET_TIMES, 'scet', 'sclk'))
    pool.apply_async(run_m2020_test, args=(SCET_TIMES, 'scet', 'sclkd'))
    pool.apply_async(run_m2020_test, args=(LMST_TIMES, 'lmst', 'scet'))
    pool.apply_async(run_m2020_test, args=(LMST_TIMES, 'lmst', 'ltst'))
    pool.apply_async(run_m2020_test, args=(LMST_TIMES, 'lmst', 'et'))
    pool.apply_async(run_m2020_test, args=(LMST_TIMES, 'lmst', 'sclk'))
    pool.apply_async(run_m2020_test, args=(LMST_TIMES, 'lmst', 'sclkd'))
    pool.apply_async(run_m2020_test, args=(LTST_TIMES, 'ltst', 'scet'))
    pool.apply_async(run_m2020_test, args=(LTST_TIMES, 'ltst', 'lmst'))
    pool.apply_async(run_m2020_test, args=(LTST_TIMES, 'ltst', 'et'))
    pool.apply_async(run_m2020_test, args=(LTST_TIMES, 'ltst', 'sclk'))
    pool.apply_async(run_m2020_test, args=(LTST_TIMES, 'ltst', 'sclkd'))
    pool.apply_async(run_m2020_test, args=(SCLK_TIMES, 'sclk', 'scet'))
    pool.apply_async(run_m2020_test, args=(SCLK_TIMES, 'sclk', 'sclkd'))
    pool.apply_async(run_m2020_test, args=(SCLK_TIMES, 'sclk', 'et'))
    pool.apply_async(run_m2020_test, args=(SCLK_TIMES, 'sclk', 'lmst'))
    pool.apply_async(run_m2020_test, args=(SCLK_TIMES, 'sclk', 'ltst'))
    pool.apply_async(run_m2020_test, args=(SCLKD_TIMES, 'sclkd', 'scet'))
    pool.apply_async(run_m2020_test, args=(SCLKD_TIMES, 'sclkd', 'sclk'))
    pool.apply_async(run_m2020_test, args=(SCLKD_TIMES, 'sclkd', 'et'))
    pool.apply_async(run_m2020_test, args=(SCLKD_TIMES, 'sclkd', 'lmst'))
    pool.apply_async(run_m2020_test, args=(SCLKD_TIMES, 'sclkd', 'ltst'))
    pool.apply_async(run_m2020_test, args=(ET_TIMES, 'et', 'scet'))
    pool.apply_async(run_m2020_test, args=(ET_TIMES, 'et', 'sclk'))
    pool.apply_async(run_m2020_test, args=(ET_TIMES, 'et', 'sclkd'))

    # closing the pool will stop any further processes from being added to the pool
    # join will block the calling thread (this script) until all processes have completed
    pool.close()
    pool.join()


def main():
    run_parallel_tests()


# Call to Main #
if __name__ == '__main__': main()