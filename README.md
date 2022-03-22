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
- Split up Terra into a different class https://github.com/unl1k3ly/AnchorHODL/blob/main/hodl.py
- Abstract out the logger to log and send notifications  
- Abstract out the types of queries and commands to contracts
- Missing pieces
  - Logging 
  - Sizing 
  - Execution Ordering
- Graceful handling of incomplete transactions (in the case of multi-block transactions)
- UI to show 
  - Pending transactions 
  - Past transactions 
  - Total PnL
- Add Aps `BackgroundScheduler`


https://github.com/nebula-protocol/nebula-bots/blob/master/lambda/rewards-bot/lambda_function.py


## Known bugs 
- For mac conda if you get an error on `ripemd160` make sure you are using 
  - conda-forge::openssl-3.0.0-h0d85af4_2
  - `conda install -c anaconda openssl`