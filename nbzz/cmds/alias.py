import click
import web3
from web3.main import Web3
from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile,keyfile
from nbzz.util.config import load_config
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.rpc.xdai_rpc import connect_w3,get_alias_contract,send_transaction

@click.group("alias", short_help="Manage your alias")
@click.pass_context
def alias_cmd(ctx: click.Context):
    """View and use your alias"""
    from pathlib import Path

    root_path: Path = ctx.obj["root_path"]
    if not root_path.is_dir():
        raise RuntimeError("Please initialize (or migrate) your config directory with nbzz init")

@alias_cmd.command("set-alias", short_help="set alias")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee",help="password of bee")
@click.option("-a", "--alias",  type=str, prompt="set alias",help="set alias")
@click.pass_context
def set_alias_cmd(ctx: click.Context, password,bee_key_path,alias) -> None:
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("wait for set alias")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

    w3=connect_w3(config["swap_endpoint"])

    my_local_acc=w3.eth.account.from_key(privatekey)
    
    alias_contract=get_alias_contract(w3)

    tx_receipt=send_transaction(w3,alias_contract.functions.setAddressAlias(alias),my_local_acc,gas=290_0000)#alias

    print(tx_receipt)
    if tx_receipt["status"] !=1:
        print( "set alias fail ")
    else:
        print( "set alias success ")

@alias_cmd.command("set-address", short_help="set address")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee",help="password of bee")
@click.option("-a", "--address",  type=str, prompt="set address",help="set address")
@click.pass_context
def set_address_cmd(ctx: click.Context, password,bee_key_path,address) -> None:
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("wait for set address")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

    w3=connect_w3(config["swap_endpoint"])

    my_local_acc=w3.eth.account.from_key(privatekey)
    
    alias_contract=get_alias_contract(w3)

    set_address=Web3.toChecksumAddress(address)
    tx_receipt=send_transaction(w3,alias_contract.functions.setAddressMapping(set_address),my_local_acc,gas=290_0000)#alias

    print(tx_receipt)
    if tx_receipt["status"] !=1:
        print( "set address fail ")
    else:
        print( "set address success ")

@alias_cmd.command("show", short_help="set address")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-a", "--address",  type=str, default="",help="check address")
@click.pass_context
def show_cmd(ctx: click.Context, bee_key_path,address) -> None:
    if address =="":
        address= keyfile(bee_key_path)["address"]

    address=Web3.toChecksumAddress(address)

    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

    w3=connect_w3(config["swap_endpoint"])
    
    alias_contract=get_alias_contract(w3)

    map_address=alias_contract.functions.addressMappingOf(address).call()
    addressAlias=alias_contract.functions.addressAliasOf(address).call()

    print(f"map address:{map_address}, alias: {addressAlias}")