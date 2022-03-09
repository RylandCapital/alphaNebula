import os

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.coins import Coins
from terra_sdk.key.mnemonic import MnemonicKey
from dotenv import load_dotenv
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.fee import Fee

load_dotenv()

NEBULA_MK = os.getenv("NEBULA_MK")

terra = LCDClient("https://lcd.terra.dev", "columbus-5")
curr_block = terra.tendermint.block_info()['block']['header']['height']

mk = MnemonicKey(mnemonic=NEBULA_MK)
wallet = terra.wallet(mk)

acc_address = wallet.key.acc_address