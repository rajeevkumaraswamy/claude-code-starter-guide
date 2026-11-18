"""Loading sensor logs from CSV."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["timestamp", "sensor_id", "value"]


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a sensor log CSV into a DataFrame in file order.

    Returns columns ``timestamp`` (UTC), ``sensor_id`` (str) and ``value`` (float).
    Naive timestamps are interpreted as UTC.
    """
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"missing required column(s): {', '.join(missing)}")
    df = df[REQUIRED_COLUMNS].copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).astype(
        "datetime64[ns, UTC]"
    )
    df["sensor_id"] = df["sensor_id"].astype(str)
    df["value"] = df["value"].astype("float64")
    return df
