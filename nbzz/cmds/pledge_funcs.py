
from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile
from nbzz.util.config import load_config
from pathlib import Path
from web3 import Web3
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.util.nbzz_abi import NBZZ_ABI

import click

def pledge(number,password,bee_key_path):
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("wait for pledge")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    swap_url=config["swap_endpoint"]
    if "http" ==swap_url[:4]:
        w3=Web3(Web3.HTTPProvider(swap_url))
    elif "ws" ==swap_url[:2]:
        w3=Web3(Web3.WebsocketProvider(swap_url))
    
    if not w3.isConnected():
        print("can't connect to swap endpoint")
        exit(1)
    my_local_acc=w3.eth.account.from_key(privatekey)
    w3.eth.default_account=my_local_acc.address
    nbzz_contract=w3.eth.contract(address=config["network_overrides"]["constants"][config["selected_network"]]["CONTRACT"],abi=NBZZ_ABI)
    construct_txn = nbzz_contract.functions.pledge().buildTransaction({"nonce":w3.eth.getTransactionCount(my_local_acc.address)}) #pledge
    print(construct_txn)
    signed =my_local_acc.sign_transaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    if tx_receipt["status"] !=1:
        print( "pledge fail ")
    else:
        print( "pledge sucess ")


def faucet(password,bee_key_path):
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("wait for faucet")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    swap_url=config["swap_endpoint"]
    if "http" ==swap_url[:4]:
        w3=Web3(Web3.HTTPProvider(swap_url))
    elif "ws" ==swap_url[:2]:
        w3=Web3(Web3.WebsocketProvider(swap_url))
    
    if not w3.isConnected():
        print("can't connect to swap endpoint")
        exit(1)
    my_local_acc=w3.eth.account.from_key(privatekey)
    w3.eth.default_account=my_local_acc.address
    nbzz_contract=w3.eth.contract(address=config["network_overrides"]["constants"][config["selected_network"]]["CONTRACT"],abi=NBZZ_ABI)
    construct_txn = nbzz_contract.functions.relief().buildTransaction({"nonce":w3.eth.getTransactionCount(my_local_acc.address)}) #faucet
    print(construct_txn)
    signed =my_local_acc.sign_transaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    if tx_receipt["status"] !=1:
        print( "faucet fail ")
    else:
        print( "faucet sucess ")