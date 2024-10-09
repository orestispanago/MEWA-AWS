import requests
import pandas as pd
from json import JSONDecodeError
import logging
import datetime
from dateutil.relativedelta import relativedelta
import glob
import os
from authentication import get_token
from requests.adapters import HTTPAdapter, Retry



logger = logging.getLogger(__name__)



def get_rain(bearer_token,
    start_date="1953-09-01T00:00:00.000Z", end_date="1953-09-30T00:00:00.000Z"
):
    logger.debug(f"Getting rain records from {start_date} to {end_date}...")
    session = requests.Session()
    retries = Retry(
        total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
    )
    url = "https://app.mewa.gov.sa/wrapi/api/NCM_MEWA/rainfallrecords"
    session.mount(url, HTTPAdapter(max_retries=retries))
    headers = {"Authorization": f"Bearer {bearer_token}"}
    body = {"from": start_date, "to": end_date}
    resp = session.post(url, headers=headers, json=body, timeout=60)
    logger.debug(f"POST rainfall records. Status: {resp.status_code}")
    df = pd.DataFrame.from_dict(resp.json())
    logger.debug(f"Retrieved {len(df)} rainfall records.")
    return df


def get_start_month():
    first_month = "1953-09"
    csv_files = glob.glob("data/rain/*.csv")
    if csv_files:
        last_csv_file = sorted(csv_files)[-1]
        logger.info(f"Last monthly file: {last_csv_file}")
        base_name = os.path.basename(last_csv_file)
        year_month = base_name.split("/")[-1].split("_")[-1].split(".")[0]
        first_month = year_month[:4] + "-" + year_month[4:]
    else:
        logger.info("No csv files found. Using: {first_month}")
    return first_month


def download_months():
    utc_now = datetime.datetime.now(datetime.UTC)
    next_month = utc_now.replace(tzinfo=None).date() + relativedelta(months=1)
    first_weather_month = get_start_month()
    month_starts = pd.date_range(first_weather_month, next_month, freq="MS")
    month_ends = pd.date_range(first_weather_month, next_month, freq="ME")
    for ms, me in zip(month_starts, month_ends):
        start_date = ms.strftime("%Y-%m-%dT00:00:00.000Z")
        end_date = me.strftime("%Y-%m-%dT00:00:00.000Z")
        try:
            bearer_token = get_token()
            df = get_rain(bearer_token, start_date=start_date, end_date=end_date)
        except JSONDecodeError as e:
            if "Expecting value" in str(e):
                bearer_token = get_token()
                df = get_rain(bearer_token, start_date=start_date, end_date=end_date)
            else:
                logger.error(e)
        if len(df) != 0:
            fname = f"data/rain/rain_{ms.strftime('%Y')}{me.strftime('%m')}.csv"
            df.to_csv(fname, index=False)
            logger.info(f"Stored {len(df)} records at {fname}.")
        else:
            logger.info("No data from {ms} to {me}.")