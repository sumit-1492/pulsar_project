import logging
import os,sys
from datetime_1 import datetime

root_dir = os.getcwd()
LOG_DIR = "pulsarlogs"
LOG_DIR = os.path.join(root_dir,LOG_DIR)

os.makedirs(LOG_DIR,exist_ok=True)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}"
file_name = f"log_{CURRENT_TIME_STAMP}.log"


log_file_path = os.path.join(LOG_DIR, file_name)


logging.basicConfig(
                    format="[%(asctime)s: %(levelname)s: %(module)s: %(message)s]",
                    datefmt= "%d-%m-%Y %H:%M:%S" ,
                    handlers=[logging.FileHandler(log_file_path),
                    logging.StreamHandler(sys.stdout)],
                    level=logging.INFO
                    )

