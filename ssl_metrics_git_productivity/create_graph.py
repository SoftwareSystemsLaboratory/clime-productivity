from argparse import ArgumentParser, Namespace
from os import path
from pprint import pprint

import matplotlib.pyplot as plt
import pandas
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
    parser.add_argument(
        "-m",
        "--maximum-degree-polynomial",
        help="Estimated maximum degree of polynomial",
        type=int,
        required=False,
        default=15,
    )
    return parser.parse_args()


def _format_window(figure: Figure) -> None:

    # xticks / xlim
    max_tick = int(max(unique_days.keys()) + 10 / 10)
    step = int(max_tick / 10)
    intervals = [i for i in range(0, max_tick + step, step)]
    plt.xticks(intervals, intervals)
    plt.xlim([-1, max((unique_days.keys())) + 1])

    # yticks / ylim?
    plt.ylim(-1, max([day for day in unique_days.values()]) * 1.1)

    """TODO
    fix windows in relation to xticks, yticks
    """

    # window -w
    args = get_argparse()
    if args.window:
        window = [int(x) for x in args.window.split(",")]
        plt.xlim(*window)

        w_dist = window[1] - window[0]
        intervals = [int((w_dist / 10) * i + window[0]) for i in range(11)]
        plt.xticks(intervals, intervals)


# prod_sum over time where time is spaced by day
def plot(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()

    # data extraction
    unique_days = {day: 0 for day in set(df["day_since_0"])}

    for day in unique_days:
        temp = df[df["day_since_0"] == day]
        unique_days[day] = temp.sum(axis=0)["productivity"]

    _format_window(figure)

    plt.ylabel("Productivity")
    plt.xlabel("Days Since First Commit")
    plt.title("Daily Productivity Sum Over Time")

    plt.plot(unique_days.keys(), unique_days.values())
    figure.savefig(filename)

    """TODO
    could be organized much more efficiently
    try in future
        graphing straight from df
    using separate dicts so that you dont have to iterate as many times
    """


def main():
    args: Namespace = get_argparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    df: DataFrame = pandas.read_json(args.input)

    plot(df, filename=args.output)


if __name__ == "__main__":
    main()
