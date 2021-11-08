from argparse import ArgumentParser, Namespace

import pandas as pd
from pandas import DataFrame


def get_args() -> Namespace:
    ap:ArgumentParser = ArgumentParser(
        prog="SSL Metrics Git Productivity",
        usage="Calculates productivity metric of a git project.",
        description="Productivity is defined as |ΔLOC| / (Team Effort) where Team Effort is the total elapsed time between commits.",
    )
    ap.add_argument(
        "--input",
        "-i",
        required=True,
        type=open,
        help="JSON file containing data formatted by ssl-metrics-git-commits-loc extract",
    )

    args: Namespace = ap.parse_args()
    return args


def get_prod(df: DataFrame) -> None:
    te: int = df["day_since_0"].max()
    p: DataFrame = df["delta_loc"].apply(lambda x: abs(x) / te)
    print(type(p))
    df["productivity"] = p


def main():
    args = get_args()
    df: DataFrame = pd.read_json(args.input)
    get_prod(df)

    df.to_json("prod.json")

if __name__ == "__main__":
    main()