import seaborn as sns

sns.set()
import pandas
import matplotlib
import matplotlib.pyplot as plt
import numpy
from dateparser import parse
import yaml


"""Graph data file(s) from an aranet4 sensor.  It takes a YAML file as input.  Example:

file: extract.csv
markers:
  "2022-11-04 13:23 MDT": "sample at lounge"
  "2022-11-04 14:13 PDT": "sample somewhere else"

"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys


def parse_args():
    "Parse the command line arguments."
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
        epilog="Exmaple Usage: aranet4-graph makeit.yml",
    )

    parser.add_argument(
        "--log-level",
        "--ll",
        default="info",
        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).",
    )

    parser.add_argument(
        "input_file",
        type=FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="The yaml based config file",
    )

    parser.add_argument(
        "output_file",
        type=str,
        nargs="?",
        default="aranet4.png",
        help="Where to save the output png",
    )

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level, format="%(levelname)-10s:\t%(message)s")
    return args


def main():
    args = parse_args()
    debug(f"here: {args.input_file}")

    content = yaml.load(args.input_file, Loader=yaml.FullLoader)

    matplotlib.use("Agg")  # avoids needing an X terminal
    font = {"size": 16}
    matplotlib.rc("font", **font)

    # Apply the default theme
    # sns.set_theme()
    # sns.color_palette("flare", as_cmap=True)
    # sns.color_palette("YlOrBr", as_cmap=True)
    # sns.color_palette("coolwarm", as_cmap=True)

    # Load an example dataset
    data = pandas.read_csv(
        content["file"], parse_dates=["Time(dd/mm/yyyy)"], dayfirst=True
    )

    if "begin" in content:
        timestamp = numpy.datetime64(int(parse(content["begin"]).timestamp()), "s")
        data = data[data["Time(dd/mm/yyyy)"] > timestamp]

    if "end" in content:
        timestamp = numpy.datetime64(int(parse(content["end"]).timestamp()), "s")
        data = data[data["Time(dd/mm/yyyy)"] < timestamp]

    annotations_d = content["markers"]
    annotations = {}
    for timestamp in annotations_d:
        time = parse(timestamp)
        annotations[numpy.datetime64(int(time.timestamp()), "s")] = annotations_d[
            timestamp
        ]

    # import pdb ; pdb.set_trace()

    # Create a visualization
    x = sns.scatterplot(
        #        size=20,
        data=data,
        hue="Carbon dioxide(ppm)",
        hue_norm=(400, 1400),
        palette="coolwarm",
        x="Time(dd/mm/yyyy)",
        y="Carbon dioxide(ppm)",
    )

    for annotation in annotations:
        index = data[data["Time(dd/mm/yyyy)"] > annotation]["Time(dd/mm/yyyy)"][:1]
        value = data[data["Time(dd/mm/yyyy)"] > annotation]["Carbon dioxide(ppm)"][:1]

        plt.annotate(
            annotations[annotation],
            xy=(index, value),
            xytext=(index, value + 400),
            arrowprops={"width": 5},
        )

    plt.xlabel("")  # don't use the column title -- label is obvious
    fig = x.get_figure()
    fig.autofmt_xdate()
    plt.tight_layout()
    fig.set_dpi(100)
    fig.set_size_inches(16, 9)
    fig.savefig(args.output_file)
    info(f"saved: {args.output_file}")


if __name__ == "__main__":
    main()
