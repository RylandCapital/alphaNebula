import os

from dotenv import load_dotenv

from Scripts.logging_config import LOGGING_CONFIG
import logging.config
import datetime

import asyncio
from terra_sdk.client.lcd import AsyncLCDClient, AsyncWallet
from terra_sdk.core.tx import Tx
from terra_sdk.key.mnemonic import MnemonicKey
from Scripts.utils.terra.terra_client import TerraNetwork
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.wasm import MsgExecuteContract
from terra_sdk.core.fee import Fee
from terra_sdk.core.bank import MsgSend


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


class StrategyExecutor:
    def __init__(self, stratName, network, mneumonic):
        self.stratName = stratName
        self.transactions = []
        self.transactionOutput = []
        self.stratId = 0
        self.network = TerraNetwork[network]
        self.terra_client = AsyncLCDClient(
            chain_id=self.network.value,
            url="https://lcd.terra.dev"
            if self.network == TerraNetwork.MAINNET
            else "https://bombay-lcd.terra.dev",
        )
        self.terra = self.terra_client.wallet(MnemonicKey(mneumonic))

    async def _addTransaction(self, msgs, memo, fee):
        # Run before transaction
        time_start = datetime.datetime.now()

        # Actual Transaction
        tx = await self.terra.create_and_sign_tx(
            CreateTxOptions(msgs=msgs, gas_prices="0.15uusd", memo=memo, fee=fee)
        )
        output = await self.terra_client.tx.broadcast_sync(tx)

        # Post transaction
        status = output.is_tx_error()
        txhash = output.txhash
        time_end = datetime.datetime.now()

        return {
            "txhash": txhash,
            # "time_start": time_start,
            # "tx": tx,
            # "output": output,
            "status": status,
            # "time_end": time_end,
        }

    def addTransaction(self, msgs, memo, fee):
        self.transactions.append(asyncio.create_task(self._addTransaction(msgs, memo, fee)))

    async def waitAllTransactions(self):
        self.transactionOutput = await asyncio.gather(*self.transactions)

    async def close(self):
        print("Closing all connections")
        self.terra.session.close()


async def process_data(wallet, idx):
    print("Processing", idx, datetime.datetime.now())
    account_number = await wallet.account_number()
    print("Finished", idx, datetime.datetime.now())
    return account_number


async def main():
    NEBULA_MK = os.getenv("NEBULA_MK")
    TERRA_NETWORK = os.getenv("TERRA_NETWORK")
    print("TERRA_NETWORK", TERRA_NETWORK)
    strategy = StrategyExecutor("Test strat", TERRA_NETWORK, NEBULA_MK)

    print("With acocunt", strategy.terra.key.acc_address)

    for i in range(10):
        print("Adding transaction", i)
        memo = "test transaction!"
        fee = Fee(200000, "120000uluna")
        msgs = [
            MsgSend(
                strategy.terra.key.acc_address,
                "terra15n6xtt0j6zpvfc0eeu7jldzllnjzftcs7ldhyj",
                "120001uluna",
            )
        ]
        strategy.addTransaction(msgs, memo, fee)

    print("Waiting all transactions")
    await strategy.waitAllTransactions()

    for i in range(10):
        print(i, strategy.transactionOutput[i])

    await strategy.close()

    # async with AsyncLCDClient("https://lcd.terra.dev", "columbus-5") as terra:
    #     messages = []
    #     wallet = terra.wallet(MnemonicKey(NEBULA_MK))
    #     for i in range(10):
    #         messages.append(asyncio.create_task(process_data(wallet, i)))

    #     output = await asyncio.gather(*messages)
    #     print(output)

    #     await terra.session.close()


asyncio.get_event_loop().run_until_complete(main())

# if __name__ == "__main__":

#     NEBULA_MK = os.getenv("NEBULA_MK")

#     terra = TerraWallet(NEBULA_MK)
#     logger.info("Connected to terra wallet {}".format(terra.get_acc_address()))
