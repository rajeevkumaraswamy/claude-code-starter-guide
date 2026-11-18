"""Summary statistics for sensor logs."""

import pandas as pd


def mean_sample_interval(df: pd.DataFrame, sensor_id: str) -> float:
    """Return the mean time between samples for one sensor, in seconds."""
    ts = df.loc[df["sensor_id"] == sensor_id, "timestamp"]
    if len(ts) < 2:
        raise ValueError("need at least 2 samples")
    return float(ts.diff().dropna().mean().total_seconds())
