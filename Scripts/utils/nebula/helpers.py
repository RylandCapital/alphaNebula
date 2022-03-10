import requests
import pandas as pd
import numpy as np

from Scripts.utils.nebula.contract_info import ContractInfo



class Cluster:
    
    '''intended to help query cluster information to facilitate further actions'''

    def __init__(self, cluster_contract):
        self.cluster_contract = cluster_contract
        pass

    #returns df of cluster target msg
    def target(self): 
        req = requests.get(
            ContractInfo().chain_url + r'wasm/contracts/{0}/store?query_msg=%7B"target":%7B%7D%7D'.format(self.cluster_contract)
        ).json()
        asset_types = [list(i['info'].keys())[0] for i in req['result']['target']]
        df = pd.DataFrame.from_dict(
            req['result']['target']
        )
        df['asset_types'] = asset_types
        df['address'] = df['info'].apply(lambda x: list(list(x.values())[0].values())[0])
        return df.drop('info', axis=1)[[
            'asset_types',
            'address',
            'amount'
        ]]
    
    #returns config json of cluster
    def config(self):
        req = requests.get(
            ContractInfo().chain_url + r'wasm/contracts/{0}/store?query_msg=%7B"config":%7B%7D%7D'.format(cluster_contract)
        ).json()
        return req['result']['config']

    


    
