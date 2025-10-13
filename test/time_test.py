"""
Unit tests for Time class.
"""

import os
from datetime import datetime, date

from jpl_time import Time, Duration, load_chronos_config, GPST_EPOCH, EpochRelativeTime, convert_to_all_formats
import spiceypy as spice

__program__ = 'time_test.py'
__author__  = 'Forrest Ridenhour'
__project__ = 'Mars2020'
__version__ = '1.0'
__dependencies__ = 'jpl_time.py, datetime, pytest'


m2020_dev_kernels_for_test = [
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_dev_kernels/m2020.tls'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_dev_kernels/M2020_SCLKSCET.NOMNM.tsc'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_dev_kernels/m2020_lmst_dev00_v3.tsc'),
    os.path.join(os.path.dirname(__file__), 'inputs/common_kernels/pck00010.tpc'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_dev_kernels/de430s.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/common_kernels/mar097.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_dev_kernels/m2020_ls_dev00_iau2000_v3.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_dev_kernels/m2020_atls_dev00_v3.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_dev_kernels/m2020_tp_dev00_iau2000_v3.tf'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_dev_kernels/m2020_lmst_dev00_v3.tsc')
]

m2020_gst_kernels_for_test = [
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/de438s.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/m2020.tf'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/m2020.tls'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/m2020.tsc'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/m2020_atls_jez_v3.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/m2020_FMAresponse_JEZ_20200717_P000.cruise.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/m2020_FMAresponse_JEZ_20200717_P000.edl.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/m2020_lmst_jez_v3.tsc'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/m2020_ls_jez_iau2000_v3.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/m2020_kernels_jez_v3/m2020_tp_jez_iau2000_v3.tf'),
    os.path.join(os.path.dirname(__file__), 'inputs/common_kernels/pck00010.tpc'),
    os.path.join(os.path.dirname(__file__), 'inputs/common_kernels/mar097.bsp')
]

msl_kernels_for_test = [
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/msl_ls_ops120808_iau2000_v1.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/naif0012.tls'),
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/de425s.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/common_kernels/mar097.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/msl.tls'),
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/msl_atls_ops120808_v1.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/msl_cruise.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/msl_lmst_ops120808_v1.tsc'),
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/pck00008.tpc'),
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/msl.tf'),
    os.path.join(os.path.dirname(__file__), 'inputs/msl_kernels_07102019/msl.tsc')
]

nsyt_kernels_for_test = [
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/de430s.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight.tls'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight.tsc'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight_atls_ops181206_v1.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight_lmst_ops181206_v1.tsc'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight_ls_ops181206_iau2000_v1.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight_nom_2016e09o_cruise_v1.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight_nom_2016e09o_edl_v1.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight_surf_ops_v1.bc'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight_tp_ops181206_iau2000_v1.tf'),
    os.path.join(os.path.dirname(__file__), 'inputs/nsyt_kernels_07112019/insight_v05.tf'),
    os.path.join(os.path.dirname(__file__), 'inputs/common_kernels/mar097.bsp'),
    os.path.join(os.path.dirname(__file__), 'inputs/common_kernels/pck00010.tpc'),
]

psyche_kernels_for_test = [
    os.path.join(os.path.dirname(__file__), 'inputs/psyche_kernels_20231017/naif0012.tls'),
    os.path.join(os.path.dirname(__file__), 'inputs/psyche_kernels_20231017/PSYC_255_SCLKSCET.00003.tsc')
]

m2020_chronos_file = os.path.join(os.path.dirname(__file__), 'inputs/chronos_config_files/chronos.m2020_multiple_paths')
insight_chronos_file = os.path.join(os.path.dirname(__file__), 'inputs/chronos_config_files/chronos.insight_test')

Time.set_spacecraft_id_and_lmst_id(-168)
Time.reload_kernels(m2020_dev_kernels_for_test)


def test_time_from_et():
    assert Time(0).to_string() == '2000-001T11:58:55.816'
    assert Time(-1).to_string() == '2000-001T11:58:54.816'
    assert Time(1).to_string() == '2000-001T11:58:56.816'

