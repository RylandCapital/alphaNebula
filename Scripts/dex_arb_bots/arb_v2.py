import requests
import time
import datetime as dt
import pandas as pd
import os

from dotenv import load_dotenv

from Scripts.utils.terra.terra_wallet import TerraWallet
from Scripts.logging_config import LOGGING_CONFIG
import logging.config

# ----------------------------------------
# Setup the log and env variables
# ----------------------------------------
load_dotenv()

# Logging INIT
if not os.path.exists("./logs"):
    os.makedirs("logs")

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger_arb = logging.getLogger("arbstrat")


if __name__ == "__main__":

    NEBULA_MK = os.getenv("NEBULA_MK")

    terraWallet = TerraWallet(NEBULA_MK)
    logger.info("Connected to terra wallet {}".format(terraWallet.get_acc_address()))
    logger_arb.info("Connected to terra wallet {}".format(terraWallet.get_acc_address()))
