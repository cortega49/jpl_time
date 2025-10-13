"""
This script generates the input times files for the
m2020time and nsyt_time comparisons. The logic is
different for each because nsyt_time is much, much
slower than m2020time due to the lack of a batch mode.
"""

import os
from jpl_time import Time, Duration

NSYT_TIME_KERNELS = [
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/de430s.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight.tls'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight.tsc'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight_atls_ops181206_v1.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight_lmst_ops181206_v1.tsc'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight_ls_ops181206_iau2000_v1.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight_nom_2016e09o_cruise_v1.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight_nom_2016e09o_edl_v1.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight_surf_ops_v1.bc'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight_tp_ops181206_iau2000_v1.tf'),
    os.path.join(os.path.dirname(__file__), '../inputs/nsyt_kernels_07112019/insight_v05.tf'),
    os.path.join(os.path.dirname(__file__), '../inputs/common_kernels/mar097.bsp'),
    os.path.join(os.path.dirname(__file__), '../inputs/common_kernels/pck00010.tpc'),
]

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

TAB = '    '

# the UTC times will be used for SCET, ERT, ETT, PST, SCLK, SCLKD and OWLT tests
NSYT_UTC_START = '2019-001T00:00:00'
NSYT_UTC_END = '2023-001T00:00:00'
NSYT_UTC_DUR = '12:34:56.789123'

M2020_UTC_START = '2022-001T00:00:00'
M2020_UTC_END = '2042-001T00:00:00'
M2020_UTC_DUR = '1M12:34:56.789123'

LMST_START = 'Sol-0001M00:00:00'
LMST_END = 'Sol-2500M00:00:00'
NSYT_LMST_DUR = '10M23:45:12.345'
M2020_LMST_DUR = '10M12:34:56.789'

ET_START = 8640000.0
ET_END = ET_START + 60 * 60 * 24 * 365 * 30 # ~30 years
NSYT_ET_DUR = 60 * 60 * 24 * 100 # 100 days
M2020_ET_DUR = 60 * 60 * 24 * 100 # 100 days

def configure_spice_nsyt():
    Time.load_kernels(NSYT_TIME_KERNELS)
    Time.set_spacecraft_id(-189)
    Time.set_lmst_sclk_id(-189900)
    Time.set_output_decimal_precision(6)
    Duration.set_output_decimal_precision(6)


def configure_spice_m2020():
    Time.load_kernels(M2020TIME_KERNELS)
    Time.set_spacecraft_id(-168)
    Time.set_lmst_sclk_id(-168900)
    Time.set_output_decimal_precision(6)
    Duration.set_output_decimal_precision(6)


def create_time_list(start, end, dur):
    time_list = []
    current_time = start
    while current_time <= end:
        time_list.append(current_time)
        current_time = current_time + dur

    return time_list


def create_time_lists(UTC_START, UTC_END, UTC_DUR, LMST_START, LMST_END, LMST_DUR, ET_START, ET_END, ET_DUR):
    et_times = create_time_list(ET_START, ET_END, ET_DUR)
    utc_list_1 = create_time_list(Time(UTC_START) + Duration('12:00:00'), Time(UTC_END) + Duration('12:00:00'),
                                   Duration(UTC_DUR))
    utc_list_2 = create_time_list(Time(UTC_START) + Duration('1T00:00:00'), Time(UTC_END) + Duration('1T00:00:00'),
                                   Duration(UTC_DUR))
    lmst_list = create_time_list(Time(LMST_START), Time(LMST_END), Duration(LMST_DUR))
    lmst_times = [t.to_lmst() for t in lmst_list]
    ltst_times = [t.replace('Sol-', 'SOL ').replace('M', ' ') for t in lmst_times]

    # utc list 1 will be for SCET_TIMES and SCLK_TIMES
    utc_times = [str(t) for t in utc_list_1]
    sclk_times = []
    for utc in utc_list_1:
        sclk_times.append(utc.to_sclk())

    # utc list 2 will be for SCLKD_TIMES
    sclkd_times = []
    for utc in utc_list_2:
        sclkd_times.append(utc.to_sclkd())

    # output lists for each set of times
    # these will end up being Python globals
    output_string = 'SCET_TIMES = [\n'
    for utc in utc_times:
        output_string += "{}'{}',\n".format(TAB, utc)
    output_string += ']\n\n'

    output_string += 'SCLK_TIMES = [\n'
    for sclk in sclk_times:
        output_string += "{}'{}',\n".format(TAB, sclk)
    output_string += ']\n\n'

    output_string += 'SCLKD_TIMES = [\n'
    for sclkd in sclkd_times:
        output_string += "{}{},\n".format(TAB, repr(sclkd))
    output_string += ']\n\n'

    output_string += 'ET_TIMES = [\n'
    for et in et_times:
        output_string += "{}{},\n".format(TAB, repr(et))
    output_string += ']\n\n'

    output_string += 'LMST_TIMES = [\n'
    for lmst in lmst_times:
        output_string += "{}'{}',\n".format(TAB, lmst)
    output_string += ']\n\n'

    output_string += 'LTST_TIMES = [\n'
    for ltst in ltst_times:
        output_string += "{}'{}',\n".format(TAB, ltst)
    output_string += ']\n\n'

    return output_string


def generate_nsyt_time_inputs():
    configure_spice_nsyt()
    nsyt_lmst_start = (Time(LMST_START) + Duration(NSYT_LMST_DUR)).to_lmst()
    output_string = create_time_lists(NSYT_UTC_START, NSYT_UTC_END, NSYT_UTC_DUR,
                                      nsyt_lmst_start, LMST_END, NSYT_LMST_DUR,
                                      ET_START, ET_END, NSYT_ET_DUR)

    with open('nsyt_time_comparison_inputs/input_times.py', 'w') as f:
        f.write(output_string)


def generate_m2020time_inputs():
    configure_spice_m2020()
    m2020_lmst_start = (Time(LMST_START) + Duration(M2020_LMST_DUR)).to_lmst()
    output_string = create_time_lists(M2020_UTC_START, M2020_UTC_END, M2020_UTC_DUR,
                                      m2020_lmst_start, LMST_END, M2020_LMST_DUR,
                                      ET_START, ET_END, M2020_ET_DUR)

    with open('m2020time_comparison_inputs/input_times.py', 'w') as f:
        f.write(output_string)


def main():
    generate_nsyt_time_inputs()
    generate_m2020time_inputs()


# Call to Main #
if __name__ == '__main__': main()