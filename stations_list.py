import requests
import pandas as pd
from authentication import get_token


BEARER_TOKEN = get_token()


def get_stations_list():
    print("Getting stations list...")
    url = "https://app.mewa.gov.sa/wrapi/api/NCM_MEWA/stationsList"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    resp = requests.get(url, headers=headers)
    print(f"GET stations list. Status: {resp.status_code}")
    # print(f"GET stations list. Response text: {resp.text}")
    df = pd.DataFrame.from_dict(resp.json())
    df = pd.json_normalize(df["response"])
    print(f"Retrieved {len(df)} stations.")
    return df


stations = get_stations_list()
stations = stations.rename(columns={'longtuide': 'longitude'})
stations.to_csv("data/stations.csv", index=False)
