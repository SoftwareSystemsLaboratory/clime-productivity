from argparse import ArgumentParser, Namespace
from os import path

import matplotlib.pyplot as plt
import pandas
from pprint import pprint
from matplotlib.figure import Figure
from pandas import DataFrame


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Convert Output",
        usage="This program converts a JSON file into various different formats.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input data file that will be read to create the graphs",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The filename to output the graph to",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-w",
        "--window",
        help="the window of days to be graphed: denoted x1,x2",
        type=str,
        required=False,
    )
    return parser.parse_args()


# prod_sum over time where time is spaced by day
def plot(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()

    # data extraction

    days = set(df["day_since_0"])
    unique_days = {day: 0 for day in days}

    unique_days = {day: {"prod": 0, "velocity": 0} for day in days}

    for day in unique_days:
        temp = df[df["day_since_0"] == day]
        unique_days[day]["prod"] = temp["productivity"].sum()
        unique_days[day]["velocity"] = temp["velocity"].max()

    # xticks
    max_tick = int(max(unique_days.keys()) + 10 / 10)
    step = int(max_tick / 10)
    intervals = [i for i in range(0, max_tick + step, step)]

    plt.xticks(intervals, intervals)

    '''TODO
    fix windows in relation to xticks, yticks'''

    # formatting
    plt.xlim([-1, max((unique_days.keys())) + 1])
    args = get_argparse()
    if args.window:
        window = [int(x) for x in args.window.split(",")]
        plt.xlim(*window)

        w_dist = window[1] - window[0]
        intervals = [int((w_dist/10)*i + window[0]) for i in range(11)]
        plt.xticks(intervals, intervals)

    '''TODO
    store prod sum (calculated already) in main
    1 is a placeholder for velocity max, but one velocity value is inf
    prod will never be negative
    '''
    plt.ylim([df['velocity'].min()*1.1, max(max([day['prod'] for day in unique_days.values()]) , df['velocity'].max()) * 1.1])

    plt.ylabel("Productivity")
    plt.xlabel("Days Since First Commit")
    plt.title("Daily Productivity Sum Over Time")

    plt.plot(unique_days.keys(), [day['prod'] for day in unique_days.values()], linewidth=3)
    plt.plot(unique_days.keys(), [day['velocity'] for day in unique_days.values()], color='red', linewidth=0.75)

    figure.savefig(filename)

    '''TODO
    could be organized much more efficiently
    try in future
        graphing straight from df
    using separate dicts so that you dont have to iterate as many times
    '''

    '''TODO
    the graphs should depict velocity = 0 when prod is at a peak
    how to achieve??
    regression modeling?
    '''


def main():
    args: Namespace = get_argparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    df: DataFrame = pandas.read_json(args.input)

    plot(df, filename=args.output)


if __name__ == "__main__":
    main()
