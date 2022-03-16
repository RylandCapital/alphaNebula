import requests
import pandas as pd
import numpy as np

from Scripts.utils.contract_info import ContractInfo



class Cluster:
    
    '''intended to help query cluster information to facilitate further actions'''

    def __init__(self, cluster_contract, net='testnet'):
        self.cluster_contract = cluster_contract
        self.net = net

    #returns target msg and cluster_state msg into pandas df ready for calcs
    def inventory(self):
        req = requests.get(
            ContractInfo().clusters[self.net]['chain_url'] + 
            r'wasm/contracts/{0}/store?query_msg=%7B"cluster_state":%7B%7D%7D'.format(
                self.cluster_contract
                )
            ).json()
        asset_types = [list(i['info'].keys())[0] for i in req['result']['target']]
        df = pd.DataFrame.from_dict(
            req['result']['target']
        )
        df['asset_types'] = asset_types
        df['address'] = df['info'].apply(lambda x: list(list(x.values())[0].values())[0])
        df['prices'] = req['result']['prices']
        df['inventory'] = req['result']['inv']
        df = df.rename(columns={'amount':'target_amount'}).drop('info', axis=1)
        return df[
            [
            'asset_types',
            'address',
            'prices',
            'inventory',
            'target_amount'
            ]
        ]

    #returns df of cluster target msg
    def target(self): 
        req = requests.get(
            ContractInfo().clusters[self.net]['chain_url'] + 
            r'wasm/contracts/{0}/store?query_msg=%7B"target":%7B%7D%7D'.format(
                self.cluster_contract
                )
            ).json()
        asset_types = [list(i['info'].keys())[0] for i in req['result']['target']]
        df = pd.DataFrame.from_dict(
            req['result']['target']
        )
        df['asset_types'] = asset_types
        df['address'] = df['info'].apply(lambda x: list(list(x.values())[0].values())[0])
        return df.rename(
            columns={'amount':'target_amount'}
            ).drop('info', axis=1)[
            [
            'asset_types',
            'address',
            'target_amount'
            ]
        ]
    
    #returns config json of cluster
    def config(self):
        req = requests.get(
            ContractInfo().clusters[self.net]['chain_url'] + 
            r'wasm/contracts/{0}/store?query_msg=%7B"config":%7B%7D%7D'.format(
                self.cluster_contract
                )
            ).json()
        return req['result']['config']

    


    
