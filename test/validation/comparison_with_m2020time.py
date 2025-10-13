"""
This script is used to compare the results of conversions done by
jpl_time with those from m2020time when the same kernels are loaded.
"""

import __init__
import os
from jpl_time import Time, Duration
from m2020time_comparison_inputs.input_times import SCET_TIMES, LMST_TIMES, LTST_TIMES, SCLKD_TIMES, SCLK_TIMES, ET_TIMES
from comparator import run_comparison, parse_external_results, write_test_csv, write_test_summary, summarize_test_results

M2020TIME_KERNELS = [
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/m2020.tls'),
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/m2020.tsc'),
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/m2020.tf'),
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/m2020_lmst_jez_v3.tsc'),
    os.path.join(os.path.dirname(__file__), '../inputs/common_kernels/pck00010.tpc'),
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/de438s.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/common_kernels/mar097.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/m2020_FMAresponse_JEZ_20200717_P000.cruise.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/m2020_FMAresponse_JEZ_20200717_P000.edl.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/m2020_ls_jez_iau2000_v3.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/m2020_atls_jez_v3.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/m2020_kernels_jez_v3/m2020_tp_jez_iau2000_v3.tf')
]

def configure_spice():
    Time.load_kernels(M2020TIME_KERNELS)
    Time.set_spacecraft_id(-168)
    Time.set_lmst_sclk_id(-168900)
    Time.set_output_decimal_precision(6)
    Duration.set_output_decimal_precision(6)


