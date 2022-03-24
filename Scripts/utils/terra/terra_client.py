from terra_sdk.client.lcd import LCDClient, AsyncLCDClient
from terra_sdk.core import AccAddress
from enum import Enum
from datetime import datetime, timezone


class TerraNetwork(Enum):
    MAINNET = "columbus-5"
    TESTNET = "bombay-12"


class TerraClient:
    client: LCDClient
    network: TerraNetwork

    def __init__(self, network: str):
        self.network = TerraNetwork[network]
        self.client = LCDClient(
            chain_id=self.network.value,
            url="https://lcd.terra.dev" if self.network == TerraNetwork.MAINNET else "https://bombay-lcd.terra.dev",
        )

    def get_block_time(self):
        return int(
            datetime.strptime(
                self.client.tendermint.block_info()["block"]["header"]["time"][:-4], "%Y-%m-%dT%H:%M:%S.%f"
            )
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )

    def get_asset_balance(self, user_address: str, asset_address: str) -> int:
        response = self.client.wasm.contract_query(asset_address, {"balance": {"address": user_address}})
        return int(response["balance"])

    def get_bank_balance(self, user_address: str, denom: str) -> int:
        response = self.client.bank.balance(AccAddress(user_address))
        for balance in response:
            if balance.denom == denom:
                return balance.amount
        return 0
