"""Generate practice/data/sample.csv and practice/data/messy.csv.

Run from the practice/ directory so the practice environment is used:
    cd practice && uv run python ../tools/make_data.py
Deterministic and idempotent.
"""

from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "practice" / "data"
START = pd.Timestamp("2026-01-01T00:00:00Z")
N = 120  # 2 hours at 1-minute spacing


def make_clean(rng: np.random.Generator) -> pd.DataFrame:
    times = START + pd.to_timedelta(np.arange(N), unit="min")
    t = np.arange(N)
    series = {
        "temp_1": 21.0 + 0.5 * np.sin(t / 20) + rng.normal(0, 0.1, N),
        "temp_2": 19.5 + 0.4 * np.cos(t / 25) + rng.normal(0, 0.1, N),
        "pressure_1": 101.3 + rng.normal(0, 0.2, N),
    }
    frames = [
        pd.DataFrame({"timestamp": times, "sensor_id": sid, "value": vals.round(3)})
        for sid, vals in series.items()
    ]
    df = pd.concat(frames, ignore_index=True)
    return df.sort_values(["timestamp", "sensor_id"], kind="stable").reset_index(
        drop=True
    )


def make_messy(clean: pd.DataFrame) -> pd.DataFrame:
    df = clean.copy()
    # 15-minute gap in temp_2 (drop 15 consecutive samples)
    gap_start = START + pd.Timedelta(minutes=50)
    gap_end = gap_start + pd.Timedelta(minutes=15)
    in_gap = (
        (df.sensor_id == "temp_2")
        & (df.timestamp >= gap_start)
        & (df.timestamp < gap_end)
    )
    df = df[~in_gap].reset_index(drop=True)
    # spike: 10x the median in pressure_1
    p = df.sensor_id == "pressure_1"
    spike_idx = df.index[p][80]
    df.loc[spike_idx, "value"] = round(10 * df.loc[p, "value"].median(), 3)
    # 3 isolated NaNs (non-adjacent, away from spike/gap)
    for i in (
        df.index[df.sensor_id == "temp_1"][20],
        df.index[df.sensor_id == "temp_2"][100],
        df.index[df.sensor_id == "pressure_1"][40],
    ):
        df.loc[i, "value"] = np.nan
    # 10 out-of-order rows: swap 5 disjoint pairs of consecutive same-sensor rows
    swaps = [
        ("temp_1", 5),
        ("temp_1", 70),
        ("temp_2", 10),
        ("temp_2", 90),
        ("pressure_1", 60),
    ]
    for sid, k in swaps:
        i, j = df.index[df.sensor_id == sid][[k, k + 1]]
        df.iloc[[i, j]] = df.iloc[[j, i]].to_numpy()
    # 5 exact duplicates, inserted right after the originals (never NaN rows)
    dup_positions = [11, 64, 125, 183, 305]
    assert not df.iloc[dup_positions].value.isna().any()
    parts, prev = [], 0
    for pos in dup_positions:
        parts.append(df.iloc[prev : pos + 1])
        parts.append(df.iloc[[pos]])
        prev = pos + 1
    parts.append(df.iloc[prev:])
    return pd.concat(parts, ignore_index=True)


def main() -> None:
    rng = np.random.default_rng(42)
    clean = make_clean(rng)
    messy = make_messy(clean)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, df in (("sample.csv", clean), ("messy.csv", messy)):
        out = df.copy()
        out["timestamp"] = out["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        out.to_csv(OUT / name, index=False)


if __name__ == "__main__":
    main()