def test_time_from_utc():
    time_string1 = '2019-150T00:00:00.000'
    time_string2 = ' 2019-150T00:00:00.000'
    time_string3 = '2019-150T00:00:00.000 '
    time_string4 = '2019-150T00:00:00.000\n'
    time_string5 = '  2019-150T00:00:00.000  '
    time_string6 = '9000-300T00:00:00.000'
    time_string1_short = '2019-150T00:00:00'

    assert str(Time(time_string1)) == time_string1
    assert repr(Time(time_string1)) == time_string1
    assert Time(time_string1).to_string() == time_string1
    assert Time(time_string2).to_string() == time_string2.strip()
    assert Time(time_string3).to_string() == time_string3.strip()
    assert Time(time_string4).to_string() == time_string4.strip()
    assert Time(time_string5).to_string() == time_string5.strip()
    assert Time(time_string6).to_string() == time_string6.strip()
    assert Time(time_string1_short).to_string() == time_string1

def test_time_from_tdb():
    time_string = '2460492.959134080'
    assert '2024-183T11:00:00.000' == Time(time_string + ' JD TDB').to_utc(3)

    time_string1 = '2020-001//12:00:00'
    assert '2020-001T11:58:50.816' == Time(time_string1 + ' TDB').to_utc(3)

def test_ert_ett_to_scet():
    time_string = '2021-150T00:00:00'
    ert_time = Time.from_ert(time_string)
    ett_time = Time.from_ett(time_string)

    assert ert_time == Time('2021-149T23:41:23.208')
    assert ett_time == Time('2021-150T00:18:36.728')

def test_scet_to_ert_ett():
    scet1 = Time('2021-149T23:41:23.208')
    scet2 = Time('2021-150T00:18:36.728')
    expected_string = '2021-150T00:00:00.000'

    assert scet1.to_ert() == expected_string
    assert scet2.to_ett() == expected_string

def test_time_from_lmst():
    # first test different numbers of 0s in the string
    # this is important because of the weird way LMST conversions are treated in SPICE

    lmst_str0 = 'Sol-050M00:00:00'
    lmst_str1 = 'Sol-050M00:00:00.1'

    assert Time(lmst_str0).to_utc() == '2021-100T18:41:52.028'
    for i in range(0, 10):
        assert Time(lmst_str0 + '.' + '0' * i).to_utc() == '2021-100T18:41:52.028'

    assert Time(lmst_str1).to_utc() == '2021-100T18:41:52.131'
    for i in range(0, 10):
        assert Time(lmst_str1 + '0' * i).to_utc() == '2021-100T18:41:52.131'

    # test different LMST formats
    lmst1 = Time('Sol-0150M12:34:56.789')
    lmst2 = Time('sol-0150M12:34:56.789')
    lmst3 = Time('SOL-0150M12:34:56.789')
    lmst4 = Time('SOL 0150 12:34:56.789')
    lmst5 = Time('150 12:34:56.789')
    lmst6 = Time('000150 12:34:56.789')
    lmst7 = Time('0150 12:34:56.789')

    assert lmst1 == lmst2 == lmst3 == lmst4 == lmst5 == lmst6 == lmst7

def test_time_to_datetime():
    assert Time('2019-001T00:00:00.000').to_datetime() == datetime(2019,1,1,0,0,0)
    assert Time('2019-001T00:00:00.000').to_date() == date(2019,1,1)

    # check that leap seconds can be converted
    assert Time('2016-366T23:59:60').to_datetime() == datetime(2016,12,31,23,59,59)
    assert Time('2016-366T23:59:60').to_date() == date(2016, 12, 31)

def test_time_from_datetime():
    dt = datetime(2019,1,1,0,0,0)
    d = date(2019,1,1)
    assert Time(dt).to_utc() == '2019-001T00:00:00.000'
    assert Time(d).to_utc() == '2019-001T00:00:00.000'

def test_from_week_day():
    assert Time.from_iso_week_day(2023, 1, 5) == Time('2023-006T00:00:00')
    assert Time.from_iso_week_day(2019, 40, 1) == Time('2019-273T00:00:00')
    assert Time.from_iso_week_day(2022, 52, 6) == Time.from_iso_week_day(2023, 0, 6)

def test_add():
    t = Time('2020-001T00:00:00')
    d1 = Duration('05:00:00')
    d2 = d1 * -1
    e1 = Time('2020-001T05:00:00')
    e2 = Time('2019-365T19:00:00')

    assert t + d1 == e1
    assert d1 + t == e1
    assert t + d2 == e2

