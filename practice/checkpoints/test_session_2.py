"""Session 2 checkpoint: sensorlog.clean.

Run: uv run pytest checkpoints/test_session_2.py
"""

import math

import pandas as pd
import pytest

from sensorlog import clean


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


def _check_pure(func, df, *args, **kwargs):
    """Call func and verify the input is untouched and the index is reset."""
    before = df.copy()
    result = func(df, *args, **kwargs)
    pd.testing.assert_frame_equal(df, before)
    assert list(result.index) == list(range(len(result)))
    return result


def test_drop_duplicate_rows():
    df = _frame(["a", "a", "a", "b"], [0, 0, 1, 0], [1, 1, 2, 3])
    result = _check_pure(clean.drop_duplicate_rows, df)
    assert len(result) == 3


def test_sort_by_time():
    df = _frame(["b", "a", "a", "b"], [1, 5, 2, 0], [1, 2, 3, 4])
    result = _check_pure(clean.sort_by_time, df)
    assert list(result["sensor_id"]) == ["a", "a", "b", "b"]
    assert list(result["value"]) == [3.0, 2.0, 4.0, 1.0]


def test_fill_missing_within_gap():
    df = _frame(["a"] * 3, [0, 1, 2], [1, math.nan, 3])
    result = _check_pure(clean.fill_missing, df)
    assert result["value"].iloc[1] == 2.0


def test_fill_missing_gap_too_large():
    df = _frame(["a"] * 3, [0, 10, 20], [1, math.nan, 3])
    result = _check_pure(clean.fill_missing, df, max_gap=pd.Timedelta("5min"))
    assert math.isnan(result["value"].iloc[1])


@pytest.mark.parametrize(
    "func", [clean.drop_duplicate_rows, clean.sort_by_time, clean.fill_missing]
)
def test_empty_frame_keeps_columns(func):
    df = _frame([], [], [])
    result = _check_pure(func, df)
    assert len(result) == 0
    assert list(result.columns) == list(df.columns)
