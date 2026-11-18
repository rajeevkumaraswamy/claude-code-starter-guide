from pathlib import Path

import pandas as pd
import pytest

from sensorlog.load import load_csv

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample.csv"


def test_load_columns_and_dtypes():
    df = load_csv(SAMPLE)
    assert list(df.columns) == ["timestamp", "sensor_id", "value"]
    assert str(df["timestamp"].dt.tz) == "UTC"
    assert df["value"].dtype == "float64"


def test_load_naive_timestamps_become_utc(tmp_path):
    p = tmp_path / "naive.csv"
    p.write_text("timestamp,sensor_id,value\n2026-01-01 00:00:00,temp_1,1.5\n")
    df = load_csv(p)
    assert df.timestamp[0] == pd.Timestamp("2026-01-01", tz="UTC")


def test_load_missing_column_raises(tmp_path):
    p = tmp_path / "bad.csv"
    p.write_text("timestamp,sensor_id\n2026-01-01 00:00:00,temp_1\n")
    with pytest.raises(ValueError, match="value"):
        load_csv(p)
