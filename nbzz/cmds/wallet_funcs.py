from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile,keyfile
from nbzz.util.config import load_config
from web3 import Web3
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.rpc.xdai_rpc import connect_w3,get_proxy_contract,send_transaction

def show_swarm_key(bee_key_path):
    address= keyfile(bee_key_path)["address"]
    print(address)
    return address

def wallet_transfer(password,bee_key_path,amount, gas, send_address):
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("Wait for pledge")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    w3=connect_w3(config["swap_endpoint"])

    send_address=Web3.toChecksumAddress(send_address)
    my_local_acc=w3.eth.account.from_key(privatekey)

    proxy_contract=get_proxy_contract(w3)
    if gas==0:
        tx_receipt=send_transaction(w3,proxy_contract.functions.transfer(send_address,Web3.toWei(amount,"ether")),my_local_acc)
    else:
        tx_receipt=send_transaction(w3,proxy_contract.functions.transfer(send_address,Web3.toWei(amount,"ether")),my_local_acc,gas=gas)

    if tx_receipt["status"] !=1:
        print( "Transfer fail ")
    else:
        print( "Transfer success ")
def wallet_balance(bee_key_path):
    address= keyfile(bee_key_path)["address"]
    address=Web3.toChecksumAddress(address)
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    w3=connect_w3(config["swap_endpoint"])
    proxy_contract=get_proxy_contract(w3)

    balance=proxy_contract.functions.balanceOf(address).call()
    return balance
