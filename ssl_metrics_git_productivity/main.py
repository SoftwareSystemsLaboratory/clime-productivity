from argparse import ArgumentParser, Namespace

import pandas as pd
from pandas import DataFrame
from pandas.core.series import Series


def get_args() -> Namespace:
    ap: ArgumentParser = ArgumentParser(
        prog="SSL Metrics Git Productivity Computer",
        usage="Calculates productivity metric of a git project.",
        description="Productivity is defined as |ΔLOC| / (Team Effort) where Team Effort is the total elapsed time between commits.",
    )
    ap.add_argument(
        "-i",
        "--input",
        required=True,
        type=open,
        help="JSON file containing data formatted by ssl-metrics-git-commits-loc extract",
    )
    ap.add_argument(
        "-o",
        "--output",
        required=True,
        type=open,
        help="JSON file containing data outputted by the application",
    )

    args: Namespace = ap.parse_args()
    return args


def get_prod(df: DataFrame) -> None:
    te: int = df["day_since_0"].max()
    p: Series = df["delta_loc"].apply(lambda x: abs(x) / te)
    print(type(p))
    df["productivity"] = p


def main():
    args = get_args()

    if args.input[-5:] != ".json":
        print("Input must be a .json file")
        quit(1)

    df: DataFrame = pd.read_json(args.input)
    get_prod(df)

    df.to_json(args.output)

if __name__ == "__main__":
    main()