def test_subtract():
    t = Time('2020-001T00:00:00')
    d1 = Duration('05:00:00')
    d2 = d1 * -1
    e1 = Time('2019-365T19:00:00')
    e2 = Time('2020-001T05:00:00')

    assert t - d1 == e1
    assert t - d2 == e2

def test_equals():
    t1 = Time('2020-001T00:00:00')
    t2 = Time('2020-001T00:00:00.00004')
    t3 = Time('2020-002T00:00:00')
    t4 = Time('2020-003T00:00:00')

    assert not t1 == None
    assert t1 == t1
    assert t1 == t2
    assert not t1 == t3
    assert not t1 == t4

def test_not_equals():
    t1 = Time('2020-001T00:00:00')
    t2 = Time('2020-001T00:00:00.00004')
    t3 = Time('2020-002T00:00:00')
    t4 = Time('2020-003T00:00:00')

    assert t1 != None
    assert not t1 != t1
    assert not t1 != t2
    assert t1 != t3
    assert t1 != t4

def test_less_than():
    t1 = Time('2020-001T00:00:00')
    t2 = Time('2020-001T00:00:00.00004')
    t3 = Time('2020-002T00:00:00')
    t4 = Time('2020-003T00:00:00')

    assert not t1 < t1
    assert not t1 < t2
    assert t1 < t3
    assert t1 < t4

def test_greater_than():
    t1 = Time('2020-001T00:00:00')
    t2 = Time('2020-001T00:00:00.00004')
    t3 = Time('2020-002T00:00:00')
    t4 = Time('2020-003T00:00:00')

    assert not t1 > t1
    assert not t1 > t2
    assert not t1 > t3
    assert not t1 > t4
    assert t4 > t1

def test_less_than_or_equal_to():
    t1 = Time('2020-001T00:00:00')
    t2 = Time('2020-001T00:00:00.00004')
    t3 = Time('2020-002T00:00:00')
    t4 = Time('2020-003T00:00:00')

    assert t1 <= t1
    assert t1 <= t2
    assert t1 <= t3
    assert t1 <= t4
    assert not t4 <= t1

def test_greater_than_or_equal_to():
    t1 = Time('2020-001T00:00:00')
    t2 = Time('2020-001T00:00:00.00004')
    t3 = Time('2020-002T00:00:00')
    t4 = Time('2020-003T00:00:00')

    assert t1 >= t1
    assert t1 >= t2
    assert not t1 >= t3
    assert not t1 >= t4
    assert t4 >= t1

def test_is_between():
    t1 = Time('2020-001T00:00:00')
    t2 = Time('2020-002T00:00:00')
    t3 = Time('2020-003T00:00:00')

    assert not t1.is_between(t2, t3)
    assert t2.is_between(t1, t3)
    assert not t3.is_between(t1, t2)

def test_round():
    t1 = Time('2020-365T12:26:49.972')
    t2 = Time('2020-366T12:30:00')
    d1 = Duration('1T00:00:00')
    d2 = Duration('01:00:00')
    d3 = Duration('00:01:00')
    d4 = Duration('00:00:01')

    assert t1.round(d1) == Time('2020-366T00:00:00')
    assert t1.round(d2) == Time('2020-365T12:00:00')
    assert t1.round(d3) == Time('2020-365T12:27:00')
    assert t1.round(d4) == Time('2020-365T12:26:50')
    assert t2.round(d1) == Time('2021-001T00:00:00')

def test_ceil():
    t1 = Time('2020-365T12:26:49.972')
    d1 = Duration('1T00:00:00')
    d2 = Duration('01:00:00')
    d3 = Duration('00:01:00')
    d4 = Duration('00:00:01')

    assert t1.ceil(d1) == Time('2020-366T00:00:00')
    assert t1.ceil(d2) == Time('2020-365T13:00:00')
    assert t1.ceil(d3) == Time('2020-365T12:27:00')
    assert t1.ceil(d4) == Time('2020-365T12:26:50')

