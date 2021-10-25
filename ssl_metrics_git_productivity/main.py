import argparse
import json
from pprint import pprint as print

import numpy as np


def get_args():
    ap = argparse.ArgumentParser(
        prog="SSL Metrics Git Productivity",
        usage="Calculates productivity measure of a git project.",
    )
    ap.add_argument("--input", "-i", required=True, type=open, help="...")
    # ap.add_argument("--graph", "-g", type=open, help="...")

    args = ap.parse_args()
    return args


def get_data(filename: str) -> list:
    "returns data from a loc.json file"
    with open(file=filename, mode="r") as file:
        return json.load(file)


def team_effort(data) -> int:
    "returns TE as total elapsed project time"
    return data[len(data) - 1]["day_since_0"]


def module_size(data) -> list:
    "returns a list of delta_loc values"
    return [abs(commit["delta_loc"]) for commit in data]


# # not needed
# def get_hash(data) -> list:
#     return [commit["hash"] for commit in data]
#
# def get_day(data) -> list:
#     return [commit["day_since_0"] for commit in data]


def productivity(MS: list, TE: int) -> list:
    "calculates prod = (MS as delta loc) / TE"
    return [float(loc / TE) for loc in MS]


def authors(data: list) -> set:
    "returns all known authors of a repo"
    return set([item["author_email"] for item in data])

def write(data: list):
    "adds the given field as key value pairs to prod.json"

    with open(file="prod.json", mode="w") as file:
        json.dump(data, file)


def main():

    # df:DataFrame = pandas.read_json(args.input)
    'df.to_json()'


    args = get_args()
    data = get_data(args.input.name)
    prod = productivity(module_size(data), team_effort(data))

    for item, p in zip(data, prod):
        item["productivity"] = p

    print(len(authors(data)))

    write(data)


if __name__ == "__main__":
    main()

"""
prod per member as {author email, name}
    prod per member graphed on the same chart

graphs of velocity and acceleration of prod
"""
