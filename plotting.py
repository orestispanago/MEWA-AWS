import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 42


df = pd.read_csv("data/stations.csv")


df["stationType"] = df["stationType"].str.replace("مطر يومي", "Rain")
df["stationType"] = df["stationType"].str.replace(
    "مناخية شاملة آلية", "Weather"
)


def plot_pie():
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


# plot_pie()


def plot_scatter_map():
    reader = Reader("gadm41_SAU_shp/gadm41_SAU_1.shp")
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
    plt.savefig("plots/scatter_map_station_types")
    plt.show()


plot_scatter_map()


def plot_scatter_map_values(df):
    reader = Reader("gadm41_SAU_shp/gadm41_SAU_1.shp")
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
    plt.savefig("plots/scatter_map_rain_values")
    plt.show()


summary = pd.read_csv("data/rain_summary.csv", index_col="station_code")
# summary = summary.loc[summary["values"]>5*365]


unknown_locations = summary.loc[summary["latitude"] == 0]
known_locations = summary.loc[summary["latitude"] != 0]

print(f"Known locations: {len(known_locations)}")
print(f"Unknown locations: {len(unknown_locations)}")
plot_scatter_map_values(known_locations)
