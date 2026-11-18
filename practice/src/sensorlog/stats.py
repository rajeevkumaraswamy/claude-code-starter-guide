"""Summary statistics for sensor logs."""

import pandas as pd


def mean_sample_interval(df: pd.DataFrame, sensor_id: str) -> float:
    """Return the mean time between samples for one sensor, in seconds."""
    ts = df.loc[df["sensor_id"] == sensor_id, "timestamp"].sort_values()
    if len(ts) < 2:
        raise ValueError("need at least 2 samples")
    return float(ts.diff().dropna().mean().total_seconds())


def summarize(df: pd.DataFrame) -> dict[str, dict[str, float]]:
    """Return count, mean, min and max of valid values per sensor."""
    result: dict[str, dict[str, float]] = {}
    for sensor_id, values in df.groupby("sensor_id")["value"]:
        valid = values.dropna()
        if valid.empty:
            nan = float("nan")
            result[str(sensor_id)] = {
                "count": 0,
                "mean": nan,
                "min": nan,
                "max": nan,
            }
        else:
            result[str(sensor_id)] = {
                "count": int(valid.count()),
                "mean": float(valid.mean()),
                "min": float(valid.min()),
                "max": float(valid.max()),
            }
    return result
