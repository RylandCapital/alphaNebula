from email import message
import requests
import time
import datetime as dt
import pandas as pd
import os

from dotenv import load_dotenv

from Scripts.utils.terra.terra_wallet import TerraWallet
from Scripts.logging_config import LOGGING_CONFIG
import logging.config
import datetime


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

import asyncio
from terra_sdk.client.lcd import AsyncLCDClient
from terra_sdk.key.mnemonic import MnemonicKey


async def process_data(wallet, idx):
    print("Processing", idx, datetime.datetime.now())
    account_number = await wallet.account_number()
    print("Finished", idx, datetime.datetime.now())
    return account_number


async def main():
    NEBULA_MK = os.getenv("NEBULA_MK")

    async with AsyncLCDClient("https://lcd.terra.dev", "columbus-5") as terra:
        messages = []
        wallet = terra.wallet(MnemonicKey(NEBULA_MK))
        for i in range(10):
            messages.append(asyncio.create_task(process_data(wallet, i)))

        output = await asyncio.gather(*messages)
        print(output)

        await terra.session.close()


asyncio.get_event_loop().run_until_complete(main())

# if __name__ == "__main__":

#     NEBULA_MK = os.getenv("NEBULA_MK")

#     terra = TerraWallet(NEBULA_MK)
#     logger.info("Connected to terra wallet {}".format(terra.get_acc_address()))
