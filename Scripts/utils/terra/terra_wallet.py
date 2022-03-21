from terra_sdk.client.lcd import Wallet
from terra_sdk.core import AccAddress
from terra_sdk.key.mnemonic import MnemonicKey
from typing import List
import os

from Scripts.utils.terra.terra_client import TerraClient


class TerraWallet:
    client: TerraClient
    wallet: Wallet

    def __init__(self, mnemonic: str) -> None:
        self.client = TerraClient(network=os.getenv("TERRA_NETWORK"))
        mk = MnemonicKey(mnemonic=mnemonic)
        self.wallet = self.client.client.wallet(mk)

    def get_acc_address(self) -> AccAddress:
        return self.wallet.key.acc_address

    def send_execute_tx(self, execute_msgs: List) -> str:
        execute_tx = self.wallet.create_and_sign_tx(msgs=execute_msgs, gas_prices="0.15uusd", gas_adjustment="1.4",)
        execute_tx_result = self.client.client.tx.broadcast(execute_tx)
        return execute_tx_result.txhash
