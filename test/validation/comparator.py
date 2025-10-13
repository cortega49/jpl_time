"""
This script contains methods for each of the
comparison scripts.
"""

import __init__
import os
import time
from jpl_time import Time, Duration, create_jpl_time_object, output_jpl_time_in_format

def get_column_headers(external_script_name):
    """
    Takes in the name of the external script being run and returns the
    corrected column names.

    :param external_script_name:
    :return:
    """
    return [
        'input_time',
        'jpl_time_result',
        '{}_result'.format(external_script_name),
        'delta',
        'jpl_time_speed',
        '{}_speed'.format(external_script_name)
    ]


def read_file(filename):
    """Opens a file and returns the lines as an array. Also checks to make sure
    that the file exists and is not zero in size."""

    # check to make sure that the file exists
    if os.path.isfile(filename):
        # check that the pef file is non-zero in size
        if os.path.getsize(filename) > 0:
            contents = open(filename).readlines()

        # if the file is zero in size then give an error
        else:
            raise ValueError('{} file is zero in size.'.format(filename))

    # if the file does not exist then give an error
    else:
        raise ValueError('{} file does not exist.'.format(filename))

    # return an array of lines of the file
    return contents


def parse_external_results(external_results_path):
    external_results = []
    contents = read_file(external_results_path)
    for line in contents[1:]:
        split_line = line.split(',')
        if len(split_line) > 0:
            external_results.append(
                {
                    'input_time': split_line[0],
                    'result': split_line[1],
                    'speed': float(split_line[2])
                }
            )
    return external_results


def convert_jpl_time(input_time, input_type, output_type):
    """

    :param input_time: input time string, float, etc.
    :param input_type: 'scet', 'ett', 'ert', 'sclk', 'sclkd', 'lmst', 'et'
    :param output_type: 'scet', 'ett', 'ert', 'sclk', 'sclkd', 'lmst', 'et', 'ltst'
    :return: the specified output type, usually a string or float
    """
    start_time = time.time()
    time_object = create_jpl_time_object(input_time, input_type)
    output_object = output_jpl_time_in_format(time_object, output_type)

    return output_object, time.time() - start_time


def calculate_delta(time1, time2, time_type):
    """
    Takes in two times and computes a delta between them, depending on the type.

    :param time1:
    :type time1: str
    :param time2:
    :type time2: str
    :param time_type:
    :return:
    """
    if time_type == 'ltst':
        time_object1 = create_jpl_time_object(time1.replace('T', 'M'), 'lmst')
        time_object2 = create_jpl_time_object(time2.replace('T', 'M'), 'lmst')

    else:
        time_object1 = create_jpl_time_object(time1, time_type)
        time_object2 = create_jpl_time_object(time2, time_type)

    if time_type in ['scet', 'ert', 'ett', 'sclk']:
        return time_object2 - time_object1

    elif time_type in ['lmst', 'ltst']:
        return (time_object2 - time_object1).to_mars_dur()

    elif time_type in ['et', 'sclkd']:
        return float(time2) - float(time1)

    else:
        raise ValueError('Error in calculate_delta: input time type {} was not an allowed type.'.format(time_type))


def convert_test_dict_to_list(test_dict):
    """
    Converts a test dict, which is made up of lists for jpl_time and
    nsyt_time/m2020time, and merges them into a single list of dicts, which also
    includes a delta for the values calculated.

    :param test_dict: dict with lists for jpl_time and nsyt_time separately
    :type test_dict: dict
    :return: combined list with test results
    :rtype: list
    """
    merged_list = []

    for i in range(0, len(test_dict['jpl_time'])):
        jpl_time_result = test_dict['jpl_time'][i]['result']
        external_result = test_dict['external'][i]['result']

        temp_dict = {
            'input_time': test_dict['jpl_time'][i]['input_time'],
            'jpl_time_result': jpl_time_result,
            'external_result': external_result,
            'delta': None,  # to be populated by each test
            'jpl_time_speed': test_dict['jpl_time'][i]['speed'],
            'external_speed': test_dict['external'][i]['speed'],
        }
        merged_list.append(temp_dict)

    return merged_list


def write_test_csv(single_test_results, filename, external_script_name):
    """
    Writes out a single test csv file given a test dict.

    :param test_results:
    :type test_results: list
    :param filename: name of output csv file
    :type filename: str
    :rtype: None
    """
    output_string = ','.join(get_column_headers(external_script_name))
    for dict in single_test_results:
        output_string += '\n' + ','.join([
            str(dict['input_time']),
            str(dict['jpl_time_result']),
            str(dict['external_result']),
            str(dict['delta']),
            str(dict['jpl_time_speed']),
            str(dict['external_speed'])
        ])

    full_output_filename = os.path.join(os.path.dirname(__file__), filename)

    with open(full_output_filename, 'w') as f:
        f.write(output_string)


