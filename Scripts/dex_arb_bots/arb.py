import requests
import time
import datetime as dt



#dexs are ts, astro, and loop
#runs indefinitely, collect timestamps where positive trade could happen
#adding .001 as cushion to swap fees for chosen dex
#if any positive bid ask crosses then theoretically send execute message
def luna_ust_arb(dex_one='ts', dex_two='astro', theo_fee1=.0031, theo_fee2 =.0021):
   
    addys = {
        'ts':'terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6',
        'astro':'terra1m6ywlgn6wrjuagcmmezzz2a029gtldhey5k552',
        'loop':'terra1sgu6yca6yjk0a34l86u6ju4apjcd6refwuhgzv'
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
        print("EXPECTED ARB BID OFFERS:{0}".format(now))
        print('DEX1 Bid/Offer: {0}'.format(dex1_bid_ask))
        print('DEX2 Bid/Offer: {0}\n'.format(dex2_bid_ask))

        #dex 1 bid/ dex 2 offer 
        print('BUY DEX1 SELL DEX2 ARB - PREDICTED: {0}'.format(dex2_bid_ask[1]/dex1_bid_ask[0]-1))
        print('BUY DEX2 SELL DEX1 ARB - PREDICTED: {0}\n\n\n'.format(dex1_bid_ask[1]/dex2_bid_ask[0]-1))


        raw_price_last1 = raw_price1
        raw_price_last2 = raw_price2

        if (raw_price_last1!=0) | (raw_price_last2!=0):
            if ((dex2_bid_ask[1]/dex1_bid_ask[0]-1)>0) | ((dex1_bid_ask[1]/dex2_bid_ask[0]-1)>0):
                positives.append(
                    {
                    'date':now,
                    'buy_1_sell_2':dex2_bid_ask[1]/dex1_bid_ask[0]-1,
                    'buy_2_sell_1':dex1_bid_ask[1]/dex2_bid_ask[0]-1
                }    
                )

                #send swap messages here if positive
            
        time.sleep(1)
        
    return positives