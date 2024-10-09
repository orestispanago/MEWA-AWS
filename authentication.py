import requests
from requests.adapters import HTTPAdapter, Retry
import logging

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


USERNAME = ""
PASSWORD = ""


def get_token():
    logger.debug("Getting token...")
    url = "https://app.mewa.gov.sa/wrapi/api/Authentication/signIn"
    body = {"USERNAME": USERNAME, "PASSWORD": PASSWORD}
    session = requests.Session()
    retries = Retry(
        total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504, 104]
    )
    session.mount(url, HTTPAdapter(max_retries=retries))
    resp = session.post(url, json=body, timeout=10)
    logger.info(f"GET token. Status: {resp.status_code}")
    # logger.debug(f"Response text: {resp.text}")
    bearer_token = resp.text
    with open("token", "w") as f:
        f.write(bearer_token)
    return bearer_token
