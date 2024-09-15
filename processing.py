import pandas as pd
import glob

csv_files = glob.glob("data/rain/*.csv")

df_list = []
for fname in csv_files:
    df = pd.read_csv(fname, parse_dates=True, index_col="gdate")
    df_list.append(df)

df_all = pd.concat(df_list)


stations = [x for _, x in df_all.groupby(df_all["stationCode"])]
station_codes = []
summary = pd.DataFrame()

for station in stations:
    station = station.sort_index()
    station_code = station["stationCode"].iloc[0].item()
    station_codes.append(station_code)
    start_date = station.index[0]
    end_date = station.index[-1]
    days_installed = (end_date - start_date).days + 1
    station_summary = {
        "station_code": f"{station_code:04}",
        "s_code": station["sCode"].values[0],
        "longitude": station["longitude"].values[0],
        "latitude": station["latitude"].values[0],
        "start_date": start_date,
        "end_date": end_date,
        "days_installed": days_installed,
        "values": len(station),
        "nan": days_installed - len(station),
    }
    # station.to_csv(f"data/rain_by_stations/rain_{station_code:04}.csv")
    df = pd.DataFrame([station_summary], columns=station_summary.keys())
    summary = pd.concat([summary, df])

summary.to_csv("data/rain_summary.csv", index=False)
