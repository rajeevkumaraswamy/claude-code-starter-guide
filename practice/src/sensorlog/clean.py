"""Cleaning helpers for sensor logs. Each returns a new DataFrame."""

import pandas as pd

DEFAULT_MAX_GAP = pd.Timedelta("5min")


def drop_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows, keeping the first."""
    return df.drop_duplicates(keep="first").reset_index(drop=True)


def sort_by_time(df: pd.DataFrame) -> pd.DataFrame:
    """Stable sort by (sensor_id, timestamp)."""
    return df.sort_values(["sensor_id", "timestamp"], kind="stable").reset_index(
        drop=True
    )


def fill_missing(
    df: pd.DataFrame, max_gap: pd.Timedelta = DEFAULT_MAX_GAP
) -> pd.DataFrame:
    """Time-interpolate NaN values when the surrounding valid gap <= max_gap."""
    out = df.copy().reset_index(drop=True)
    for _, idx in out.groupby("sensor_id").groups.items():
        sub = out.loc[idx].sort_values("timestamp", kind="stable")
        ts = sub["timestamp"]
        vals = sub["value"]
        valid_ts = ts.where(vals.notna())
        prev_ts = valid_ts.ffill()
        next_ts = valid_ts.bfill()
        gap = next_ts - prev_ts
        filled = vals.set_axis(ts).interpolate(method="time").set_axis(sub.index)
        ok = vals.isna() & (gap <= max_gap)
        out.loc[sub.index[ok.to_numpy()], "value"] = filled[ok]
    return out
