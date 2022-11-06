import seaborn
seaborn.set()
import pandas
import matplotlib.pyplot as plt
import numpy
from dateparser import parse

# Import seaborn
import seaborn as sns

# Apply the default theme
# sns.set_theme()
# sns.color_palette("flare", as_cmap=True)
# sns.color_palette("YlOrBr", as_cmap=True)
# sns.color_palette("coolwarm", as_cmap=True)

# Load an example dataset
data = pandas.read_csv("data2.csv", parse_dates=["Time(dd/mm/yyyy)"], dayfirst=True)

data = data[data["Time(dd/mm/yyyy)"] > "2022-11-04 08:23"]

annotations_d = {
#    numpy.datetime64(int(x.timestamp()), 's'): "waiting",
    "2022-11-04 12:30 MDT": "waiting",
    "2022-11-04 13:23 MDT": "boarding",
    "2022-11-04 14:10 MDT": "taking off",
    "2022-11-04 16:00 MDT": "landing",
#    "02/11/2022 13:03:04": "boarding",
}

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
