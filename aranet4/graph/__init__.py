import seaborn
seaborn.set()
import pandas
import matplotlib.pyplot as plt

# Import seaborn
import seaborn as sns

# Apply the default theme
# sns.set_theme()
# sns.color_palette("flare", as_cmap=True)
# sns.color_palette("YlOrBr", as_cmap=True)
# sns.color_palette("coolwarm", as_cmap=True)

# Load an example dataset
data = pandas.read_csv("data1.csv", parse_dates=["Time(dd/mm/yyyy)"], dayfirst=True)

annotations = {
    "02/11/2022 13:03:04": "boarding",
}

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

index = data[data["Time(dd/mm/yyyy)"] == "2022-11-04 16:37:59"]["Time(dd/mm/yyyy)"]
value = data[data["Time(dd/mm/yyyy)"] == "2022-11-04 16:37:59"]["Carbon dioxide(ppm)"]

import pdb ; pdb.set_trace()

plt.annotate("boarding", (index, value))

data.set_index("Time(dd/mm/yyyy)", inplace=True)
spot = data.loc["2022-11-04 16:37:59"]

plt.annotate("boarding", (1644613384, 2400))
plt.annotate("boarding", (1667566984, 2400))
x.text(1667566984, 1200, "test")

#data[]


fig = x.get_figure()
fig.savefig("out.png")
