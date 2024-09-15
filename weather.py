import requests
import pandas as pd
import os
import glob
from json import JSONDecodeError
import logging
from authentication import bearer_token, refresh_token
import datetime
from requests.adapters import HTTPAdapter, Retry


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def format_weather_response(df):
    stations_df_list = []
    for col in list(df)[6:]:
        station = pd.DataFrame.from_dict(df[col][0])
        stations_df_list.append(station)
    stations = pd.concat(stations_df_list, axis=0)
    return stations


def get_weather(
    start_date="1964-01-01T00:00:00.000Z", end_date="1964-01-01T00:00:00.000Z"
):
    logger.debug(f"Getting weather records from {start_date} to {end_date}...")
    session = requests.Session()
    retries = Retry(
        total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
    )
    url = "https://app.mewa.gov.sa/wrapi/api/NCM_MEWA/ClimateRecords"
    session.mount(url, HTTPAdapter(max_retries=retries))
    headers = {"Authorization": f"Bearer {bearer_token}"}
    body = {"from": start_date, "to": end_date}
    resp = session.post(url, json=body, headers=headers, timeout=20)
    logger.debug(f"POST weather records. Status: {resp.status_code}")
    df = pd.json_normalize(resp.json())
    stations = format_weather_response(df)
    logger.debug(f"Retrieved {len(stations)} weather records.")
    return stations


def get_start_date():
    start_date = "1964-01-01T00:00:00.000Z"
    csv_files = glob.glob("data/weather/*/*.csv")
    if csv_files:
        last_csv_file = sorted(csv_files)[-1]
        logger.info(f"Last monthly file: {last_csv_file}")
        base_name = os.path.basename(last_csv_file)
        date_str = base_name.split("/")[-1].split("_")[-1].split(".")[0]
        date = datetime.datetime.strptime(date_str, "%Y%m%d")
        start_date = date.strftime("%Y-%m-%dT00:00:00.000Z")
    else:
        logger.info("No csv files found. Using: {start_date}")
    return start_date


def download_weather_days():
    utc_now = datetime.datetime.now(datetime.UTC)
    start_date = get_start_date()
    dates = pd.date_range(start_date, utc_now)
    for date in dates:
        date_str = date.strftime("%Y-%m-%dT00:00:00.000Z")
        try:
            df = get_weather(start_date=date_str, end_date=date_str)
        except JSONDecodeError as e:
            if "Expecting value" in str(e):
                refresh_token()
                df = get_weather(start_date=date_str, end_date=date_str)
            else:
                logger.error(e)
        if len(df) != 0:
            folder = f"data/weather/{date.strftime('%Y')}"
            os.makedirs(folder, exist_ok=True)
            fname = f"{folder}/weather_{date.strftime('%Y%m%d')}.csv"
            df.to_csv(fname, index=False)
            logger.info(f"Stored {len(df)} records at {fname}.")
        else:
            logger.info(f"No data for {start_date}.")


download_weather_days()