def test_floor():
    t1 = Time('2020-365T12:26:49.972')
    d1 = Duration('1T00:00:00')
    d2 = Duration('01:00:00')
    d3 = Duration('00:01:00')
    d4 = Duration('00:00:01')

    assert t1.floor(d1) == Time('2020-365T00:00:00')
    assert t1.floor(d2) == Time('2020-365T12:00:00')
    assert t1.floor(d3) == Time('2020-365T12:26:00')
    assert t1.floor(d4) == Time('2020-365T12:26:49')


def test_round_lmst():
    lmst = Time('Sol-1234M12:34:56.123')
    d1 = Duration('1M00:00:00')
    d2 = Duration('M01:00:00')
    d3 = Duration('M00:01:00')
    d4 = Duration('M00:00:01')

    assert lmst.round_lmst(d1) == Time('Sol-1235M00:00:00')
    assert lmst.round_lmst(d2) == Time('Sol-1234M13:00:00')
    assert lmst.round_lmst(d3) == Time('Sol-1234M12:35:00')
    assert lmst.round_lmst(d4) == Time('Sol-1234M12:34:56')


def test_ceil_lmst():
    lmst = Time('Sol-1234M12:34:56.123')
    d1 = Duration('1M00:00:00')
    d2 = Duration('M01:00:00')
    d3 = Duration('M00:01:00')
    d4 = Duration('M00:00:01')

    assert lmst.ceil_lmst(d1) == Time('Sol-1235M00:00:00')
    assert lmst.ceil_lmst(d2) == Time('Sol-1234M13:00:00')
    assert lmst.ceil_lmst(d3) == Time('Sol-1234M12:35:00')
    assert lmst.ceil_lmst(d4) == Time('Sol-1234M12:34:57')


def test_floor_lmst():
    lmst = Time('Sol-1234M12:34:56.789123')
    d1 = Duration('1M00:00:00')
    d2 = Duration('M01:00:00')
    d3 = Duration('M00:01:00')
    d4 = Duration('M00:00:01')

    assert lmst.floor_lmst(d1) == Time('Sol-1234M00:00:00')
    assert lmst.floor_lmst(d2) == Time('Sol-1234M12:00:00')
    assert lmst.floor_lmst(d3) == Time('Sol-1234M12:34:00')
    assert lmst.floor_lmst(d4) == Time('Sol-1234M12:34:56')


def test_to_string():
    s1 = '2020-002T00:00:00.000'
    t1 = Time(s1)
    assert t1.to_string() == s1


def test_to_time_formats():
    t = Time('2020-002T00:00:00')

    assert t.to_utc() == '2020-002T00:00:00.000'
    assert t.to_utc_strftime('%m/%d/%Y, %H:%M:%S') == '01/02/2020, 00:00:00'
    assert t.to_isoc() == '2020-01-02T00:00:00.000'
    assert t.to_julian() == 'JD 2458850.500'
    assert t.to_calendar() == '2020 JAN 02 00:00:00.000'


def test_to_timezones():
    t = Time('2020-002T00:00:00')

    assert t.to_pt() == '2020-001T16:00:00.000'
    assert t.to_indian_std_time() == '2020-002T05:30:00.000'
    assert t.to_timezone('America/Adak') == '2020-001T14:00:00.000'


def test_to_lmst():
    t = Time('2022-001T00:00:00')
    assert t.to_lmst() == 'Sol-0308M02:59:38.698'
    assert t.to_lmst(0) == 'Sol-0308M02:59:39'
    assert t.to_lmst(1) == 'Sol-0308M02:59:38.7'
    assert t.to_lmst(2) == 'Sol-0308M02:59:38.70'
    assert t.to_lmst(3) == 'Sol-0308M02:59:38.698'


def test_to_lmst_strftime():
    t = Time('2022-001T00:00:00')
    format_string1 = 'Sol-{0:04d}M{1:02d}:{2:02d}:{3:06.3f}'
    format_string2 = 'SOL {0:04d} {1:02d}:{2:02d}:{3:09.6f}'
    assert t.to_lmst_strftime(format_string1) == 'Sol-0308M02:59:38.698'
    assert t.to_lmst_strftime(format_string2) == 'SOL 0308 02:59:38.698040'


