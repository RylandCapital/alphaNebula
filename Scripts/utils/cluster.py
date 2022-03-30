import requests
import pandas as pd
import numpy as np

from Scripts.utils.contract_info import ContractInfo


#current gas https://bombay-fcd.terra.dev/v1/txs/gas_prices

class Cluster:
    
    '''intended to help query cluster information to facilitate further actions'''

    def __init__(self, cluster_contract, net='testnet'):
        self.cluster_contract = cluster_contract
        self.net = net

    #returns target msg and cluster_state msg into pandas df ready for calcs
    def inventory(self):
        req = requests.get(
            ContractInfo().clusters[self.net]['chain_url'] + r'wasm/contracts/{0}/store?query_msg=%7B"cluster_state":%7B%7D%7D'.format(self.cluster_contract)
        ).json()
        asset_types = [list(i['info'].keys())[0] for i in req['result']['target']]
        df = pd.DataFrame.from_dict(req['result']['target'])
        df['asset_types'] = asset_types
        df['address'] = df['info'].apply(
            lambda x: list(list(x.values())[0].values())[0]
        )
        df['prices'] = [float(x) for x in req['result']['prices']]
        df['inventory'] = [int(x) for x in req['result']['inv']]
        df['inventory_pcts'] = df['inventory']/df['inventory'].sum()
        df = df.rename(columns={'amount':'target_amount'}).drop('info', axis=1)
        df['target_amount'] = df['target_amount'].astype('int64')
        df['deviation_amount'] = df['target_amount']-df['inventory']
        df['outstanding_tokens'] = req['result']['outstanding_balance_tokens']
        df['outstanding_tokens'] = df['outstanding_tokens'].astype('int64')
        df['target_pcts'] = df['target_amount']/df['target_amount'].sum()
        return df[
            [
            'asset_types',
            'address',
            'prices',
            'inventory',
            'inventory_pcts',
            'target_amount',
            'target_pcts',
            'deviation_amount',
            'outstanding_tokens',
            ]
        ]

    #returns df of cluster's target values (query_msg=target)
    def target(self): 
        req = requests.get(
            ContractInfo().clusters[self.net]['chain_url'] + r'wasm/contracts/{0}/store?query_msg=%7B"target":%7B%7D%7D'.format(self.cluster_contract)
        ).json()
        asset_types = [list(i['info'].keys())[0] for i in req['result']['target']]
        df = pd.DataFrame.from_dict(req['result']['target'])
        df['asset_types'] = asset_types
        df['address'] = df['info'].apply(lambda x: list(list(x.values())[0].values())[0])
        return df.rename(columns={'amount':'target_amount'}).drop('info', axis=1)[
            [
            'asset_types',
            'address',
            'target_amount'
            ]
        ]
    
    #returns json of cluster's config (query_msg=config)
    def config(self):
        req = requests.get(
            ContractInfo().clusters[self.net]['chain_url'] + r'wasm/contracts/{0}/store?query_msg=%7B"config":%7B%7D%7D'.format(self.cluster_contract)
        ).json()
        return req['result']['config']

    


    
