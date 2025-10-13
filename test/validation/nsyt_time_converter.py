"""
This script runs nsyt_time on the insight machines
for each of the input times.
"""

import sys
import time
import multiprocessing
from nsyt_time_comparison_inputs.input_times import SCET_TIMES, LMST_TIMES, LTST_TIMES, SCLK_TIMES, SCLKD_TIMES, ET_TIMES

sys.path.insert(0, '/gds/nsy/bin/')
try:
    import nsyt_time
except ImportError:
    raise ImportError('Could not import nsyt_time. Needed for sclk-scet converstions.')

try:
    TIME_CONVERTER = nsyt_time.TimeConverter(nsyt_time.ALIASES_FILE)
except NameError:
    pass


def run_nsyt_time_individual(input_time, input_time_type, return_time_type):
    """
    Runs nsyt_time using subprocess to do a single time conversion.

    :param input_time: input time
    :param input_time_type: the type of the input time as a lowercase string
    :param return_time_type: the type of the output you want as a lowercase string
    :return:
    :rtype: str
    """
    if isinstance(input_time, float):
        input_time_string = repr(input_time)
    else:
        input_time_string = str(input_time)

    if return_time_type != 'et' and input_time_type != 'et':
        return TIME_CONVERTER.run_alias('{}2{}'.format(input_time_type, return_time_type), input_time_string)
    else:
        time_conversion_dict = nsyt_time.TimeDict(input_time_string, input_time_type,TIME_CONVERTER)

        return time_conversion_dict[return_time_type]


def run_nsyt_time_test(input_time_list, input_type, output_type):
    nsyt_time_results = []
    for input_time in input_time_list:
        start_time = time.time()
        temp_dict = {
            'input_time': input_time,
            'nsyt_time_result': run_nsyt_time_individual(input_time, input_type, output_type)
        }
        temp_dict['nsyt_time_speed'] = time.time() - start_time
        nsyt_time_results.append(temp_dict)

    output_string = 'input_time,nsyt_time_result,nsyt_time_speed\n'
    for dict in nsyt_time_results:
        output_string += str(dict['input_time']) + ',' + str(dict['nsyt_time_result']) + ',' + str(dict['nsyt_time_speed']) + '\n'

    with open('nsyt_time_{}_to_{}_results.csv'.format(input_type, output_type), 'w') as f:
        f.write(output_string)


def run_parallel_tests():
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.apply_async(run_nsyt_time_test, args=(SCET_TIMES, 'scet', 'lmst'))
    pool.apply_async(run_nsyt_time_test, args=(SCET_TIMES, 'scet', 'ltst'))
    pool.apply_async(run_nsyt_time_test, args=(SCET_TIMES, 'scet', 'et'))
    pool.apply_async(run_nsyt_time_test, args=(SCET_TIMES, 'scet', 'sclk'))
    pool.apply_async(run_nsyt_time_test, args=(SCET_TIMES, 'scet', 'sclkd'))
    pool.apply_async(run_nsyt_time_test, args=(LMST_TIMES, 'lmst', 'scet'))
    pool.apply_async(run_nsyt_time_test, args=(LMST_TIMES, 'lmst', 'ltst'))
    pool.apply_async(run_nsyt_time_test, args=(LMST_TIMES, 'lmst', 'et'))
    pool.apply_async(run_nsyt_time_test, args=(LMST_TIMES, 'lmst', 'sclk'))
    pool.apply_async(run_nsyt_time_test, args=(LMST_TIMES, 'lmst', 'sclkd'))
    pool.apply_async(run_nsyt_time_test, args=(LTST_TIMES, 'ltst', 'scet'))
    pool.apply_async(run_nsyt_time_test, args=(LTST_TIMES, 'ltst', 'lmst'))
    pool.apply_async(run_nsyt_time_test, args=(LTST_TIMES, 'ltst', 'et'))
    pool.apply_async(run_nsyt_time_test, args=(LTST_TIMES, 'ltst', 'sclk'))
    pool.apply_async(run_nsyt_time_test, args=(LTST_TIMES, 'ltst', 'sclkd'))
    pool.apply_async(run_nsyt_time_test, args=(SCLK_TIMES, 'sclk', 'scet'))
    pool.apply_async(run_nsyt_time_test, args=(SCLK_TIMES, 'sclk', 'sclkd'))
    pool.apply_async(run_nsyt_time_test, args=(SCLK_TIMES, 'sclk', 'et'))
    pool.apply_async(run_nsyt_time_test, args=(SCLK_TIMES, 'sclk', 'lmst'))
    pool.apply_async(run_nsyt_time_test, args=(SCLK_TIMES, 'sclk', 'ltst'))
    pool.apply_async(run_nsyt_time_test, args=(SCLKD_TIMES, 'sclkd', 'scet'))
    pool.apply_async(run_nsyt_time_test, args=(SCLKD_TIMES, 'sclkd', 'sclk'))
    pool.apply_async(run_nsyt_time_test, args=(SCLKD_TIMES, 'sclkd', 'et'))
    pool.apply_async(run_nsyt_time_test, args=(SCLKD_TIMES, 'sclkd', 'lmst'))
    pool.apply_async(run_nsyt_time_test, args=(SCLKD_TIMES, 'sclkd', 'ltst'))
    pool.apply_async(run_nsyt_time_test, args=(ET_TIMES, 'et', 'scet'))
    pool.apply_async(run_nsyt_time_test, args=(ET_TIMES, 'et', 'sclk'))
    pool.apply_async(run_nsyt_time_test, args=(ET_TIMES, 'et', 'sclkd'))

    # closing the pool will stop any further processes from being added to the pool
    # join will block the calling thread (this script) until all processes have completed
    pool.close()
    pool.join()


def main():
    run_parallel_tests()


# Call to Main #
if __name__ == '__main__': main()
