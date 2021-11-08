"""takes a loc file as an argument ...
returns a prod file with calculated productivity"""

import argparse
import json
from pprint import pprint as print

import numpy as np
import pandas as pd
from pandas import DataFrame


def get_args():
    ap = argparse.ArgumentParser(
        prog="SSL Metrics Git Productivity",
        usage="Calculates productivity measure of a git project.",
    )
    ap.add_argument("--input", "-i", required=True, type=open, help="...")
    # ap.add_argument("--graph", "-g", type=open, help="...")

    args = ap.parse_args()
    return args


def get_prod(df: DataFrame):
    """returns the productivity of each commit as
    prod = module_size / team effort
    prod = delta_loc / elapsed time
    """

    te = df["day_since_0"].max()

    "calculates module_size as the absolute value of delta_loc"
    p = df["delta_loc"].apply(lambda x: abs(x) / te)

    df["productivity"] = p


def main():

    args = get_args()

    df: DataFrame = pd.read_json(args.input)
    get_prod(df)
    get_velocity(df)

    "transpose to look pretty"
    "dont transpose to be effective"
    df.to_json("prod.json")
    # df.T.to_json("prod.json")

    output = [{'productivity':p, 'hash':h, 'day_since_0':d} for p,h,d in zip(prod,hash,days)]
    write(output)

if __name__ == "__main__":
    main()

""" TODO
prod per member as {author email, name}
    prod per member graphed on the same chart

graphs of acceleration of prod
"""
