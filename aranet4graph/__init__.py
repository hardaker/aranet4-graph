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

    # find where to save the output PNG to
    output_file = args.output_file
    if not output_file:
        output_file = content.get("output")

    if not output_file:
        error(
            f"neither 'output_file' was given or an 'output' key in '{args.input_file.name}' was supplied"
        )
        exit(1)

    # bootstrap matplotlib lib fonts/size
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
        content["input"], parse_dates=["Time(dd/mm/yyyy)"], dayfirst=True
    )

    if "begin" in content:
        timestamp = numpy.datetime64(int(parse(content["begin"]).timestamp()), "s")
        data = data[data["Time(dd/mm/yyyy)"] > timestamp]

    if "end" in content:
        timestamp = numpy.datetime64(int(parse(content["end"]).timestamp()), "s")
        data = data[data["Time(dd/mm/yyyy)"] < timestamp]

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

    # if markers are specified, create all the needed data for it
    annotations = {}
    if "markers" in content:
        annotations_d = content["markers"]
        for timestamp in annotations_d:

            # turn their date string into a raw epoch int
            time = parse(timestamp)
            time_d64 = numpy.datetime64(int(time.timestamp()), "s")

            # extract the value
            value = annotations_d[timestamp]

            # turn a raw string into a dict
            if isinstance(value, str):
                value = {"label": value}

            annotations[time_d64] = value

    for annotation in annotations:
        # pull the next recorded timestamp *after* the annotation stamp
        index = data[data["Time(dd/mm/yyyy)"] > annotation]["Time(dd/mm/yyyy)"][:1]
        # and the value
        value = data[data["Time(dd/mm/yyyy)"] > annotation]["Carbon dioxide(ppm)"][:1]

        # default vertical offset of 400
        vertical_offset = annotations[annotation].get("offset", 400)

        # info(index)
        # info(type(index))
        # import pdb ; pdb.set_trace()
        plt.annotate(
            annotations[annotation]["label"],
            xy=(index, value),
            xytext=(index, value + vertical_offset),
            arrowprops={"width": 5},
        )

    plt.xlabel("")  # don't use the column title -- label is obvious
    fig = x.get_figure()
    fig.autofmt_xdate()
    #    plt.tight_layout()
    fig.set_dpi(100)
    fig.set_size_inches(16, 9)

    fig.savefig(output_file)
    info(f"saved: {output_file}")


if __name__ == "__main__":
    main()
