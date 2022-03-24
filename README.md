# Install instructions 
- Create a new virtualenv
  - Make sure `python3 --version` returns 3.9.4
  - `pip install virtualenv`
  - `python3 -m venv env`
- Run `source env/bin/activate`
- Install the packages using `pip install -r requirements.txt` 

# Before running code 
- Run `source env/bin/activate`

# When making changes in packages
- Run `pip install XX`
- Run `pip freeze > requirements.txt` 


# To Do 
- Abstract out the logger to log and send notifications  
- Abstract out the types of queries and commands to contracts
- Missing pieces
  - Sizing 
  - Position Executor
- Graceful handling of incomplete transactions (in the case of multi-block transactions)
- UI to show 
  - Pending transactions 
  - Past transactions 
  - Total PnL
- Add Aps `BackgroundScheduler`
- Add discord bot alert for position executor
- Should run the bot at multiple places to let them compete ... 

https://github.com/nebula-protocol/nebula-bots/blob/master/lambda/rewards-bot/lambda_function.py

```python
def initialize(context):
    context.i = 0
    context.asset = symbol('AAPL')


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return

def main():
  terra = AsyncTerraWallet(...)
  uuid = terra.executeTransaction(...)
  uuid2 = terra.executeTransaction(...)
  tx = terra.getTransactionStatus(uuid)
  tx = terra.waitTransaction(uuid)

  terra.waitAllTransactions()

class Transaction:
  def __init__():
    self.time_start
    self.time_end
    self.task = SOMETHING
  
  async def run_task():
    if self.task:
      self.task()
      # Update the time and the status 
      result = await terra.tx.broadcast_sync()
      result.is_tx_error()
      result.code
    return

    # Use sync: https://github.com/cosmos/cosmos-sdk/issues/4186
  
```

From Phong 
- this is how we do it for our oms. we create records for the order so pre execution data like order amount, dex, belief price(price at that time), timestamp. then execution records so mostly same overlapping data exepct this has fees and actual trade value and tx timestamps.
- ok see this is interesting. in my mind I was thinking saving the pools asset amounts every second would be fine, but that doesnt really give you trade data, only price data. there could have been 1 trade or 5 trades that changed the assets in the pool. so collecting txs from the contract, not asset amounts is the only way


## Known bugs 
- For mac conda if you get an error on `ripemd160` make sure you are using 
  - conda-forge::openssl-3.0.0-h0d85af4_2
  - `conda install -c anaconda openssl`