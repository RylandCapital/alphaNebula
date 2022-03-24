import threading
import os

from terra_sdk.client.lcd import LCDClient

from Scripts.dex_arb_bots.prototypes.arb import arb


NEBULA_MK = os.getenv("NEBULA_MK")

terra = LCDClient(
    "https://lcd.terra.dev", "columbus-5"
    )

if __name__ == "__main__":


    #luna-ust
    bot1 = threading.Thread(target=arb, kwargs={
        'dex_buy':'terraswap', #dex you are buying on 
        'dex_sell':'astro', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.ts_astro', #name for output
        'pair':'luna-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot2 = threading.Thread(target=arb, kwargs={
        'dex_buy':'astro', #dex you are buying on 
        'dex_sell':'terraswap', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.astro_ts', #name for output
        'pair':'luna-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot3 = threading.Thread(target=arb, kwargs={
        'dex_buy':'astro', #dex you are buying on 
        'dex_sell':'loop', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.astro_loop', #name for output
        'pair':'luna-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot4 = threading.Thread(target=arb, kwargs={
        'dex_buy':'loop', #dex you are buying on 
        'dex_sell':'astro', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.loop_astro', #name for output
        'pair':'luna-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot5 = threading.Thread(target=arb, kwargs={
        'dex_buy':'loop', #dex you are buying on 
        'dex_sell':'terraswap', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.loop_ts', #name for output
        'pair':'luna-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    )

    bot6 = threading.Thread(target=arb, kwargs={
        'dex_buy':'terraswap', #dex you are buying on 
        'dex_sell':'loop', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'uluna', #what you are selling
        'algo_name':'lunaust.loop_ts', #name for output
        'pair':'luna-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    )



    #anc-ust
    bot7 = threading.Thread(target=arb, kwargs={
        'dex_buy':'terraswap', #dex you are buying on 
        'dex_sell':'astro', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76', #what you are selling
        'algo_name':'ancust.ts_astro', #name for output
        'pair':'anc-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot8 = threading.Thread(target=arb, kwargs={
        'dex_buy':'astro', #dex you are buying on 
        'dex_sell':'terraswap', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76', #what you are selling
        'algo_name':'ancust.astro_ts', #name for output
        'pair':'anc-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot9 = threading.Thread(target=arb, kwargs={
        'dex_buy':'astro', #dex you are buying on 
        'dex_sell':'loop', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76', #what you are selling
        'algo_name':'ancust.astro_loop', #name for output
        'pair':'anc-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot10 = threading.Thread(target=arb, kwargs={
        'dex_buy':'loop', #dex you are buying on 
        'dex_sell':'astro', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76', #what you are selling
        'algo_name':'ancust.loop_astro', #name for output
        'pair':'anc-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot11 = threading.Thread(target=arb, kwargs={
        'dex_buy':'loop', #dex you are buying on 
        'dex_sell':'terraswap', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76', #what you are selling
        'algo_name':'ancust.loop_ts', #name for output
        'pair':'anc-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    )

    bot12 = threading.Thread(target=arb, kwargs={
        'dex_buy':'terraswap', #dex you are buying on 
        'dex_sell':'loop', #dex you are selling on
        'denom_buy':'uusd', #what you are using to buy 
        'denom_sell':'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76', #what you are selling
        'algo_name':'ancust.ts_loop', #name for output
        'pair':'anc-ust', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    )



    #lunax-luna
    bot13 = threading.Thread(target=arb, kwargs={
        'dex_buy':'terraswap', #dex you are buying on 
        'dex_sell':'loop', #dex you are selling on
        'denom_buy':'uluna', #what you are using to buy 
        'denom_sell':'terra17y9qkl8dfkeg4py7n0g5407emqnemc3yqk5rup', #what you are selling
        'algo_name':'lunaxluna.ts_loop', #name for output
        'pair':'lunax-luna', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    bot14 = threading.Thread(target=arb, kwargs={
        'dex_buy':'loop', #dex you are buying on 
        'dex_sell':'terraswap', #dex you are selling on
        'denom_buy':'uluna', #what you are using to buy 
        'denom_sell':'terra17y9qkl8dfkeg4py7n0g5407emqnemc3yqk5rup', #what you are selling
        'algo_name':'lunaxluna.loop_ts', #name for output
        'pair':'lunax-luna', #name used for contractInfo and Discord hooks
        'theo_fee1':.00305, #swap fee buy dex
        'theo_fee2' :.00305, #sawp fee sell dex
        'client':terra,
        'walletkey':NEBULA_MK,
        'thresh':.0035, #pct predicted arb to trigger trade
        'pcttrade':.25
     } #pct of wallet to trade when arb is triggered)
    ) 

    

    bots = [
     bot1,
     bot2,
     bot7,
     bot8,
     bot11,
     bot12,
     bot13,
     bot14
     ]
    
    for bot in bots:
        bot.start()