def test_to_lmst_am_pm():
    am1 = Time('Sol-150M11:55:00')
    am2 = Time('Sol-150M00:00:00')
    am3 = Time('Sol-150M11:59:59.999')
    am4 = Time('Sol-150M05:00:00.123')

    pm1 = Time('Sol-150M23:55:00')
    pm2 = Time('Sol-150M12:00:00')
    pm3 = Time('Sol-150M23:59:59.999')
    pm4 = Time('Sol-150M17:00:00.123')

    assert am1.to_lmst_am_pm() == am2.to_lmst_am_pm() == am3.to_lmst_am_pm() == am4.to_lmst_am_pm() == 'AM'
    assert pm1.to_lmst_am_pm() == pm2.to_lmst_am_pm() == pm3.to_lmst_am_pm() == pm4.to_lmst_am_pm() == 'PM'


def test_to_ltst():
    t = Time('2022-001T00:00:00')
    assert t.to_ltst() == 'Sol-0308T03:32:42'


def test_from_ltst():
    # make sure that each comparison is within 1.1 seconds
    Time.set_comparison_precision(Duration(1.1))
    for i in range(0, 500):
        t = Time('2021-150T00:00:00') + Duration("T06:00:00") * i
        ltst = t.to_ltst()
        assert Time.from_ltst(ltst) == t


def test_to_sclk():
    t = Time('2022-001T00:00:00')
    assert t.to_sclk() == '1/0694267269-12059'


def test_to_sclkd():
    t = Time('2022-001T00:00:00')
    assert t.to_sclkd() == 694267269.1840057


def test_from_sclk():
    t1 = Time.from_sclk('1/0793195269-12059')
    assert t1 == Time('2025-050T00:00:00.000')

    t2 = Time.from_sclk('1/0793195269:12059')
    assert t2 == Time('2025-050T00:00:00.000')

    t3 = Time.from_sclk('1/0793195269 12059')
    assert t3 == Time('2025-050T00:00:00.000')

    t4 = Time.from_sclk('1/0793195269,12059')
    assert t4 == Time('2025-050T00:00:00.000')

    t5 = Time.from_sclk('1/0793195269.12059')
    assert t5 == Time('2025-050T00:00:00.000')


def test_to_sols():
    t1 = Time('2022-001T00:00:00')
    t2 = Time('Sol-050M00:01:00')

    assert t1.to_sols() == 308
    assert t2.to_sols() == 50


def test_to_fractional_sols():
    t1 = Time('Sol-050M12:00:00')
    t2 = Time('Sol-100M06:00:00')

    assert t1.to_fractional_sols() == 50.5
    assert t2.to_fractional_sols() == 100.25


def test_to_et():
    t1 = Time('2022-001T00:00:00')
    t2 = Time(t1.to_et())
    assert t1.to_et() == 694267269.1839212
    assert t1 == t2


def test_to_from_tai():
    t1 = Time()
    t1_tai = t1.to_tai()
    t2 = Time('2020-001T00:00:00')
    t2_tai = t2.to_tai()

    assert t1_tai == Time.from_tai(t1_tai).to_tai()
    assert t2_tai == Time.from_tai(t2_tai).to_tai()
    assert t2_tai == spice.unitim(t2.to_et(), 'ET', 'TAI')


def test_to_scet():
    t1 = Time('2022-001T00:00:00')
    assert t1.to_scet() == '2022-001T00:00:00.000'


def test_to_ert():
    t1 = Time('2022-001T00:00:00')
    downleg = Time.downleg(t1)
    ert1 = t1 + downleg

    assert t1.to_ert() == ert1.to_utc()


def test_to_ett():
    t1 = Time('2022-001T00:00:00')
    upleg = Time.upleg(t1)
    ett1 = t1 - upleg

    assert t1.to_ett() == ett1.to_utc()


def test_to_gps():
    t1 = Time('1980-006T00:00:00')
    t2 = Time('2020-150T00:00:00')
    t3 = Time('2021-001T00:00:00')

    assert t1.to_gps_seconds() == 0
    assert t2.to_gps() == '2020-150T00:00:18.000'
    assert t3.to_gps_seconds() == 1293494418 # this number came from https://www.andrews.edu/~tzs/timeconv/timedisplay.php


