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

# returns data from a loc.json file
def get_data(filename: str) -> list:
    with open(file=filename, mode="r") as file:
        return json.load(file)


def team_effort(data) -> int:
    return data[len(data) - 1]["day_since_0"]


def module_size(data) -> list:
    return [abs(commit["delta_loc"]) for commit in data]

def get_hash(data) -> list:
    return [commit["hash"] for commit in data]

def get_day(data) -> list:
    return [commit["day_since_0"] for commit in data]


def productivity(MS: list, TE: int) -> list:
    return [float(loc / TE) for loc in MS]


def write(data:list):
    "adds the given field as key value pairs to prod.json"

    with open(file='prod.json', mode="w") as file:
        json.dump(data, file)


def main():

    args = get_args()
    data = get_data(args.jsonfile.name)
    prod = productivity(module_size(data), team_effort(data))
    hash = get_hash(data)
    days = get_day(data)

    '''TODO
    append prod to the data and return whole dataset
    output = [... for ... in zip(prod,data)]
    '''

    output = [{'productivity':p, 'hash':h, 'day_since_0':d} for p,h,d in zip(prod,hash,days)]
    write(output)

if __name__ == "__main__":
    main()

'''
prod per member as {author email, name}
    prod per member graphed on the same chart

graphs of velocity and acceleration of prod
'''
