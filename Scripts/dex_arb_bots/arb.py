import requests
import time
import datetime as dt
import pandas as pd
import json
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



'''
Arbitrage Bot - Prototype. 
Using luna-ust as asset. 
'''

#dexs are ts, astro, and loop
#runs indefinitely, collect timestamps where positive trade could happen
#adding .001 as cushion to swap fees for chosen dex
#if any positive bid ask crosses then theoretically send execute message
'''theo fee one and two must be adjusted depending on dex!!!'''
'''market impact calc will be added using x*y = (x+deltaX)*(y+deltaY) where deltaX and deltaY
are the amounts of each asset we are depositing and removing'''
def luna_ust_arb(dex_one='terraswap', dex_two='astro', denom_buy='uusd', denom_sell='uluna',
     theo_fee1=.00305, theo_fee2 =.00205, client=None, walletkey=None, thresh=.002, pcttrade=.75):

    #inputs
    raw_price_last1 = 0
    raw_price_last2 = 0

    #ARB CALCS
    run = True
    raw_price_last1 = 0
    raw_price_last2 = 0
    positives = [{}] #collect positive timstamps as test
    post_banks = [pd.DataFrame([])]
    theodf = pd.DataFrame([], columns=[
        'dex1_theo',
        'dex2_theo',
        'dex1_bid',
        'dex1_offer',
        'dex2_bid',
        'dex2_offer',
        ]
    )
    while run == True:

        try:
            now = dt.datetime.now()
            dex1_address = ContractInfo().dexes[dex_one]['luna-ust']['mainnet']
            dex2_address = ContractInfo().dexes[dex_two]['luna-ust']['mainnet']

            dex1 = requests.get(
                "https://fcd.terra.dev/wasm/contracts/{0}/store?query_msg=%7B%22pool%22:%7B%7D%7D".format(str(dex1_address))
                ).json()
            dex2 = requests.get(
                'https://fcd.terra.dev/wasm/contracts/{0}/store?query_msg=%7B%22pool%22:%7B%7D%7D'.format(str(dex2_address))
                ).json()

            # convert to df with denom index. this solves asset order difference between dexes
            dex1 = pd.DataFrame(dex1['result']['assets'])
            dex1['info'] = dex1['info'].apply(lambda x: x['native_token']['denom'])
            dex2 = pd.DataFrame(dex2['result']['assets'])
            dex2['info'] = dex2['info'].apply(lambda x: x['native_token']['denom'])
            #set index as info column, providing denom as dataframe index
            dex1.set_index('info', inplace=True)
            dex2.set_index('info', inplace=True)

            #get theo price no adjustments
            raw_price1 = float(dex1.loc[denom_buy])/float(dex1.loc[denom_sell])
            raw_price2 = float(dex2.loc[denom_buy])/float(dex2.loc[denom_sell])

            #collect expected bid offer for next trade based off current theo
            dex1_bid_ask = [
                raw_price1*(1-theo_fee1), #bid
                raw_price1*(1+theo_fee1)  #offer
                ]
            dex2_bid_ask = [
                raw_price2*(1-theo_fee2),  #bid
                raw_price2*(1+theo_fee2)   #offer
                ]
            
            #looking for bid offer crosses
            buy1sell2 = dex2_bid_ask[0]/dex1_bid_ask[1]-1 #bid-dex2/offer-dex1
            buy2sell1 = dex1_bid_ask[0]/dex2_bid_ask[1]-1 #bid-dex1/offer-dex2

            #only/collect print data if anything has changed, aka trades have occured in pool to avoid clutter
            if (raw_price_last1 != raw_price1) | (raw_price_last2 != raw_price2):
                print("DEX1 THEO: {0}".format(raw_price1))
                print("DEX2 THEO: {0}\n".format(raw_price2))
                print("EXPECTED ARB BID OFFERS:{0}".format(now))
                print('DEX1 Bid/Offer: {0}'.format(dex1_bid_ask))
                print('DEX2 Bid/Offer: {0}\n'.format(dex2_bid_ask))            
                print('BUY DEX1 SELL DEX2 ARB - PREDICTED: {0}'.format(buy1sell2))
                print('BUY DEX2 SELL DEX1 ARB - PREDICTED: {0}\n\n\n'.format(buy2sell1))

                #collect for analysis
                    #theos
                theodf.loc[now, 'dex1_theo'] = raw_price1
                theodf.loc[now, 'dex2_theo'] = raw_price2
                theodf.loc[now, 'dex1_bid'] = dex1_bid_ask[0]
                theodf.loc[now, 'dex1_offer'] = dex1_bid_ask[1]
                theodf.loc[now, 'dex2_bid'] = dex2_bid_ask[0]
                theodf.loc[now, 'dex2_offer'] = dex2_bid_ask[1]

                    #positive arb opportunities 
                if (buy1sell2>0) | (buy2sell1>0):
                    positives.append({
                        'datetime':'now',
                        'buy1sell2':buy1sell2,
                        'buy2sell1':buy2sell1,
                    })

            #update lasts
            raw_price_last1 = raw_price1
            raw_price_last2 = raw_price2

            #make trades if applicable this makes sure trades are fired on start of algo
            if (raw_price_last1!=0) | (raw_price_last2!=0):

                #if dex1 is the buy side dex send buy message to dex1, sell to dex2
                if (buy1sell2>thresh):
                    print('Threshold met')
                    # Gets (what seems random) connection reset error, retrying seems to fix. 
                        # FIXES ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host
                    try:
                        print('I am about to trade')
                        mk = MnemonicKey(
                        mnemonic=walletkey
                        )
                        wallet = client.wallet(mk)
                        # Grab bank and format in a way that does error out whether there are 2 or 100 currencies.
                        bank = pd.DataFrame(
                            client.bank.balance(wallet.key.acc_address)[0].to_data()
                        ).set_index('denom').astype(int)
                    except Exception as e:
                        print('I got an error...')
                        print(e)
                        print('.................')
                        print('I trying to trade agian.')
                        mk = MnemonicKey(
                        mnemonic=walletkey
                        )
                        wallet = client.wallet(mk)
                        bank = pd.DataFrame(
                            client.bank.balance(wallet.key.acc_address)[0].to_data()
                        ).set_index('denom').astype(int)
                                   
                    msgs = [
                    MsgExecuteContract(
                                wallet.key.acc_address,
                                dex1_address,
                                {
                                "swap": {
                                    "belief_price": "{0}".format(dex1_bid_ask[1]), #hit the offer on dex1
                                    "max_spread": "0.001",
                                    "offer_asset": {
                                    "amount": "{0}".format(int(bank.loc[denom_buy,'amount']*pcttrade)),
                                    "info": {
                                        "native_token": {
                                        "denom": "{0}".format(denom_buy)
                                        }
                                    }
                                    }
                                }
                                },
                            { denom_buy: int(bank.loc[denom_buy,'amount']*pcttrade) }
                            ),
                    MsgExecuteContract(
                                wallet.key.acc_address,
                                dex2_address,
                                {
                                "swap": {
                                    "belief_price": "{0}".format(dex2_bid_ask[0]),
                                    "max_spread": "0.001",
                                    "offer_asset": {
                                    "amount": "{0}".format(

                                        int(bank.loc[denom_buy,'amount']*pcttrade / dex1_bid_ask[1]) #using $ value of UST used to buy / dex 1 predicted offer price offer price 

                                        ), 
                                    "info": {
                                        "native_token": {
                                        "denom": "{0}".format(denom_sell)
                                        }
                                    }
                                    }
                                }
                                },
                            { denom_sell: int(bank.loc[denom_buy,'amount']*pcttrade / dex1_bid_ask[1]) }
                            )
                    ]
                    
                    tx = wallet.create_and_sign_tx(
                    CreateTxOptions(msgs=msgs,
                     gas_prices="0.15uusd")
                        )
                    client.tx.broadcast(tx)


                    #(trade is over, no rush, so 2 sec sleep)
                    time.sleep(2)

                    #collect data for review
                    post_bank = pd.concat(
                        [
                        bank,
                        pd.DataFrame(
                            client.bank.balance(wallet.key.acc_address)[0].to_data()
                        ).set_index('denom').astype(int)
                    ], axis=1
                    )
                    post_bank['diff'] = (post_bank.iloc[:,1]-post_bank.iloc[:,0])/1000000
                    post_bank['trade_execution'] = now
                    post_banks.append(post_banks)


                    #add both buy and sell side txs for if dex2 is purchase dex (this isnt complete)
                        #currently just looking for dex 1 buys for now while testing.

                    #sleep to make avoid dups/rapid fire
                        #honestly just a safety measure, theoretically you might have back to back 
                        #opportunities to arb, but for now lets sleep for a little and then look for more
                    print('Sleeping for 60 seconds ...\n\n\n')
                    time.sleep(60)

            #1 second increment between DEX queries looking for arbitrade situations
            time.sleep(1)

        # any exceptions lets shut down for now and analyze mistakes
        except Exception as e:
            print(e)
            
#            return [positives, post_banks, theodf]
            



if __name__ == "__main__":

    NEBULA_MK = os.getenv("NEBULA_MK")

    terra = LCDClient(
    "https://lcd.terra.dev", "columbus-5"
    )

    data = luna_ust_arb(
        dex_one='loop',
        dex_two='astro',
        denom_buy='uusd',
        denom_sell='uluna',
        theo_fee1=.00305,
        theo_fee2 =.00205,
        client=terra,
        walletkey=NEBULA_MK,
        thresh=-.05,
        pcttrade=.50)
