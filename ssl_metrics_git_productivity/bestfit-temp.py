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
) -> None:

    figure: Figure = plt.figure()
    plt.suptitle("subtitle")

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

    figure.savefig("prod.png")
    figure.clf()


def plot(
    x: list,
    y: list,
    xLabel: str,
    yLabel: str,
    title: str,
    maximumDegree: int,
    repositoryName: str,
    filename: str,
) -> tuple:
    _graphFigure(
        repositoryName=repositoryName,
        xLabel=xLabel,
        yLabel=yLabel,
        title=title,
        x=x,
        y=y,
        maximumDegree=maximumDegree,
        filename=filename,
    )
    return (x, y)
