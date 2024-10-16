import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 42


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
    plt.savefig("plots/pie_station_types.png")
    plt.show()


def plot_scatter_map(df):
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
        data=df, y="latitude", x="longtuide", hue="stationType", ax=ax
    )
    ax.legend(bbox_to_anchor=(1, 1.02), loc="upper left")
    plt.title("MEWA AWS")
    plt.tight_layout()
    plt.savefig("plots/scatter_map_station_types.png")
    plt.show()


def plot_scatter_map_values(df):
    reader = Reader("shapefiles/gadm41_SAU_1.shp")
    projection = ccrs.Mercator()
    plt.figure(figsize=(6, 4))
    plt.rc("font", size=MEDIUM_SIZE)
    ax = plt.axes(projection=projection)
    shape_feature = ShapelyFeature(
        reader.geometries(), projection, facecolor="none"
    )
    ax.add_feature(shape_feature)

    plt.scatter(
        df["longitude"], df["latitude"], c=df["values"], cmap="jet", s=12
    )
    clb = plt.colorbar()
    clb.ax.set_title("values")
    plt.title("MEWA Rain stations")
    plt.tight_layout()
    plt.savefig("plots/scatter_map_rain_values.png")
    plt.show()


def plot_hist(
    df, title="MEWA Rain data", fname="plots/rain_stations_years.png"
):
    plt.figure(figsize=(6, 4))
    plt.hist(df["years"], bins=50, edgecolor="k")
    plt.rc("font", size=MEDIUM_SIZE)
    plt.xlabel("Years of data")
    plt.title(title)
    plt.ylabel("Number of stations")
    plt.tight_layout()
    plt.savefig(fname)
    plt.show()


stations = pd.read_csv("data/stations.csv")


stations["stationType"] = stations["stationType"].str.replace(
    "مطر يومي", "Rain"
)
stations["stationType"] = stations["stationType"].str.replace(
    "مناخية شاملة آلية", "Weather"
)

plot_pie(stations)
plot_scatter_map(stations)

summary = pd.read_csv("data/rain_summary.csv", index_col="station_code")

unknown_locations = summary.loc[summary["latitude"] == 0]
known_locations = summary.loc[summary["latitude"] != 0]
known_over_a_year = known_locations.loc[known_locations["years"] > 1]

print("========= Rain =========")
print(f"Total rain stations: {len(summary)}")
print(f"Unknown locations: {len(unknown_locations)}")
print(f"Known locations: {len(known_locations)}")
print(f"Known locations over a year: {len(known_over_a_year)}")

plot_hist(known_over_a_year, title="MEWA rain data > 1 year")

plot_scatter_map_values(known_locations)

weather_summary = pd.read_csv(
    "data/weather_summary.csv", index_col="station_code"
)
weather_over_a_year = weather_summary.loc[weather_summary["years"] > 1]
print("========= Weather =========")
print(f"Total weather stations: {len(weather_summary)}")
print(f"Known locations over a year: {len(weather_over_a_year)}")

plot_hist(
    weather_over_a_year,
    title="MEWA weather data > 1 year",
    fname="plots/weather_stations_years.png",
)
