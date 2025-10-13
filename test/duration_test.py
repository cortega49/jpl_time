"""
Unit tests for Duration class.
"""

from datetime import timedelta
from jpl_time import Duration

__program__ = 'duration_test.py'
__author__  = 'Forrest Ridenhour'
__project__ = 'Mars2020'
__version__ = '1.0'
__dependencies__ = 'jpl_time.py, datetime, pytest'


ONE_SECOND = Duration('00:00:01')
ONE_MINUTE = Duration('00:01:00')
ONE_HOUR = Duration('01:00:00')
ONE_DAY = Duration('1T00:00:00')
ONE_SOL = Duration('1M00:00:00')

def test_creating_durations_from_seconds():
    assert Duration(1).to_seconds() == 1
    assert str(Duration(5.5)) == '00:00:05.500'
    assert repr(Duration(5.5)) == '00:00:05.500'
    assert Duration(5.5).to_string() == '00:00:05.500'
    assert Duration(-1).to_string() == '-00:00:01.000'
    assert Duration(0).to_string() == '00:00:00.000'
    assert Duration(-10.0) == Duration(-10)

def test_creating_durations_from_timedelta():
    assert Duration(timedelta(seconds=1)) == Duration(1)

def test_creating_durations_from_strings():
    assert Duration('0:1:0').to_string() == '00:01:00.000'
    assert Duration(' 0:1:0').to_string() == '00:01:00.000'
    assert Duration('0:1:0\n').to_string() == '00:01:00.000'
    assert Duration('  0:1:0  ').to_string() == '00:01:00.000'
    assert Duration('00:01:00').to_string() == '00:01:00.000'
    assert Duration('0:1:0.0000').to_string() == '00:01:00.000'
    assert Duration('00:00:01').to_seconds() == 1
    assert Duration('M00:00:01').to_seconds() == 1.0274912517
    assert Duration('5T00:00:01').to_string() == '5T00:00:01.000'
    assert Duration('1M00:00:00').to_mars_dur() == '1M00:00:00.000'
    assert Duration('-01:00:00').to_string() == '-01:00:00.000'
    assert Duration('50:00:00').to_string() == '2T02:00:00.000'

def test_to_string_decimals():
    d = Duration('01:00:02.5649')
    assert d.to_string(0) == '01:00:03'
    assert d.to_string(1) == '01:00:02.6'
    assert d.to_string(2) == '01:00:02.56'
    assert d.to_string(3) == '01:00:02.565'
    assert d.to_string(4) == '01:00:02.5649'
    assert d.to_string(5) == '01:00:02.56490'
    assert d.to_string(6) == '01:00:02.564900'

def test_strfdelta():
    d1 = Duration('-3T4:5:6.789')
    assert d1.strfdelta('{1:02d}T{2:02d}:{3:02d}:{4:05.2f}') == '03T04:05:06.79'
    assert d1.strfdelta('{0}{1:02d}T{2:02d}:{3:02d}:{4:06.3f}') == '-03T04:05:06.789'
    assert d1.strfdelta('{0}{1} days, {2} hours, {3} minutes, {4} seconds') == '-3 days, 4 hours, 5 minutes, 6.789 seconds'

    d2 = Duration('04:05:00.001')
    assert d2.strfdelta('{0}{1} days, {2} hours, {3} minutes, {4} seconds') == '0 days, 4 hours, 5 minutes, 0.001 seconds'

def test_mars_strfdelta():
    d1 = Duration('-3M04:05:06.789')
    assert d1.mars_strfdelta('{0}{1} sols, {2} hours, {3} minutes, {4} seconds') == '-3 sols, 4 hours, 5 minutes, 6.789 seconds'

    d2 = Duration('M04:05:00.001')
    assert d2.mars_strfdelta('{0}{1} sols, {2} hours, {3} minutes, {4} seconds') == '0 sols, 4 hours, 5 minutes, 0.001 seconds'


def test_add_durations():
    assert ONE_SECOND + ONE_MINUTE == Duration('00:01:01')
    assert ONE_SECOND + ONE_MINUTE + ONE_HOUR == Duration('01:01:01')
    assert ONE_SECOND + ONE_MINUTE + ONE_HOUR + ONE_DAY == Duration('1T01:01:01')

