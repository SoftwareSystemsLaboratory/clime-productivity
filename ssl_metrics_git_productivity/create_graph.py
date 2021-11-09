from argparse import ArgumentParser, Namespace
from operator import itemgetter
from os import path
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas
from matplotlib.figure import Figure
from pandas import DataFrame
from sklearn.metrics import r2_score


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
        "--maximum_degree_polynomial",
        help="Estimated maximum degree of polynomial",
        type=int,
        required=False,
        default=15,
    )
    parser.add_argument(
        "-r",
        "--repository_name",
        help="Name of the repository that is being analyzed",
        type=str,
        required=False,
    )
    # parser.add_argument(
    #     "-d",
    #     "--derive",
    #     help="Flag to indicate derivation",
    #     type=open, # ??? what type is a flag argument
    #     required=False,
    # )
    return parser.parse_args()


def _format_window(figure: Figure, unique_days: dict) -> None:

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
    add window option for derivatives
    """

    # window -w
    args = get_argparse()
    if args.window:
        window = [int(x) for x in args.window.split(",")]
        plt.xlim(*window)

        w_dist = window[1] - window[0]
        intervals = [int((w_dist / 10) * i + window[0]) for i in range(11)]
        plt.xticks(intervals, intervals)


def __findBestFitLine(x: list, y: list, maximumDegrees: int) -> tuple:
    "returns the closest fit polynomial within the range of maximum degrees"

    # https://www.w3schools.com/Python/python_ml_polynomial_regression.asp
    data: list = []
    degree: int

    for degree in range(maximumDegrees):
        model: np.poly1d = np.poly1d(np.polyfit(x, y, degree))
        r2Score: np.float64 = r2_score(y, model(x))
        temp: tuple = (r2Score, model)
        data.append(temp)

    return max(data, key=itemgetter(0))


def _graphFigure(
    repositoryName: str,
    xLabel: str,
    yLabel: str,
    title: str,
    x: list,
    y: list,
    maximumDegree: int,
    filename: str
) -> None:

    figure: Figure = plt.figure()
    plt.suptitle(repositoryName)

    # Data
    plt.subplot(2, 2, 1)
    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabel)
    plt.title(title)
    plt.plot(x, y)
    plt.tight_layout()

    # Best Fit
    plt.subplot(2, 2, 2)
    data: tuple = __findBestFitLine(x=x, y=y, maximumDegrees=maximumDegree)
    bfModel: np.poly1d = data[1]
    line: np.ndarray = np.linspace(0, max(x), 100)
    plt.ylabel(ylabel=yLabel)
    plt.xlabel(xlabel=xLabel)
    plt.title("Best Fit Line")
    plt.plot(line, bfModel(line))
    plt.tight_layout()

    "plt.ylim(-0.2)"

    # Velocity of Best Fit
    plt.subplot(2, 2, 3)
    velocityModel = np.polyder(p=bfModel, m=1)
    line: np.ndarray = np.linspace(0, max(x), 100)
    plt.ylabel(ylabel="Velocity Unit")
    plt.xlabel(xlabel=xLabel)
    plt.title("Velocity")
    plt.plot(line, velocityModel(line))
    plt.tight_layout()

    # Acceleration of Best Fit
    plt.subplot(2, 2, 4)
    accelerationModel = np.polyder(p=bfModel, m=2)
    line: np.ndarray = np.linspace(0, max(x), 100)
    plt.ylabel(ylabel="Acceleration Unit")
    plt.xlabel(xlabel=xLabel)
    plt.title("Acceleration")
    plt.plot(line, accelerationModel(line))
    plt.tight_layout()

    figure.savefig("subplot.png")
    figure.clf()


# prod_sum over time where time is spaced by day
def plot(df: DataFrame, args: Namespace) -> None:
    figure: Figure = plt.figure()

    # data extraction
    unique_days = {day: 0 for day in set(df["day_since_0"])}

    for day in unique_days:
        temp = df[df["day_since_0"] == day]
        unique_days[day] = temp.sum(axis=0)["productivity"]

    # if arg.derive:
    #     _format_window(figure, unique_days)
    #
    #     plt.ylabel("Productivity")
    #     plt.xlabel("Days Since First Commit")
    #     plt.title("Daily Productivity Sum Over Time")
    #
    #     plt.plot(unique_days.keys(), unique_days.values())
    #     figure.savefig(args.output)
    #     figure.clf()
    # else:

    "logic ... if -d then derive else do just the regular prod graph"

    _graphFigure(
        repositoryName=args.repository_name,
        xLabel="Days Since First Commit",
        yLabel="Prod",
        title="Productivity",
        x=[key for key in unique_days.keys()],
        y=[val for val in unique_days.values()],
        maximumDegree=args.maximum_degree_polynomial,
        filename: str=args.output,
    )


def main():
    args: Namespace = get_argparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    df: DataFrame = pandas.read_json(args.input)

    plot(df, args)


if __name__ == "__main__":
    main()
