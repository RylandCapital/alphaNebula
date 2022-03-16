from Scripts.utils.contract_info import ContractInfo
from Scripts.utils.helpers import Cluster



net = 'testnet'
address = ContractInfo().clusters[net]['clusters']['MAU']
cstate = Cluster(address, net=net).inventory()