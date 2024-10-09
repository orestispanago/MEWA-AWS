import logging
import os
from ftplib import FTP, error_perm

logger = logging.getLogger(__name__)


FTP_IP = ""
FTP_USER = ""
FTP_PASSWORD = ""
FTP_DIR = "/MEWA-AWS"


def ftp_mkdir_and_enter(ftp_session, dir_name):
    if dir_name not in ftp_session.nlst():
        ftp_session.mkd(dir_name)
        logger.debug(f"Created FTP directory {dir_name}")
    ftp_session.cwd(dir_name)

def ftp_make_dirs(ftp_session, folder_path):
    for f in folder_path.split("/"):
        ftp_mkdir_and_enter(ftp_session, f)


def ftp_upload_file(ftp_session, local_path, remote_path):
    with open(local_path, "rb") as f:
        ftp_session.storbinary(f"STOR {remote_path}", f)
    logger.info(f"Uploaded {local_path} to {remote_path} at FTP")


def ftp_upload_files_list(local_files):
    with FTP(FTP_IP, FTP_USER, FTP_PASSWORD) as ftp:
        ftp.cwd(FTP_DIR)
        for local_file in local_files:
            path_without_first_dir = os.path.join(*(local_file.split(os.path.sep)[1:]))
            remote_path =path_without_first_dir
            try:
                ftp_upload_file(ftp, local_file, remote_path)
            except error_perm as e:
                if "55" in str(e):
                    ftp_make_dirs(ftp, os.path.dirname(remote_path))
                    ftp.cwd(FTP_DIR)
                    ftp_upload_file(ftp, local_file, remote_path)