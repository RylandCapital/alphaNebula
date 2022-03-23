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
- Use ayncterra

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
    return
```


## Known bugs 
- For mac conda if you get an error on `ripemd160` make sure you are using 
  - conda-forge::openssl-3.0.0-h0d85af4_2
  - `conda install -c anaconda openssl`