def calculate_runtimes(result_dict):
    total_jpl_time_runtime = 0.0
    total_external_runtime = 0.0
    for result in result_dict['results']:
        total_jpl_time_runtime += float(result['jpl_time_speed'])
        total_external_runtime += float(result['external_speed'])

    average_jpl_time_runtime = total_jpl_time_runtime / len(result_dict['results'])
    average_external_runtime = total_external_runtime / len(result_dict['results'])

    ratio = total_external_runtime / total_jpl_time_runtime

    return total_jpl_time_runtime, total_external_runtime, average_jpl_time_runtime, average_external_runtime, ratio


def calculate_average_absolute_delta(result_dict):
    time_type = result_dict['output_type']

    if time_type in ['scet', 'ert', 'ett', 'sclk']:
        total_abs_delta = Duration(0)
        for result in result_dict['results']:
            total_abs_delta += Duration(result['delta']).abs()

        return (total_abs_delta / len(result_dict['results'])).to_string(6)

    elif time_type in ['lmst', 'ltst']:
        total_abs_delta = Duration(0)
        for result in result_dict['results']:
            total_abs_delta += Duration(result['delta']).abs()

        return (total_abs_delta / len(result_dict['results'])).to_mars_dur(6)

    elif time_type in ['et', 'sclkd']:
        total_abs_delta = 0.0
        for result in result_dict['results']:
            total_abs_delta += abs(float(result['delta']))

        return str(total_abs_delta / len(result_dict['results']))

    else:
        raise ValueError(
            'Error in calculate_average_absolute_delta: input time type {} was not an allowed type.'.format(time_type))


def summarize_test_results(all_test_results):
    """
    Takes in a dict of all of the test_results lists and summarizes
    the results.

    :param all_test_results: dict of all test_results lists
    :type all_test_results: dict
    :return: dict with summary of test results
    :rtype: dict
    """
    summary_dict = {}
    for test_name in all_test_results:
        total_jpl_time_runtime, \
        total_external_runtime, \
        average_jpl_time_runtime, \
        average_external_runtime, \
        ratio = calculate_runtimes(all_test_results[test_name])
        avg_abs_delta = calculate_average_absolute_delta(all_test_results[test_name])
        test = all_test_results[test_name]['input_type'] + ' to ' + all_test_results[test_name]['output_type']

        summary_dict[test] = {
            'total_jpl_time_runtime': total_jpl_time_runtime,
            'total_external_runtime': total_external_runtime,
            'average_jpl_time_runtime': average_jpl_time_runtime,
            'average_external_runtime': average_external_runtime,
            'avg_abs_delta': avg_abs_delta,
            'ratio': ratio
        }

    return summary_dict


def write_test_summary(summary_dict, external_script_name):
    output_lines = ['Comparison of jpl_time and {} conversions']

    test_number = 1

    for test_name in sorted(summary_dict):
        output_lines.append('Test {}: {}'.format(test_number, test_name))

        output_lines.append('Total jpl_time runtime: {} seconds'.format(
            summary_dict[test_name]['total_jpl_time_runtime']
        ))
        output_lines.append('Total {} runtime: {} seconds'.format(
            external_script_name,
            summary_dict[test_name]['total_external_runtime']
        ))
        output_lines.append('Average jpl_time runtime: {} seconds'.format(
            summary_dict[test_name]['average_jpl_time_runtime']
        ))
        output_lines.append('Average {} runtime: {} seconds'.format(
            external_script_name,
            summary_dict[test_name]['average_external_runtime']
        ))
        output_lines.append('Runtime ratio: {}'.format(
            summary_dict[test_name]['ratio']
        ))
        output_lines.append('Average absolute delta: {}'.format(
            summary_dict[test_name]['avg_abs_delta']
        ))
        output_lines.append('')
        test_number += 1

    return output_lines


def run_comparison(input_times, external_results, input_type, output_type):
    test_results = []

    for index, input_time in enumerate(input_times):
        temp_dict = {'input_time': str(input_time)}

        # jpl_time calculation
        jpl_time_result, jpl_time_speed = convert_jpl_time(input_time, input_type, output_type)
        temp_dict['jpl_time_result'] = jpl_time_result
        temp_dict['jpl_time_speed'] = jpl_time_speed

        # external data
        external_result = external_results[index]['result']
        temp_dict['external_result'] = external_result
        temp_dict['external_speed'] = str(external_results[index]['speed'])

        temp_dict['delta'] = calculate_delta(jpl_time_result, external_result, output_type)

        test_results.append(temp_dict)

    return test_results