def main():
    configure_spice()

    test_results = {
        'scet_to_lmst':     {'results': run_comparison(SCET_TIMES, parse_external_results('m2020time_outputs/m2020time_scet_to_lmst_results.csv'), 'scet', 'lmst'),    'input_type': 'scet',   'output_type': 'lmst'},
        'scet_to_ltst':     {'results': run_comparison(SCET_TIMES, parse_external_results('m2020time_outputs/m2020time_scet_to_ltst_results.csv'), 'scet', 'ltst'),    'input_type': 'scet',   'output_type': 'ltst'},
        'scet_to_et':       {'results': run_comparison(SCET_TIMES, parse_external_results('m2020time_outputs/m2020time_scet_to_et_results.csv'), 'scet', 'et'),        'input_type': 'scet',   'output_type': 'et'},
        'scet_to_sclk':     {'results': run_comparison(SCET_TIMES, parse_external_results('m2020time_outputs/m2020time_scet_to_sclk_results.csv'), 'scet', 'sclk'),    'input_type': 'scet',   'output_type': 'sclk'},
        'scet_to_sclkd':    {'results': run_comparison(SCET_TIMES, parse_external_results('m2020time_outputs/m2020time_scet_to_sclkd_results.csv'), 'scet', 'sclkd'),  'input_type': 'scet',   'output_type': 'sclkd'},
        'lmst_to_scet':     {'results': run_comparison(LMST_TIMES, parse_external_results('m2020time_outputs/m2020time_lmst_to_scet_results.csv'), 'lmst', 'scet'),    'input_type': 'lmst',   'output_type': 'scet'},
        'lmst_to_ltst':     {'results': run_comparison(LMST_TIMES, parse_external_results('m2020time_outputs/m2020time_lmst_to_ltst_results.csv'), 'lmst', 'ltst'),    'input_type': 'lmst',   'output_type': 'ltst'},
        'lmst_to_et':       {'results': run_comparison(LMST_TIMES, parse_external_results('m2020time_outputs/m2020time_lmst_to_et_results.csv'), 'lmst', 'et'),        'input_type': 'lmst',   'output_type': 'et'},
        'lmst_to_sclk':     {'results': run_comparison(LMST_TIMES, parse_external_results('m2020time_outputs/m2020time_lmst_to_sclk_results.csv'), 'lmst', 'sclk'),    'input_type': 'lmst',   'output_type': 'sclk'},
        'lmst_to_sclkd':    {'results': run_comparison(LMST_TIMES, parse_external_results('m2020time_outputs/m2020time_lmst_to_sclkd_results.csv'), 'lmst', 'sclkd'),  'input_type': 'lmst',   'output_type': 'sclkd'},
        'ltst_to_scet':     {'results': run_comparison(LTST_TIMES, parse_external_results('m2020time_outputs/m2020time_ltst_to_scet_results.csv'), 'ltst', 'scet'),    'input_type': 'ltst',   'output_type': 'scet'},
        'ltst_to_lmst':     {'results': run_comparison(LTST_TIMES, parse_external_results('m2020time_outputs/m2020time_ltst_to_lmst_results.csv'), 'ltst', 'lmst'),    'input_type': 'ltst',   'output_type': 'lmst'},
        'ltst_to_et':       {'results': run_comparison(LTST_TIMES, parse_external_results('m2020time_outputs/m2020time_ltst_to_et_results.csv'), 'ltst', 'et'),        'input_type': 'ltst',   'output_type': 'et'},
        'ltst_to_sclk':     {'results': run_comparison(LTST_TIMES, parse_external_results('m2020time_outputs/m2020time_ltst_to_sclk_results.csv'), 'ltst', 'sclk'),    'input_type': 'ltst',   'output_type': 'sclk'},
        'ltst_to_sclkd':    {'results': run_comparison(LTST_TIMES, parse_external_results('m2020time_outputs/m2020time_ltst_to_sclkd_results.csv'), 'ltst', 'sclkd'),  'input_type': 'ltst',   'output_type': 'sclkd'},
        'sclk_to_scet':     {'results': run_comparison(SCLK_TIMES, parse_external_results('m2020time_outputs/m2020time_sclk_to_scet_results.csv'), 'sclk', 'scet'),    'input_type': 'sclk',   'output_type': 'scet'},
        'sclk_to_sclkd':    {'results': run_comparison(SCLK_TIMES, parse_external_results('m2020time_outputs/m2020time_sclk_to_sclkd_results.csv'), 'sclk', 'sclkd'),  'input_type': 'sclk',   'output_type': 'sclkd'},
        'sclk_to_et':       {'results': run_comparison(SCLK_TIMES, parse_external_results('m2020time_outputs/m2020time_sclk_to_et_results.csv'), 'sclk', 'et'),        'input_type': 'sclk',   'output_type': 'et'},
        'sclk_to_lmst':     {'results': run_comparison(SCLK_TIMES, parse_external_results('m2020time_outputs/m2020time_sclk_to_lmst_results.csv'), 'sclk', 'lmst'),    'input_type': 'sclk',   'output_type': 'lmst'},
        'sclk_to_ltst':     {'results': run_comparison(SCLK_TIMES, parse_external_results('m2020time_outputs/m2020time_sclk_to_ltst_results.csv'), 'sclk', 'ltst'),    'input_type': 'sclk',   'output_type': 'ltst'},
        'sclkd_to_scet':    {'results': run_comparison(SCLKD_TIMES, parse_external_results('m2020time_outputs/m2020time_sclkd_to_scet_results.csv'), 'sclkd', 'scet'), 'input_type': 'sclkd',  'output_type': 'scet'},
        'sclkd_to_sclk':    {'results': run_comparison(SCLKD_TIMES, parse_external_results('m2020time_outputs/m2020time_sclkd_to_sclk_results.csv'), 'sclkd', 'sclk'), 'input_type': 'sclkd',  'output_type': 'sclk'},
        'sclkd_to_et':      {'results': run_comparison(SCLKD_TIMES, parse_external_results('m2020time_outputs/m2020time_sclkd_to_et_results.csv'), 'sclkd', 'et'),     'input_type': 'sclkd',  'output_type': 'et'},
        'sclkd_to_lmst':    {'results': run_comparison(SCLKD_TIMES, parse_external_results('m2020time_outputs/m2020time_sclkd_to_lmst_results.csv'), 'sclkd', 'lmst'), 'input_type': 'sclkd',  'output_type': 'lmst'},
        'sclkd_to_ltst':    {'results': run_comparison(SCLKD_TIMES, parse_external_results('m2020time_outputs/m2020time_sclkd_to_ltst_results.csv'), 'sclkd', 'ltst'), 'input_type': 'sclkd',  'output_type': 'ltst'},
        'et_to_scet':       {'results': run_comparison(ET_TIMES, parse_external_results('m2020time_outputs/m2020time_et_to_scet_results.csv'), 'et', 'scet'),          'input_type': 'et',     'output_type': 'scet'},
        'et_to_sclk':       {'results': run_comparison(ET_TIMES, parse_external_results('m2020time_outputs/m2020time_et_to_sclk_results.csv'), 'et', 'sclk'),          'input_type': 'et',     'output_type': 'sclk'},
        'et_to_sclkd':      {'results': run_comparison(ET_TIMES, parse_external_results('m2020time_outputs/m2020time_et_to_sclkd_results.csv'), 'et', 'sclkd'),        'input_type': 'et',     'output_type': 'sclkd'}
    }

    write_test_csv(test_results['scet_to_lmst']['results'], 'm2020time_comparison_outputs/scet_to_lmst.csv', 'm2020time')
    write_test_csv(test_results['scet_to_ltst']['results'], 'm2020time_comparison_outputs/scet_to_ltst.csv', 'm2020time')
    write_test_csv(test_results['scet_to_et']['results'], 'm2020time_comparison_outputs/scet_to_et.csv', 'm2020time')
    write_test_csv(test_results['scet_to_sclk']['results'], 'm2020time_comparison_outputs/scet_to_sclk.csv', 'm2020time')
    write_test_csv(test_results['scet_to_sclkd']['results'], 'm2020time_comparison_outputs/scet_to_sclkd.csv', 'm2020time')
    write_test_csv(test_results['lmst_to_scet']['results'], 'm2020time_comparison_outputs/lmst_to_scet.csv', 'm2020time')
    write_test_csv(test_results['lmst_to_ltst']['results'], 'm2020time_comparison_outputs/lmst_to_ltst.csv', 'm2020time')
    write_test_csv(test_results['lmst_to_et']['results'], 'm2020time_comparison_outputs/lmst_to_et.csv', 'm2020time')
    write_test_csv(test_results['lmst_to_sclk']['results'], 'm2020time_comparison_outputs/lmst_to_sclk.csv', 'm2020time')
    write_test_csv(test_results['lmst_to_sclkd']['results'], 'm2020time_comparison_outputs/lmst_to_sclkd.csv', 'm2020time')
    write_test_csv(test_results['ltst_to_scet']['results'], 'm2020time_comparison_outputs/ltst_to_scet.csv','m2020time')
    write_test_csv(test_results['ltst_to_lmst']['results'], 'm2020time_comparison_outputs/ltst_to_lmst.csv','m2020time')
    write_test_csv(test_results['ltst_to_et']['results'], 'm2020time_comparison_outputs/ltst_to_et.csv', 'm2020time')
    write_test_csv(test_results['ltst_to_sclk']['results'], 'm2020time_comparison_outputs/ltst_to_sclk.csv','m2020time')
    write_test_csv(test_results['ltst_to_sclkd']['results'], 'm2020time_comparison_outputs/ltst_to_sclkd.csv','m2020time')
    write_test_csv(test_results['sclk_to_scet']['results'], 'm2020time_comparison_outputs/sclk_to_scet.csv', 'm2020time')
    write_test_csv(test_results['sclk_to_sclkd']['results'], 'm2020time_comparison_outputs/sclk_to_sclkd.csv', 'm2020time')
    write_test_csv(test_results['sclk_to_et']['results'], 'm2020time_comparison_outputs/sclk_to_et.csv', 'm2020time')
    write_test_csv(test_results['sclk_to_lmst']['results'], 'm2020time_comparison_outputs/sclk_to_lmst.csv', 'm2020time')
    write_test_csv(test_results['sclk_to_ltst']['results'], 'm2020time_comparison_outputs/sclk_to_ltst.csv', 'm2020time')
    write_test_csv(test_results['sclkd_to_scet']['results'], 'm2020time_comparison_outputs/sclkd_to_scet.csv', 'm2020time')
    write_test_csv(test_results['sclkd_to_sclk']['results'], 'm2020time_comparison_outputs/sclkd_to_sclk.csv', 'm2020time')
    write_test_csv(test_results['sclkd_to_et']['results'], 'm2020time_comparison_outputs/sclkd_to_et.csv', 'm2020time')
    write_test_csv(test_results['sclkd_to_lmst']['results'], 'm2020time_comparison_outputs/sclkd_to_lmst.csv', 'm2020time')
    write_test_csv(test_results['sclkd_to_ltst']['results'], 'm2020time_comparison_outputs/sclkd_to_ltst.csv', 'm2020time')
    write_test_csv(test_results['et_to_scet']['results'], 'm2020time_comparison_outputs/et_to_scet.csv', 'm2020time')
    write_test_csv(test_results['et_to_sclk']['results'], 'm2020time_comparison_outputs/et_to_sclk.csv', 'm2020time')
    write_test_csv(test_results['et_to_sclkd']['results'], 'm2020time_comparison_outputs/et_to_sclkd.csv', 'm2020time')

    summary_dict = summarize_test_results(test_results)
    output_lines = write_test_summary(summary_dict, 'm2020time')

    with open('m2020time_comparison_outputs/jpl_time_vs_m2020time_summary.txt', 'w') as f:
        f.write('\n'.join(output_lines))


# Call to Main #
if __name__ == '__main__': main()
