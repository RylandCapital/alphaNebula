import os
import requests
import time
import datetime as dt

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.coins import Coins
from terra_sdk.key.mnemonic import MnemonicKey
from dotenv import load_dotenv
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.fee import Fee


load_dotenv()

NEBULA_MK = os.getenv("NEBULA_MK")


'''Basic LCD usage and wallet connect'''
terra = LCDClient(
    "https://lcd.terra.dev", "columbus-5"
    )
curr_block = terra.tendermint.block_info()['block']['header']['height']

mk = MnemonicKey(
    mnemonic=NEBULA_MK
    )
wallet = terra.wallet(mk)
acc_address = wallet.key.acc_address


'''DEX TIME AND SALES LUNA-UST using TerraSwap/Astroport/Loop'''
addys = {
    'ts':'terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6',
    'astro':'terra1m6ywlgn6wrjuagcmmezzz2a029gtldhey5k552',
    'loop':'terra1sgu6yca6yjk0a34l86u6ju4apjcd6refwuhgzv'
}

#inputs
run = True
dex = addys['astro']
theo_fee = .002
raw_price_last = 0
amount0_last = 0
amount1_last = 0
last_trade = 0
type = None

#run time and sales
while run == True:
    dex1 = requests.get('https://fcd.terra.dev/wasm/contracts/{0}/store?query_msg=%7B%22pool%22:%7B%7D%7D'.format(dex)).json()
    #get theo price no adjustments
    raw_price = float(dex1['result']['assets'][0]['amount'])/float(dex1['result']['assets'][1]['amount'])
    #check if any trades were made in last 1 second if not pass
    if raw_price!=raw_price_last:

        amount0change = float(dex1['result']['assets'][0]['amount'])-amount0_last
        amount1change = float(dex1['result']['assets'][1]['amount'])-amount1_last
        last_trade = abs(amount0change/amount1change)


        if amount0change>0:
            type='Buy Luna'
        else:
            type='Sell Luna'

        print("LAST TRADE STATISTICS")
        print('Trade Type: {0}'.format(type))
        print('theo price: {0}'.format(raw_price_last))
        if type=='Buy Luna':
            print('adjusted theo: {0}\n'.format(raw_price_last*(1+theo_fee)))
        if type=='Sell Luna':
            print('adjusted theo: {0}\n'.format(raw_price_last*(1-theo_fee)))

        print('number_ust_traded: {0}'.format(amount0change/1000000))
        print('number_luna_traded: {0}\n'.format(amount1change/1000000))
        print('actual_traded_price: {0}'.format(last_trade))
        print('market_impact: {0}%\n'.format(last_trade/raw_price-1))

        #collect expected bid offer for next trade based off current theo
        dex1_bid_ask = [
            raw_price*(1+theo_fee),
            raw_price*(1-theo_fee)
            ]
        print("EXPECTED BID OFFER FOR NEXT TRADE")
        print('Current Theo Bid/Offer: {0}\n\n\n'.format(dex1_bid_ask))


        amount0_last = abs(float(dex1['result']['assets'][0]['amount']))
        amount1_last = abs(float(dex1['result']['assets'][1]['amount']))
        raw_price_last = raw_price

    time.sleep(1)
    















