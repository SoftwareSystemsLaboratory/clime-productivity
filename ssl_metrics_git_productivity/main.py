"""takes a loc file as an argument ...
returns a prod file with calculated productivity"""

import argparse

import numpy as np
import pandas as pd
from pandas import DataFrame


def get_args():
    ap = argparse.ArgumentParser(
        prog="SSL Metrics Git Productivity",
        usage="Calculates productivity measure of a git project.",
    )
    ap.add_argument("--input", "-i", required=True, type=open, help="...",)

    args = ap.parse_args()
    return args


def get_prod(df: DataFrame):
    te = df["day_since_0"].max()
    p = df["delta_loc"].apply(lambda x: abs(x) / te)
    df["productivity"] = p


<<<<<<< HEAD
def get_velocity(df: DataFrame):
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


=======
>>>>>>> 09a32f644aa1a0e9e628d92c9d4b150e03c45dc7
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
