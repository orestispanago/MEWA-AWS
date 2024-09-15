import requests
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
    resp = requests.post(url, json=body)
    logger.info(f"GET token. Status: {resp.status_code}")
    logger.debug(f"Response text: {resp.text}")
    bearer_token = resp.text
    return bearer_token


def refresh_token():
    bearer_token = get_token()
    with open("token", "w") as f:
        f.write(bearer_token)


with open("token", "r") as f:
    bearer_token = f.read()