def test_from_gps():
    t1 = 0
    t2 = '2020-150T00:00:18.000'
    t3 = 1293494418

    assert Time.from_gps_seconds(t1).to_string() == Time(GPST_EPOCH).to_string()
    assert Time.from_gps(t2).to_string() == Time('2020-150T00:00:00.000').to_string()
    assert Time.from_gps_seconds(t3).to_string() == Time('2021-001T00:00:00').to_string()


def test_min():
    t1 = Time('2022-001T00:00:00')
    t2 = Time('2022-001T00:00:00.0004')
    t3 = Time('2022-001T00:00:01')
    t4 = Time('2022-002T00:00:00')

    Time.set_comparison_precision(Duration(0.001))

    assert min([t1, t2]) == t1
    assert min([t1, t2]) == t2
    assert not min([t1, t3]) == t3
    assert min([t4, t3, t2, t1]) == t1


def test_max():
    t1 = Time('2022-001T00:00:00')
    t2 = Time('2022-001T00:00:00.0004')
    t3 = Time('2022-001T00:00:01')
    t4 = Time('2022-002T00:00:00')

    assert max([t1, t2]) == t1
    assert max([t1, t2]) == t2
    assert max([t1, t3]) == t3
    assert max([t4, t3, t2, t1]) == t4


def test_set_time_decimal_precision():
    # we want to compare for different precisions
    t = Time('2022-001T00:00:00')
    t2 = Time('2022-001T00:00:01')
    t3 = Time('2022-001T00:00:00.1')
    t4 = Time('2022-001T00:00:00.01')
    t5 = Time('2022-001T00:00:00.001')
    t6 = Time('2022-001T00:00:00.0001')

    # default precision is 3
    assert t.to_lmst() == 'Sol-0308M02:59:38.698'
    assert t != t5
    assert t == t6

    Time.set_output_decimal_precision(-1)
    Time.set_comparison_precision(Duration(10))
    assert t.to_lmst() == 'Sol-0308M02:59:40'
    assert t == t2

    Time.set_output_decimal_precision(0)
    Time.set_comparison_precision(Duration(1))
    assert t.to_lmst() == 'Sol-0308M02:59:39'
    assert t != t2
    assert t == t3

    Time.set_output_decimal_precision(1)
    Time.set_comparison_precision(Duration(.1))
    assert t.to_lmst() == 'Sol-0308M02:59:38.7'
    assert t != t3
    assert t == t4

    Time.set_output_decimal_precision(2)
    Time.set_comparison_precision(Duration(.01))
    assert t.to_lmst() == 'Sol-0308M02:59:38.70'
    assert t != t4
    assert t == t5

    Time.set_output_decimal_precision(3)
    Time.set_comparison_precision(Duration(.001))
    assert t.to_lmst() == 'Sol-0308M02:59:38.698'
    assert t != t5
    assert t == t6


def test_update_spacecraft():
    t = Time('2021-150T00:00:00')
    assert t.get_spacecraft_id() == -168
    assert t.to_lmst() == 'Sol-0097M21:41:44.318'

    Time.set_spacecraft_id(-76)
    Time.set_lmst_sclk_id(-76900)
    Time.reload_kernels(msl_kernels_for_test)

    assert t.get_spacecraft_id() == -76
    assert t.to_lmst() == 'Sol-3133M06:51:24.930'
    assert round(t.to_sclkd(), 3) == 675602050.989

    # test method which sets both
    Time.set_spacecraft_id(-168)
    Time.set_lmst_sclk_id(-168900)
    Time.set_spacecraft_id_and_lmst_id(-76)
    assert t.to_lmst() == 'Sol-3133M06:51:24.930'


def test_now():
    now_dt = datetime.utcnow()
    now_time = Time.now()
    Time.set_comparison_precision(Duration("00:00:01"))
    assert Time(now_dt) == now_time


def test_unload_kernel():
    # make sure this does not crash
    Time.unload_kernel('test')

    # test reloading the kernels and getting list of kernels
    Time.reload_kernels(m2020_dev_kernels_for_test)
    kernel_list = Time.get_all_loaded_kernels()
    assert len(kernel_list) == len(m2020_dev_kernels_for_test)

    # test unloading a kernel without the path
    Time.unload_kernel('m2020.tls')
    kernel_list2 = Time.get_all_loaded_kernels()
    assert len(kernel_list) - 1 == len(kernel_list2)

    # test unloading all kernels
    Time.unload_kernels(m2020_dev_kernels_for_test)
    assert len(Time.get_all_loaded_kernels()) == 0

    Time.reload_kernels(m2020_dev_kernels_for_test)
    Time.set_spacecraft_id_and_lmst_id(-168)


