from web3 import Web3
import web3
from web3.middleware import geth_poa_middleware
from nbzz.util.config import load_config
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.util import nbzz_abi

def connect_w3(swap_url):
    if "http" == swap_url[:4]:
        w3 = Web3(Web3.HTTPProvider(swap_url))
    elif "ws" == swap_url[:2]:
        w3 = Web3(Web3.WebsocketProvider(swap_url))
    elif "ipc" ==swap_url[-3:]:
        w3 = Web3(Web3.IPCProvider(swap_url))
    else:
        print(f"swap_url format error. swap_url: {swap_url} ")

    w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # inject poa middleware
    if not w3.isConnected():
        print("can't connect to swap endpoint")
        exit(1)
    return w3

def get_one_filter(event,block_number):
    address_set=set()
    transfer_filter = event.createFilter(fromBlock=block_number, toBlock=block_number,)
    for event in transfer_filter.get_all_entries():
        address_set.add(bytes.fromhex(event["args"]["_address"][2:]))
    return address_set

def node_filter(contract,block_number,node_set,trust_node_set):
    node_set |= get_one_filter(contract.events.nodeConfirmOf,block_number)
    node_set -= get_one_filter(contract.events.nodeOfflineOf,block_number)
    
    trust_node_set |=get_one_filter(contract.events.addingATrustNode,block_number)
    trust_node_set -=get_one_filter(contract.events.deletingATrustedNode,block_number)
    
    print(f"block_num:{block_number} , pledge_num:{len(node_set)} ,trust_node_set:{len(trust_node_set)}")

def get_contract_info(contract_name):
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    any_contract_address=config["network_overrides"]["constants"][config["selected_network"]][contract_name]
    return any_contract_address

def get_model_contract(w3):
    contract_address=get_contract_info("CONTRACT_MODEL")
    model_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.MODEL_ABI)

    model_contract_height = get_contract_info("BLOCKHEIGHT")
    return model_contract,model_contract_height

def get_alias_contract(w3):
    contract_address=get_contract_info("CONTRACT_ALIAS")
    alias_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.ALIAS_ABI)
    return alias_contract

def get_glod_contract(w3):
    contract_address=get_contract_info("CONTRACT_GLOD")
    glod_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.GLOD_ABI)
    return glod_contract

def get_proxy_contract(w3):
    contract_address=get_contract_info("CONTRACT_PROXY")
    proxy_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.PROXY_ABI)
    return proxy_contract

def send_transaction(w3:Web3,construct,account:web3.Account,gas=None,print_info=True,timeout=120):

    tran_dict={"from":account.address,"nonce":w3.eth.getTransactionCount(account.address)}
    if gas: tran_dict["gas"] = gas

    construct_txn  = construct.buildTransaction(tran_dict)
    if print_info:
        print(construct_txn)
    signed =account.sign_transaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash,timeout)

    return tx_receipt