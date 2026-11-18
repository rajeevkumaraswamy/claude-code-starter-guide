"""Session 1 checkpoint: sensorlog.stats.summarize.

Run: uv run pytest checkpoints/test_session_1.py
"""

import math

import pandas as pd

from sensorlog.stats import summarize


def _frame(rows):
    """Build a frame with the load_csv schema (even when empty)."""
    return pd.DataFrame(
        {
            "timestamp": pd.Series(
                pd.to_datetime(
                    [f"2026-01-01 00:{i:02d}:00" for i in range(len(rows))],
                    utc=True,
                ),
                dtype="datetime64[ns, UTC]",
            ),
            "sensor_id": pd.Series([r[0] for r in rows], dtype=object),
            "value": pd.Series([r[1] for r in rows], dtype="float64"),
        }
    )


def test_summarize_two_sensors():
    df = _frame([("a", 1), ("a", 2), ("a", 3), ("b", 10)])
    assert summarize(df) == {
        "a": {"count": 3, "mean": 2.0, "min": 1.0, "max": 3.0},
        "b": {"count": 1, "mean": 10.0, "min": 10.0, "max": 10.0},
    }


def test_summarize_excludes_nan():
    df = _frame([("a", 1), ("a", math.nan), ("a", 3)])
    result = summarize(df)
    assert result["a"]["count"] == 2
    assert result["a"]["mean"] == 2.0


def test_summarize_all_nan_sensor():
    df = _frame([("a", math.nan), ("a", math.nan)])
    result = summarize(df)
    assert result["a"]["count"] == 0
    assert math.isnan(result["a"]["mean"])


def test_summarize_empty():
    df = _frame([])
    assert summarize(df) == {}
