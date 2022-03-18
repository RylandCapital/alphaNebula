import requests
import time
import datetime as dt
import os

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.coins import Coins
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.wasm import MsgExecuteContract

from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.fee import Fee

from Scripts.utils.contract_info import ContractInfo

from dotenv import load_dotenv
load_dotenv()



#dexs are ts, astro, and loop
#runs indefinitely, collect timestamps where positive trade could happen
#adding .001 as cushion to swap fees for chosen dex
#if any positive bid ask crosses then theoretically send execute message
def luna_ust_arb(dex_one='ts', dex_two='astro', theo_fee1=.00305, theo_fee2 =.00205,
                 client=None, walletkey=None, thresh=.002, pcttrade=.75):

    addys = {
        'ts':'terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6',
        'astro':'terra1m6ywlgn6wrjuagcmmezzz2a029gtldhey5k552',
    }

    #inputs
    raw_price_last1 = 0
    raw_price_last2 = 0

    #ARB CALCS
    run = True
    raw_price_last1 = 0
    raw_price_last2 = 0
    positives = [{}] #collect positive timstamps as test
    while run == True:

        try:

            now = dt.datetime.now()
            dex1 = requests.get(
                "https://fcd.terra.dev/wasm/contracts/{0}/store?query_msg=%7B%22pool%22:%7B%7D%7D".format(str(addys[dex_one]))
                ).json()
            dex2 = requests.get(
                'https://fcd.terra.dev/wasm/contracts/{0}/store?query_msg=%7B%22pool%22:%7B%7D%7D'.format(str(addys[dex_two]))
                ).json()
            #get theo price no adjustments

            raw_price1 = float(dex1['result']['assets'][0]['amount'])/float(dex1['result']['assets'][1]['amount'])
            raw_price2 = float(dex2['result']['assets'][0]['amount'])/float(dex2['result']['assets'][1]['amount'])

            #collect expected bid offer for next trade based off current theo
            dex1_bid_ask = [
                raw_price1*(1+theo_fee1),
                raw_price1*(1-theo_fee1)
                ]
            dex2_bid_ask = [
                raw_price2*(1+theo_fee2),
                raw_price2*(1-theo_fee2)
                ]

            print("DEX1 THEO: {0}".format(raw_price1))
            print("DEX2 THEO: {0}\n".format(raw_price2))
            print("EXPECTED ARB BID OFFERS:{0}".format(now))
            print('DEX1 Bid/Offer: {0}'.format(dex1_bid_ask))
            print('DEX2 Bid/Offer: {0}\n'.format(dex2_bid_ask))

            #dex 1 bid/ dex 2 offer
            buy1sell2 = dex2_bid_ask[1]/dex1_bid_ask[0]-1
            buy2sell1 = dex1_bid_ask[1]/dex2_bid_ask[0]-1
            print('BUY DEX1 SELL DEX2 ARB - PREDICTED: {0}'.format(buy1sell2))
            print('BUY DEX2 SELL DEX1 ARB - PREDICTED: {0}\n\n\n'.format(buy2sell1))

            #update lasts
            raw_price_last1 = raw_price1
            raw_price_last2 = raw_price2

            #make trades if applicable
            if (raw_price_last1!=0) | (raw_price_last2!=0):
                if (buy1sell2>thresh):


                    #connect to wallet and get updated bank
                    mk = MnemonicKey(
                        mnemonic=walletkey
                        )
                    wallet = client.wallet(mk)
                    bank = client.bank.balance(wallet.key.acc_address)[0]
                    amounts = {
                        'uusd': bank['uusd'].amount,
                        'uluna': bank['uluna'].amount
                    }


                    #construct buy tx
                    msg = MsgExecuteContract(
                                wallet.key.acc_address,
                                addys[dex_one],
                                {
                                "swap": {
                                    "belief_price": "{0}".format(raw_price1),
                                    "max_spread": "0.001",
                                    "offer_asset": {
                                    "amount": "{0}".format(int(amounts['uusd']*pcttrade)),
                                    "info": {
                                        "native_token": {
                                        "denom": "uusd"
                                        }
                                    }
                                    }
                                }
                                },
                            { 'uusd': int(amounts['uusd']*pcttrade) }
                            )
                    tx = wallet.create_and_sign_tx(
                    CreateTxOptions(msgs=[msg],
                     gas_prices="0.15uusd")
                        )
                    buy_result = client.tx.broadcast(tx)


                    #construct sell tx

                    #add both buy and sell side txs for if dex2 is purchase dex


                    #sleep to make avoid dups/rapid fire
                    time.sleep(100)

            time.sleep(1)

        except:
            return positives






if __name__ == "__main__":

    NEBULA_MK = os.getenv("NEBULA_MK")

    terra = LCDClient(
    "https://lcd.terra.dev", "columbus-5"
    )

    positives = luna_ust_arb(
        dex_one='ts',
        dex_two='astro',
        theo_fee1=.00305,
        theo_fee2 =.00205,
        client=terra,
        walletkey=NEBULA_MK,
        thresh=.002,
        pcttrade=.50)
