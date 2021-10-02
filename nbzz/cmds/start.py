import click
from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile,keyfile
from nbzz.util.config import load_config
from web3 import Web3
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
import leveldb
from nbzz.rpc.xdai_rpc import connect_w3,get_model_contract,send_transaction
from nbzz.cmds.pledge_funcs import show_pledge
@click.command("start", short_help="start nbzz")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("--bee-statestore-path", default="./statestore", help="Config statestore path", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee",help="password of bee")
@click.pass_context
def start_cmd(ctx: click.Context, password,bee_key_path,bee_statestore_path) -> None:
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    
    db=leveldb.LevelDB(bee_statestore_path)
    overlay_address=db.Get(b"non-mineable-overlay").decode().strip('"')
    print("Wait for start")
    print(f"overlay_address: {overlay_address}")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    w3=connect_w3(config["swap_endpoint"])

    my_local_acc=w3.eth.account.from_key(privatekey)
    print(f"eth_address: {my_local_acc.address}")
    model_contract,_=get_model_contract(w3)
    pledgenum=show_pledge(my_local_acc.address,"")
    if Web3.fromWei(pledgenum,"ether")<15:
        print("ERROR: The pledge nbzz amount is less than 15.")
        exit(1)
    nodestate=model_contract.functions.nodeState(my_local_acc.address).call()
    if nodestate[0] and overlay_address==nodestate[3]:
        print("Nbzz already start")
        exit(0)

    tx_receipt=send_transaction(w3,model_contract.functions.nodeOnline(my_local_acc.address,overlay_address),my_local_acc,gas=40_0000)

    print(tx_receipt)
    if tx_receipt["status"] !=1:
        print( "Start fail ")
    else:
        print( "Start success ")

@click.command("status", short_help="status nbzz")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("--bee-statestore-path", default="./statestore", help="Config statestore path", type=click.Path(exists=True), show_default=True)
@click.pass_context
def status_cmd(ctx: click.Context, bee_key_path,bee_statestore_path) -> None:
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    db=leveldb.LevelDB(bee_statestore_path)
    overlay_address=db.Get(b"non-mineable-overlay").decode().strip('"')
    w3=connect_w3(config["swap_endpoint"])
    model_contract,_=get_model_contract(w3)
    eth_address=Web3.toChecksumAddress(keyfile(bee_key_path)["address"])
    nbzz_status=model_contract.functions.nodeState(eth_address).call()
    if nbzz_status[1]:
        print("Nbzz Mining")
    elif nbzz_status[0] and overlay_address==nbzz_status[3]:
        print("Nbzz running")
    else:
        print("Nbzz not running")