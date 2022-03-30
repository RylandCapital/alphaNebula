from Scripts.utils.contract_info import ContractInfo
from Scripts.utils.cluster import Cluster



net = 'testnet'
address = ContractInfo().clusters[net]['clusters']['LUST']
cstate = Cluster(address, net=net).inventory()