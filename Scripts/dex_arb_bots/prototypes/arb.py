import requests
import time
import datetime as dt
import pandas as pd
import base64, json
import os

from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.coins import Coins
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.wasm import MsgExecuteContract

from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.fee import Fee

from Scripts.utils.contract_info import ContractInfo

from contextlib import redirect_stdout
from printPrepender import PrintPrepender

from dotenv import load_dotenv

load_dotenv()



'''
Arbitrage Bot - Prototype. 
Using luna-ust as asset. 

Fees = Gas_Fees + Tax **tax is now 0**
Gas_Fees = Gas_Prices * Gas 
           Gas_Prices = Cost Per Unit Gas e.g. .15uusd
           Gas = Gas Requested e.g. 467,017 from txFinder
           So .467017 * .15uusd = .070053 UST

           the difference between gas_used and gas_requested is important.
           what you send is gas requested, what actually is used is gas_used. 
           the difference is not refunded so keeping gas_requested as tight
           to gas used can be very beneficial.

Example Tx to Understand Calcs Above = https://finder.extraterrestrial.money/mainnet/tx/A992EDC1F789E1C444B7D93408766E0022535C49E5FE7461B90BF3C5C84B570F
Updated Gas Prices - https://fcd.terra.dev/v1/txs/gas_prices

'''

