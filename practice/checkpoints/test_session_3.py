"""Session 3 checkpoint: mean_sample_interval must ignore file order.

Run: uv run pytest checkpoints/test_session_3.py
"""

import pandas as pd
import pytest

from sensorlog.stats import mean_sample_interval


def _frame(seconds):
    """Build a one-sensor frame with the load_csv schema."""
    start = pd.Timestamp("2026-01-01", tz="UTC")
    return pd.DataFrame(
        {
            "timestamp": pd.Series(
                pd.to_datetime(
                    [start + pd.Timedelta(seconds=s) for s in seconds], utc=True
                ),
                dtype="datetime64[ns, UTC]",
            ),
            "sensor_id": pd.Series(["a"] * len(seconds), dtype=object),
            "value": pd.Series([1.0] * len(seconds), dtype="float64"),
        }
    )


def test_out_of_order_rows():
    assert mean_sample_interval(_frame([0, 120, 60]), "a") == 60.0


def test_single_sample_raises():
    with pytest.raises(ValueError):
        mean_sample_interval(_frame([0]), "a")
