import glob
from uploaders import ftp_upload_files_list
import rain
import weather
import logging
import logging.config
import os
import traceback
from logging.handlers import RotatingFileHandler


os.chdir(os.path.dirname(os.path.abspath(__file__)))

logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s]  %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    handlers=[
        RotatingFileHandler(
            "logs/logfile.log", maxBytes=10 * 1024 * 1042, backupCount=5
        ),
        logging.StreamHandler(),
    ],
)


def archive_except_last(local_files):
    if len(local_files) > 1:
        for local_file in sorted(local_files[:-1]):
            dest_path = local_file.replace("data", "data/archive")
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            os.rename(local_file, dest_path)
            logger.info(f"Renamed local file {local_file} to {dest_path}")


def main():
    logger.debug(f"{'-' * 15} RAIN TASK {'-' * 15}")
    rain.download_months()
    rain_files = glob.glob("data/rain/*.csv")
    ftp_upload_files_list(rain_files)
    archive_except_last(rain_files)

    logger.debug(f"{'-' * 15} WEATHER TASK {'-' * 15}")
    weather.download_till_yesterday()
    weather_files = glob.glob("data/weather/*/*.csv")
    ftp_upload_files_list(weather_files)
    archive_except_last(weather_files)

    logger.debug(f"{'-' * 15} SUCCESS {'-' * 15}")


if __name__ == "__main__":
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
