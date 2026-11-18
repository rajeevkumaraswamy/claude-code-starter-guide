import pandas as pd
import pytest

from sensorlog.stats import mean_sample_interval


def _df(seconds):
    ts = pd.to_datetime(seconds, unit="s", utc=True)
    return pd.DataFrame(
        {"timestamp": ts, "sensor_id": "temp_1", "value": [1.0] * len(seconds)}
    )


def test_mean_interval_sorted_data():
    assert mean_sample_interval(_df([0, 60, 120]), "temp_1") == 60.0


def test_mean_interval_single_sample_raises():
    with pytest.raises(ValueError, match="need at least 2 samples"):
        mean_sample_interval(_df([0]), "temp_1")
