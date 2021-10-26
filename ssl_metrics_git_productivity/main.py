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


def get_velocity(df: DataFrame):
    """returns the velocity of prod as
    change in prod over change in time
    calculates the sum of prod per dat since there are no hourly timestamps
    """

    daily_prod = []
    delta_prod = []
    prod_t1 = 0

    delta_time = []
    day_t1 = 0

    "does days need to be sorted??"
    days = set(df["day_since_0"])

    for day in days:
        temp = df[df["day_since_0"] == day]
        prod = temp["productivity"].sum()

        delta_prod += [prod - prod_t1 for i in range(len(temp.T.columns))]
        prod_t1 = prod

        delta_time += [day - day_t1 for i in range(len(temp.T.columns))]
        day_t1 = day

    df["delta_prod"] = delta_prod
    df["delta_time"] = delta_time

    df["velocity"] = df["delta_prod"] / df["delta_time"]

    """
    calculations:
        daily prod
        change in prod
        change in time
        dprod / dtime

        velocity = daily velocity
        dvelocity
        dvelocity / dtime
    """


def main():

    args = get_args()

    df: DataFrame = pd.read_json(args.input)
    get_prod(df)
    get_velocity(df)

    "transpose to look pretty"
    "dont transpose to be effective"
    df.to_json("prod.json")
    # df.T.to_json("prod.json")


if __name__ == "__main__":
    main()

""" TODO
prod per member as {author email, name}
    prod per member graphed on the same chart

graphs of acceleration of prod
"""
