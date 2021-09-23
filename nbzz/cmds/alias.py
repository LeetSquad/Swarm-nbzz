import click
import web3
from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile,keyfile
from nbzz.util.config import load_config
from web3 import Web3
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.util.nbzz_abi import NBZZ_ABI
import eth_keyfile

@click.command("alias", short_help="set alias")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee",help="password of bee")
@click.option("-a", "--alias",  type=str, prompt="set alias",help="set alias")
@click.pass_context
def alias_cmd(ctx: click.Context, password,bee_key_path,alias) -> None:
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("wait for start")
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
    construct_txn = nbzz_contract.functions.setAddressAlias(alias).buildTransaction({"nonce":w3.eth.getTransactionCount(my_local_acc.address),"gas":290_0000}) #alias
    print(construct_txn)
    signed =my_local_acc.sign_transaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    if tx_receipt["status"] !=1:
        print( "set alias fail ")
    else:
        print( "set alias success ")