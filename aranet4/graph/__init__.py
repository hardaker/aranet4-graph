import seaborn as sns
sns.set()
import pandas
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
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: aranet4-graph makeit.yml")

    parser.add_argument("--log-level", "--ll", default="info",
                        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).")

    parser.add_argument("input_file", type=FileType('r'),
                        nargs='?', default=sys.stdin,
                        help="The yaml based config file")

    parser.add_argument("output_file", type=str, default="aranet4.png",
                        help="Where to save the output png")

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level,
                        format="%(levelname)-10s:\t%(message)s")
    return args


def main():
    args = parse_args()
    debug(f"here: {args.input_file}")
    
    content = yaml.load(args.input_file, Loader=yaml.FullLoader)

    debug("here")
    # Apply the default theme
    # sns.set_theme()
    # sns.color_palette("flare", as_cmap=True)
    # sns.color_palette("YlOrBr", as_cmap=True)
    # sns.color_palette("coolwarm", as_cmap=True)

    # Load an example dataset
    data = pandas.read_csv(content["file"],
                           parse_dates=["Time(dd/mm/yyyy)"],
                           dayfirst=True)

    if "begin" in content:
        data = data[data["Time(dd/mm/yyyy)"] > content["begin"]]

    if "end" in content:
        data = data[data["Time(dd/mm/yyyy)"] < content["ent"]]

    

    annotations_d = {
    #    numpy.datetime64(int(x.timestamp()), 's'): "waiting",
        "2022-11-04 12:30 MDT": "waiting",
        "2022-11-04 13:23 MDT": "boarding",
        "2022-11-04 14:10 MDT": "taking off",
        "2022-11-04 16:00 MDT": "landing",
    #    "02/11/2022 13:03:04": "boarding",
    }

    annotations_d = content["markers"]
    annotations = {}
    for timestamp in annotations_d:
        time = parse(timestamp)
        annotations[numpy.datetime64(int(time.timestamp()), 's')] = annotations_d[timestamp]

    #import pdb ; pdb.set_trace()

    # Create a visualization
    x = sns.scatterplot(
        size=2,
        data=data,
        hue="Carbon dioxide(ppm)",
        hue_norm=(400,2500),
        palette="coolwarm",
        x="Time(dd/mm/yyyy)",
        y="Carbon dioxide(ppm)", 
    )

    for annotation in annotations:
        index = data[data["Time(dd/mm/yyyy)"] > annotation]["Time(dd/mm/yyyy)"][:1]
        value = data[data["Time(dd/mm/yyyy)"] > annotation]["Carbon dioxide(ppm)"][:1]

        plt.annotate(annotations[annotation], xy=(index, value), xytext=(index, value+400),
                     arrowprops={'width': 5})

    fig = x.get_figure()
    fig.autofmt_xdate()
    fig.savefig("out.png")


if __name__ == "__main__":
    main()
