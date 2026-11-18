"""Session 4 checkpoint: sensorlog.clean.flag_outliers (Hampel filter).

Run: uv run pytest checkpoints/test_session_4.py
"""

import math

import pandas as pd

from sensorlog.clean import flag_outliers


def _frame(sensors, minutes, values):
    """Build a frame with the load_csv schema (even when empty)."""
    start = pd.Timestamp("2026-01-01", tz="UTC")
    return pd.DataFrame(
        {
            "timestamp": pd.Series(
                pd.to_datetime(
                    [start + pd.Timedelta(minutes=m) for m in minutes], utc=True
                ),
                dtype="datetime64[ns, UTC]",
            ),
            "sensor_id": pd.Series(sensors, dtype=object),
            "value": pd.Series(values, dtype="float64"),
        }
    )


def _spike_values():
    values = [10.0] * 11
    values[5] = 100.0
    return values


def test_single_spike_flagged():
    df = _frame(["a"] * 11, range(11), _spike_values())
    flags = flag_outliers(df)
    assert flags.dtype == bool
    assert list(flags.index) == list(df.index)
    assert [i for i, f in flags.items() if f] == [5]


def test_shuffled_input_flags_same_rows():
    df = _frame(["a"] * 11, range(11), _spike_values())
    shuffled = df.sample(frac=1, random_state=0)
    flags = flag_outliers(shuffled)
    assert set(flags.index) == set(df.index)
    assert [i for i, f in flags.items() if f] == [5]


def test_nan_is_not_flagged():
    values = _spike_values()
    values[2] = math.nan
    df = _frame(["a"] * 11, range(11), values)
    flags = flag_outliers(df)
    assert not flags.iloc[2]
    assert flags.iloc[5]


def test_all_nan_sensor_all_false():
    df = _frame(["a"] * 5, range(5), [math.nan] * 5)
    assert not flag_outliers(df).any()


def test_sensors_are_independent():
    sensors = ["a"] * 11 + ["b"] * 11
    minutes = list(range(11)) * 2
    values = _spike_values() + [10.0] * 11
    df = _frame(sensors, minutes, values)
    flags = flag_outliers(df)
    assert [i for i, f in flags.items() if f] == [5]
