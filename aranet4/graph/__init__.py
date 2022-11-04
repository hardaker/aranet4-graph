import seaborn
seaborn.set()
import pandas

# Import seaborn
import seaborn as sns

# Apply the default theme
# sns.set_theme()
# sns.color_palette("flare", as_cmap=True)
# sns.color_palette("YlOrBr", as_cmap=True)
# sns.color_palette("coolwarm", as_cmap=True)

# Load an example dataset
data = pandas.read_csv("data1.csv", parse_dates=["Time(dd/mm/yyyy)"], dayfirst=True)

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
fig = x.get_figure()
fig.savefig("out.png")