def test_msl_isa_51015():
    # msl_time.​py and the msltime web service appear to only allow 5 digits of precision.​
    # this test verifies that the from_sclkd method behaves correctly

    Time.reload_kernels(msl_kernels_for_test)
    Time.set_spacecraft_id_and_lmst_id(-76)

    t1 = Time.from_sclkd(428432592.48402)
    t2 = Time.from_sclkd(428432592.48404)
    t3 = Time.from_sclkd(428432592.484024434)
    t4 = Time.from_sclkd(428432592.48403)

    # note that this is comparing 3 decimal places in utc, which is why they are the same
    assert t1.to_utc() == t2.to_utc() == t3.to_utc() == t4.to_utc()

    t5 = Time.from_sclk('1/0428432592-48402')
    t6 = Time.from_sclk('1/0428432592-48403')

    assert t5.to_utc() == t6.to_utc()

    Time.reload_kernels(m2020_dev_kernels_for_test)
    Time.set_spacecraft_id_and_lmst_id(-168)


def test_msl_isa_50875():
    Time.reload_kernels(msl_kernels_for_test)
    Time.set_spacecraft_id_and_lmst_id(-76)

    # msl_time and viper disagree in one-​way light time for the same time.​
    t = Time('2011-353T23:59:59')
    assert round(Time.downleg(t).to_seconds(), 3) == 22.725

    Time.reload_kernels(m2020_dev_kernels_for_test)
    Time.set_spacecraft_id_and_lmst_id(-168)


def test_msl_isa_56582():
    Time.reload_kernels(msl_kernels_for_test)
    Time.set_spacecraft_id_and_lmst_id(-76)

    # Call to msl_time that failed: msl_time.​py -​t Sol-​671M10:00:00
    t = Time('Sol-671M10:00:00')
    assert t.to_lmst() == 'Sol-0671M10:00:00.000'

    Time.reload_kernels(m2020_dev_kernels_for_test)
    Time.set_spacecraft_id_and_lmst_id(-168)


def test_psyche_issue_sclkd():
    Time.set_spacecraft_id(-255)
    Time.reload_kernels(psyche_kernels_for_test)
    mydict = convert_to_all_formats(Time('2023-10-17T20:37:00'))
    assert mydict['sclkd'] == '750847089.1840057'


def test_load_chronos_config():
    # this tests using relative paths in chronos files and getting the SC and LMST IDs from the files
    # first load insight file
    load_chronos_config(insight_chronos_file)
    assert Time.get_spacecraft_id() == -189
    assert Time.get_lmst_sclk_id() == -189900
    assert Time('2019-352T21:01:08.972').to_lmst(3) == 'Sol-0377M06:54:27.996'

    load_chronos_config(m2020_chronos_file)
    assert Time.get_spacecraft_id() == -168
    assert Time.get_lmst_sclk_id() == -168900
    assert Time('2022-001T00:00:00').to_lmst(3) == 'Sol-0308M02:59:38.698'

    Time.reload_kernels(m2020_dev_kernels_for_test)


def test_epoch_relative_times():
    t0 = Time('2000-001T00:00:00')
    EpochRelativeTime.add_epoch('a', t0)
    t1 = EpochRelativeTime('a+00:05:00')
    d = Duration('00:10:00')

    t2 = t1 - d
    t3 = d + t1
    d2 = t1 - t0
    times = [t0, t1, t2]

    assert 'a+00:05:00' == t1.to_string(0)
    assert '2000-001T00:05:00' == t1.to_utc(0)
    assert 'a-00:05:00' == t2.to_string(0)
    assert '1999-365T23:55:00' == t2.to_utc(0)
    assert '00:05:00' == d2.to_string(0)
    assert 'a+00:15:00' == t3.to_string(0)
    assert 'a+00:15:00.000' == str(t3)

    assert -42835.81608708757 == t1.to_et()

    sorted_times = sorted(times)
    assert 'a-00:05:00,2000-001T00:00:00,a+00:05:00' == ','.join([time.to_string(0) for time in sorted_times])