#dexs are ts, astro, and loop
#runs indefinitely, collect timestamps where positive trade could happen
#adding .001 as cushion to swap fees for chosen dex
#if any positive bid ask crosses then theoretically send execute message
'''theo fee one and two must be adjusted depending on dex!!!'''
'''market impact calc will be added using x*y = (x+deltaX)*(y+deltaY) where deltaX and deltaY
are the amounts of each asset we are depositing and removing'''
def arb(dex_buy='terraswap',
        dex_sell='astro',
        denom_buy='uusd',
        denom_sell='terra12hgwnpupflfpuual532wgrxu2gjp0tcagzgx4n',
        algo_name='ts-astro',
        pair='mars-ust',
        native=False,
        theo_fee1=.00305,
        theo_fee2 =.00305,
        client=None,
        walletkey=None,
        thresh=.0035,
        pcttrade=.75,
        alerthook=None
        ):

    #inputs
    raw_price_last1 = 0
    raw_price_last2 = 0

    #ARB CALCS
    run = True
    raw_price_last1 = 0
    raw_price_last2 = 0
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
    best_theo = -1000
    best_theofees = -1000

    dex1_address = ContractInfo().dexes[dex_buy][pair]['mainnet']
    dex2_address = ContractInfo().dexes[dex_sell][pair]['mainnet']
    while run == True:

            #run time
            now = dt.datetime.now()

            #ping asset amounts
            dex1 = requests.get(
                "https://lcd.terra.dev/wasm/contracts/{0}/store?query_msg=%7B%22pool%22:%7B%7D%7D".format(str(dex1_address))
                ).json()
            dex2 = requests.get(
                'https://lcd.terra.dev/wasm/contracts/{0}/store?query_msg=%7B%22pool%22:%7B%7D%7D'.format(str(dex2_address))
                ).json()

            # convert to df with denom index. this solves asset order difference between dexes
            def extract_pool_df(x):
                try:
                    value = x['native_token']['denom']
                except:
                    value = x['token']['contract_addr']
                return value
                
            dex1 = pd.DataFrame(dex1['result']['assets'])
            dex1['info'] = dex1['info'].apply(lambda x: extract_pool_df(x))
            dex2 = pd.DataFrame(dex2['result']['assets'])
            dex2['info'] = dex2['info'].apply(lambda x: extract_pool_df(x))
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

            #IMMEDIATELY MAKE TRADE IF NEEDED
            if (raw_price_last1!=0) | (raw_price_last2!=0):

                #if dex1 is the buy side dex send buy message to dex1, sell to dex2
                if (buy1sell2>thresh):
                    # Gets (what seems random) connection reset error, retrying seems to fix. 
                        # FIXES ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host
                    try:
                        mk = MnemonicKey(
                        mnemonic=walletkey
                        )
                        # Grab bank and format in a way that does error out whether there are 2 or 100 currencies.
                        bank = pd.DataFrame(
                            client.bank.balance(mk.acc_address)[0].to_data()
                        ).set_index('denom').astype(int) 
                    except Exception as e:
                        print('attempt 2 on wallet connect: {0}'.format(e))
                        mk = MnemonicKey(
                        mnemonic=walletkey
                        )
                        # Grab bank and format in a way that does error out whether there are 2 or 100 currencies.
                        bank = pd.DataFrame(
                            client.bank.balance(mk.acc_address)[0].to_data()
                        ).set_index('denom').astype(int)

                      
                    msgs = [
                    MsgExecuteContract(
                                mk.acc_address,
                                dex1_address,
                                {
                                "swap": {
                                    "belief_price": "{0}".format(dex1_bid_ask[1]), #hit the offer on dex1
                                    "max_spread": "0.0015",
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
                            )]
                    #if you are selling a native coin like uluna then send this message to execuete the sell side tx
                    if native==True:
                        msgs.append(
                                    MsgExecuteContract(
                                    mk.acc_address,
                                    dex2_address,
                                    {
                                    "swap": {
                                        "belief_price": "{0}".format(dex2_bid_ask[0]),
                                        "max_spread": "0.0015",
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
                        )
                    #or if selling a non-native coin like mars, anc, etx then send this message to execuete the sell side tx
                    else:
                        msg = {
                               "swap": {
                                    "belief_price": "{0}".format(dex2_bid_ask[0]),
                                    "max_spread": "0.0015"
                                    }
                                }
                        msgs.append(
                            MsgExecuteContract(
                                mk.acc_address,
                                denom_sell, #token contract you are selling 
                                {
                                    "send": {
                                        "contract": dex2_address,
                                        "amount": '{0}'.format(int(bank.loc[denom_buy,'amount']*pcttrade / dex1_bid_ask[1])),
                                        'msg': base64.b64encode(bytes(json.dumps(msg), "ascii")).decode(),
                                    }
                                },
                                
                            ),
                        )
                        
                    wallet = terra.wallet(mk)
                    tx = wallet.create_and_sign_tx(
                    CreateTxOptions(msgs=msgs,
                    gas_prices="0.15uusd",
                    gas_adjustment="1.2")
                        )
                    client.tx.broadcast(tx)

                    #TRADE IS OVER COLLECT PRE TRADE DATA
                    
                    #print in console
                    print('Trade Executed ...\n')
                    print('Here are the pre-trade-stats')
                    theodf.loc[now, 'dex1_theo'] = raw_price1
                    theodf.loc[now, 'dex2_theo'] = raw_price2
                    theodf.loc[now, 'dex1_bid'] = dex1_bid_ask[0]
                    theodf.loc[now, 'dex1_offer'] = dex1_bid_ask[1]
                    theodf.loc[now, 'dex2_bid'] = dex2_bid_ask[0]
                    theodf.loc[now, 'dex2_offer'] = dex2_bid_ask[1]
                    print(theodf.T.to_dict())
                    
                    #send to discord
                    data = {
                        "content": 'Attempting an arbitrage on ' +
                        "{0}-{1}".format(denom_buy, denom_sell) +
                        ' between {0}'.format(algo_name) +
                        ' with a thresh of {0}'.format(thresh)
                        }
                    requests.post(alerthook, json=data)

                    #sleep to make avoid dups/rapid fire
                        #honestly just a safety measure, theoretically you might have back to back 
                        #opportunities to arb, but for now lets sleep for a little and then look for more
                    
                    
                    time.sleep(60)
                    


            #update best prices so far for viewing analysis in console
            if (raw_price2/raw_price1-1) > best_theo:
                best_theo = (raw_price2/raw_price1-1)
            if (buy1sell2) > best_theofees:
                best_theofees = buy1sell2
            
                

            #only/collect print data if anything has changed, aka trades have occured in pool to avoid clutter
            if (raw_price_last1 != raw_price1) | (raw_price_last2 != raw_price2):
                print(
                        "{0}.{1}.{2} ".format(pair, dex_buy, dex_sell) +
                        "{0} ".format(now) +
                        "RAW PRICE DEX1 {0} ".format(raw_price1) + 
                        "RAW PRICE DEX2 {0} ".format(raw_price2) + 
                        "THEO ARB: {0} ".format(
                        (raw_price2/raw_price1-1)) + 
                        '-' +
                        ' ARB W FEES FEES: {0} '.format(
                            buy1sell2
                        )
                        + '   BEST {0} : {1}'.format(best_theo, best_theofees)

                )

                #update lasts
                raw_price_last1 = raw_price1
                raw_price_last2 = raw_price2

            
            #1 second increment between DEX queries looking for arbitrade situations
            time.sleep(1)




NEBULA_MK = os.getenv("NEBULA_MK")
DISCORD_LUNAUST = os.getenv("DISCORD_LUNAUST")
DISCORD_ANCUST = os.getenv("DISCORD_ANCUST")
DISCORD_LUNAXLUNA = os.getenv("DISCORD_LUNAXLUNA")
DISCORD_MARSUST = os.getenv("DISCORD_MARSUST")

terra = LCDClient(
    "https://lcd.terra.dev", "columbus-5"
    )

arb(dex_buy='terraswap',
    dex_sell='astro',
    denom_buy='uusd',
    denom_sell='terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76',
    algo_name='ts_astro',
    pair='anc-ust',
    native=False,
    theo_fee1=.00305,
    theo_fee2 =.00305,
    client=terra,
    walletkey=NEBULA_MK,
    thresh=.0035,
    pcttrade=.50,
    alerthook=DISCORD_ANCUST)
