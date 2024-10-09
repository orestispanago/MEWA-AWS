import pandas as pd
import seaborn as sns
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.pyplot as plt

SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 42


def plot_scatter_map(df, fname="plots/scatter_map_station_types.png"):
    reader = Reader("shapefiles/gadm41_SAU_1.shp")
    projection = ccrs.Mercator()
    plt.figure(figsize=(6, 4))
    plt.rc("font", size=MEDIUM_SIZE)
    ax = plt.axes(projection=projection)
    shape_feature = ShapelyFeature(
        reader.geometries(), projection, facecolor="none"
    )
    ax.add_feature(shape_feature)
    sns.scatterplot(
        data=df, y="latitude", x="longitude", hue="stationType", ax=ax
    )
    ax.legend(bbox_to_anchor=(1, 1.02), loc="upper left")
    plt.title("MEWA AWS")
    plt.tight_layout()
    plt.savefig(fname)
    plt.show()
   
def plot_pie(df):
    plt.figure(figsize=(6, 4))
    plt.rc("font", size=MEDIUM_SIZE)
    data = df["stationType"].value_counts()
    ax = data.plot(
        kind="pie",
        autopct=lambda p: "{:.2f}% \n ({:,.0f})".format(p, p * sum(data) / 100),
        # autopct='%1.1f%%',
        shadow=True,
        explode=[0.05, 0.05],
        legend=True,
        title="MEWA AWS types",
        ylabel="",
        labeldistance=None,
    )
    ax.legend(bbox_to_anchor=(1, 1.02), loc="upper left")
    plt.tight_layout()
    plt.savefig("plots/pie_station_types1.png")
    plt.show()

stations = pd.read_csv("data/stations.csv", index_col="stationCode")
weather = pd.read_csv("data/weather_summary.csv", index_col="station_code")
rain = pd.read_csv("data/rain_summary.csv", index_col="station_code")
rain["stationType"] = "rain"
idx = rain.index.intersection(weather.index)
rain.loc[idx , 'stationType'] = "weather"

unknown_locations = rain.loc[rain["latitude"] == 0]
known_locations = rain.loc[rain["latitude"] != 0]

print(f"Total stations: {len(rain)}")
print(f"Unknown locations: {len(unknown_locations)}")
print(f"Known locations: {len(known_locations)}")


plot_scatter_map(known_locations, fname="plots/scatter_map_station_types1.png")
plot_pie(known_locations)