def test_get_epoch_cvf_string():
    EpochRelativeTime.add_epoch("test",        Time("2000-001T12:00:00"))
    EpochRelativeTime.add_epoch("hello_there", Time("2020-001T00:00:00"))
    EpochRelativeTime.add_epoch("third",       Time("2022-001T00:00:00"))
    EpochRelativeTime.add_epoch("gps_test",    Time("2021-001T00:00:00"))

    cvf_string = EpochRelativeTime._get_epoch_cvf_string(['test', 'hello_there', 'gps_test'])
    assert "/hello_there\n\"const\" 2020-001T00:00:00" in cvf_string
    assert "/gps_test\n\"const\" 2021-001T00:00:00" in cvf_string
    assert cvf_string.index("test") < cvf_string.index("gps_test")

    cvf_string = EpochRelativeTime._get_epoch_cvf_string(header_in='MPST\n', sort_by_time=False)
    assert '/third\n' in cvf_string
    assert 'MPST\n' in cvf_string
    assert cvf_string.index('gps_test') < cvf_string.index('test')


def test_add_all_from_epoch_cvf():
    epoch_file = os.path.join(os.path.dirname(__file__), 'inputs/cvf/dc075a_tf.r4.cvf')

    EpochRelativeTime.add_all_from_epoch_cvf(epoch_file)
    assert Time('2014-231T02:44:00') == Time(EpochRelativeTime('CRU_seqbound_001', Duration(0)))
    assert Time('2014-240T18:00:11') == Time(EpochRelativeTime('CRU_tv_003', Duration(0)))
    assert Time('2014-258T10:38:04') == Time(EpochRelativeTime('CRU_comm_002', Duration(0)))
    assert Time('2014-300T08:00:00') == Time(EpochRelativeTime('CRU_coast_004', Duration(0)))


def test_to_gst():
    # load kernels for GST tests
    Time.reload_kernels(m2020_gst_kernels_for_test)

    local_midnight = Time('Sol-0000M00:00:00')

    # from SFP windows CEDL defaults 20191023
    assert Time('Sol-000M02:15:00').to_gst(local_midnight) == 8323
    assert Time('Sol-000M08:30:00').to_gst(local_midnight) == 31441
    assert Time('Sol-000M09:00:00').to_gst(local_midnight) == 33291
    assert Time('Sol-000M09:30:00').to_gst(local_midnight) == 35140
    assert Time('Sol-000M14:15:00').to_gst(local_midnight) == 52710
    assert Time('Sol-000M19:41:00').to_gst(local_midnight) == 72808

    expected_offset_per_sol = 0.24414688000979368
    for i in range(0, 2000):
        assert (Time('Sol-0M00:00:00') + Duration('1M00:00:00') * i).to_gst(local_midnight) == int(round(expected_offset_per_sol * i))

    Time.reload_kernels(m2020_dev_kernels_for_test)


def test_from_gst():
    # load kernels for GST tests
    Time.reload_kernels(m2020_gst_kernels_for_test)

    local_midnight = Time('Sol-0000M00:00:00')

    # from SFP windows CEDL defaults 20191023
    assert Time.from_gst(8323, 0, local_midnight, 0) == Time('Sol-0000M02:15:00.312')
    assert Time.from_gst(31441, 0, local_midnight, 0) == Time('Sol-0000M08:29:59.774')
    assert Time.from_gst(33291, 0, local_midnight, 0) == Time('Sol-0000M09:00:00.276')
    assert Time.from_gst(35140, 0, local_midnight, 0) == Time('Sol-0000M09:29:59.805')
    assert Time.from_gst(52710, 0, local_midnight, 0) == Time('Sol-0000M14:14:59.707')
    assert Time.from_gst(72808, 0, local_midnight, 0) == Time('Sol-0000M19:40:59.971')

    Time.set_comparison_precision(Duration('M00:00:00.5'))
    expected_offset_per_sol = 0.24414688000979368
    for i in range(0, 2000):
        assert (Time('Sol-0M00:00:00') + Duration('1M00:00:00') * i) == \
            Time.from_gst(int(round(expected_offset_per_sol * i)), i, local_midnight, 0)

    Time.set_comparison_precision(Duration(0.001))
    Time.reload_kernels(m2020_dev_kernels_for_test)
