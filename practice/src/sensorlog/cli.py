"""Command-line interface: ``sensorlog summary <csv>``."""

import argparse
import sys
from pathlib import Path

from sensorlog.load import load_csv
from sensorlog.stats import summarize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sensorlog")
    sub = parser.add_subparsers(dest="command", required=True)
    summary = sub.add_parser("summary", help="print per-sensor statistics")
    summary.add_argument("csv", type=Path)
    args = parser.parse_args(argv)

    if not args.csv.is_file():
        print(f"error: file not found: {args.csv}", file=sys.stderr)
        return 2
    stats = summarize(load_csv(args.csv))
    for sensor_id in sorted(stats):
        s = stats[sensor_id]
        print(
            f"{sensor_id}: count={s['count']} mean={s['mean']:.3f} "
            f"min={s['min']:.3f} max={s['max']:.3f}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
