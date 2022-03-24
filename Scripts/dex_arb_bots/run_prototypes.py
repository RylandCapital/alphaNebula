import threading
import os

from terra_sdk.client.lcd import LCDClient

from Scripts.dex_arb_bots.prototypes.arb import luna_ust_arb


NEBULA_MK = os.getenv("NEBULA_MK")

terra = LCDClient(
    "https://lcd.terra.dev", "columbus-5"
    )

if __name__ == "__main__":

    bot1 = threading.Thread(target=luna_ust_arb, kwargs={
        'dex_buy':'terraswap', #dex you are buying on 
        'dex_sell':'astro', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.ts_astro', #name for output
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot2 = threading.Thread(target=luna_ust_arb, kwargs={
        'dex_buy':'astro', #dex you are buying on 
        'dex_sell':'terraswap', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.astro_ts', #name for output
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot3 = threading.Thread(target=luna_ust_arb, kwargs={
        'dex_buy':'astro', #dex you are buying on 
        'dex_sell':'loop', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.astro_loop', #name for output
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot4 = threading.Thread(target=luna_ust_arb, kwargs={
        'dex_buy':'loop', #dex you are buying on 
        'dex_sell':'astro', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.loop_astro', #name for output
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot5 = threading.Thread(target=luna_ust_arb, kwargs={
        'dex_buy':'loop', #dex you are buying on 
        'dex_sell':'terraswap', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.loop_ts', #name for output
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    )

    bot6 = threading.Thread(target=luna_ust_arb, kwargs={
        'dex_buy':'terraswap', #dex you are buying on 
        'dex_sell':'loop', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.loop_ts', #name for output
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    )

    bot1.start()
    bot2.start()
    bot3.start()
    bot4.start()
    bot5.start()
    bot6.start()

