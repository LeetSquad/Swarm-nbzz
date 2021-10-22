import click
from web3 import Web3
from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile,keyfile
from nbzz.rpc.xdai_rpc import connect_w3, get_lock_contract,send_transaction
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.util.config import load_config
from typing import Dict
@click.group("lockup", short_help="Manage your wallet") 
def lockup_cmd() -> None:
    pass

@lockup_cmd.command("status", short_help="Check the number of nbzz currently locked.")
@click.option("-a", "--address", help="Address to send the nbzz", type=str,default="")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
def detail_cmd(address: str,bee_key_path,) -> None:
    if not address:
        address= keyfile(bee_key_path)["address"]
    address=Web3.toChecksumAddress(address)
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    w3=connect_w3(config["swap_endpoint"])
    lock_contract=get_lock_contract(w3)
    releasable=lock_contract.functions.lockupReleasable(address).call()
    remaining=lock_contract.functions.lockupRemaining(address).call()
    print(f"Locked nbzz: {Web3.fromWei(remaining,'ether')}, releasable nbzz: {Web3.fromWei(releasable,'ether')}.")

@lockup_cmd.command("release", short_help="Release nbzz that can be released.")
@click.option("-a", "--address", help="Address to send the nbzz", type=str,default="")
@click.option("-p", "--password",  type=str, prompt="input password of bee", help="password of bee")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
def release_cmd(address,password,bee_key_path) -> None:
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    w3=connect_w3(config["swap_endpoint"])
    my_local_acc=w3.eth.account.from_key(privatekey)

    if not address:
        release_address= keyfile(bee_key_path)["address"]
    else:
        release_address= address
    release_address=Web3.toChecksumAddress(release_address)
    lock_contract=get_lock_contract(w3)

    releasable=lock_contract.functions.lockupReleasable(release_address).call()
    if releasable>0:
        tx_receipt=send_transaction(w3,lock_contract.functions.lockupRelease(release_address),my_local_acc)

        print(tx_receipt)
    else:
        print("The number of nbzz that can be released is 0.")
    if tx_receipt["status"] !=1:
        print( "Start fail ")
    else:
        print( "Start success ")



