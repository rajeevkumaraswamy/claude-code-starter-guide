"""Cleaning helpers for sensor logs. Each returns a new DataFrame."""

import numpy as np
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


def flag_outliers(
    df: pd.DataFrame, window: int = 7, n_sigmas: float = 3.0
) -> pd.Series:
    """Hampel filter: flag values far from their rolling median, per sensor.

    Returns a bool Series aligned to ``df.index``. NaN values are never flagged.
    """
    flags = pd.Series(False, index=df.index, dtype=bool)
    ordered = df.sort_values("timestamp", kind="stable")
    for _, sub in ordered.groupby("sensor_id"):
        x = sub["value"].to_numpy(dtype=float)
        n = len(x)
        left = window // 2
        right = window - left - 1
        hit = np.zeros(n, dtype=bool)
        for i in range(n):
            if np.isnan(x[i]):
                continue
            win = x[max(0, i - left) : min(n, i + right + 1)]
            win = win[~np.isnan(win)]
            med = np.median(win)
            mad = np.median(np.abs(win - med))
            hit[i] = abs(x[i] - med) > n_sigmas * 1.4826 * mad
        flags.loc[sub.index] = hit
    return flags