def test_subtract_durations():
    assert ONE_HOUR - ONE_MINUTE == Duration('00:59:00')
    assert ONE_SECOND - ONE_MINUTE == Duration('-00:00:59')
    assert ONE_SECOND - ONE_HOUR == Duration('-00:59:59')

def test_multiply_durations():
    assert ONE_SECOND * 5 == Duration('00:00:05')
    assert ONE_SECOND * -10 == Duration('-00:00:10')

def test_divide_durations():
    assert ONE_MINUTE / ONE_SECOND == 60
    assert ONE_HOUR / 3600 == ONE_SECOND
    assert Duration('01:13:01') / 2 == Duration('00:36:30.5')

def test_mod():
    assert Duration('00:03:10.1251') % Duration('00:00:00.001') == Duration('00:00:00.0001')
    assert Duration('00:03:10.1251') % Duration('00:00:00.01') == Duration('00:00:00.0051')
    assert Duration('00:03:10.125') % ONE_SECOND == Duration('00:00:00.125')
    assert Duration('00:03:10.125') % ONE_MINUTE == Duration('00:00:10.125')
    assert Duration('00:03:10.125') % ONE_HOUR == Duration('00:03:10.125')

    assert Duration('00:01:00.101') % Duration('00:00:00.001') == Duration(0)
    assert Duration('00:01:00.101') % (Duration(0.001) / 3 * 3) == Duration(0)
    assert Duration('01:00:00.001') % Duration(0.25) == Duration(.001)

def test_operators():
    assert ONE_SECOND < ONE_MINUTE
    assert ONE_MINUTE > ONE_SECOND
    assert ONE_SECOND == Duration('00:00:01')
    assert ONE_SECOND >= ONE_SECOND
    assert ONE_HOUR <= ONE_HOUR
    assert not ONE_HOUR <= ONE_SECOND
    assert ONE_HOUR != ONE_SECOND

def test_to_timedelta():
    assert ONE_SECOND.to_timedelta() == timedelta(seconds=1)

def test_to_mars_dur():
    assert Duration('1M00:00:00').to_mars_dur() == '1M00:00:00.000'
    assert Duration('-M01:00:00').to_mars_dur() == '-M01:00:00.000'

def test_to_seconds():
    assert ONE_HOUR.to_seconds() == 3600
    assert (ONE_HOUR * -2).to_seconds() == -7200

    assert ONE_HOUR.to_minutes() == 60
    assert ONE_HOUR.to_hours() == 1
    assert ONE_HOUR.to_days() == 1/24

def test_abs():
    assert ONE_MINUTE.abs() == ONE_MINUTE
    assert Duration('-01:00:00').abs() == ONE_HOUR

def test_round():
    d = Duration('06:03:59.972')
    assert d.round(ONE_HOUR) == Duration('06:00:00')
    assert d.round(ONE_MINUTE) == Duration('06:04:00')
    assert d.round(ONE_SECOND) == Duration('06:04:00')

def test_ceil():
    d = Duration('06:03:59.972')
    assert d.ceil(ONE_HOUR) == Duration('07:00:00')
    assert d.ceil(ONE_MINUTE) == Duration('06:04:00')
    assert d.ceil(ONE_SECOND) == Duration('06:04:00')

def test_floor():
    d = Duration('06:03:59.972')
    assert d.floor(ONE_HOUR) == Duration('06:00:00')
    assert d.floor(ONE_MINUTE) == Duration('06:03:00')
    assert d.floor(ONE_SECOND) == Duration('06:03:59')

def test_set_duration_decimal_precision():
    d  = Duration('01:00:00')
    d2 = Duration('01:00:01')
    d3 = Duration('01:00:00.1')
    d4 = Duration('01:00:00.01')
    d5 = Duration('01:00:00.001')
    d6 = Duration('01:00:00.0001')

    # default precision is 3
    assert d == d6
    assert d != d5

    Duration.set_comparison_precision(10)
    assert d == d2

    Duration.set_comparison_precision(1)
    assert d != d2
    assert d == d3

    Duration.set_comparison_precision(.1)
    assert d != d3
    assert d == d4

    Duration.set_comparison_precision(.01)
    assert d != d4
    assert d == d5

    Duration.set_comparison_precision(.001)
    assert d != d5
    assert d == d6
