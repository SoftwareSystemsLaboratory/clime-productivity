from argparse import ArgumentParser, Namespace
from operator import itemgetter
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas
from matplotlib.figure import Figure
from pandas import DataFrame
from sklearn.metrics import r2_score


def getArgparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="ssl-metrics-git-bus-factor Graph Generator",
        usage="This is a proof of concept demonstrating that it is possible to use git to compute the bus factor of a project.",
        description="The only required arguement of this program is -i/--input. The default action is to do nothing until a filename for the graph is inputted."
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
        help="The filename to output the bus factor graph to",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-m",
        "--maximum-degree-polynomial",
        help="Estimated maximum degree of polynomial",
        type=int,
        required=False,
        default=15
    )
    parser.add_argument(
        "-r",
        "--repository-name",
        help="Name of the repository that is being analyzed",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--x-window-min",
        help="The smallest x value that will be plotted",
        type=int,
        required=False,
        default=0
    )
    parser.add_argument(
        "--x-window-max",
        help="The largest x value that will be plotted",
        type=int,
        required=False,
        default=-1
    )
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
    filename: str,
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

    figure.savefig(filename)
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

    _graphFigure(
        repositoryName=args.repository_name,
        xLabel="Days Since First Commit",
        yLabel="Prod",
        title="Productivity",
        x=[key for key in unique_days.keys()],
        y=[val for val in unique_days.values()],
        maximumDegree=args.maximum_degree_polynomial,
        filename=args.output,
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
