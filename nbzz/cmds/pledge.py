import click
from web3 import Web3
from pathlib import Path
from nbzz.cmds.pledge_funcs import add_pledge,unpack_pledge,disunpack_pledge,show_pledge,pledge_status

@click.group("pledge", short_help="Manage your pledge") 
def pledge_cmd() -> None:
    pass

@pledge_cmd.command("add", short_help="pledge nbzz")
@click.option("-n", "--number", default=15, help="Number of pledged coins", show_default=True)
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee",help="password of bee")
@click.pass_context
def add_cmd(ctx: click.Context, number, password,bee_key_path) -> None:
    add_pledge(number,password,bee_key_path)

@pledge_cmd.command("unpack", short_help="pledge nbzz")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee",help="password of bee")
@click.pass_context
def unpack_cmd(ctx: click.Context, password,bee_key_path) -> None:
    unpack_pledge(password,bee_key_path)

@pledge_cmd.command("disunpack", short_help="pledge nbzz")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee",help="password of bee")
@click.pass_context
def disunpack_cmd(ctx: click.Context,  password,bee_key_path) -> None:
    disunpack_pledge(password,bee_key_path)

@pledge_cmd.command("show", short_help="pledge nbzz")
@click.option("-a", "--address",  type=str, default="",help="check address")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.pass_context
def show_cmd(ctx: click.Context, address,bee_key_path) -> None:
    pledge_num=show_pledge(address,bee_key_path)
    print(f"pledge: {Web3.fromWei(pledge_num,'ether')} nbzz")

@pledge_cmd.command("status", short_help="pledge nbzz")
@click.option("-a", "--address",  type=str, default="",help="check address")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.pass_context
def status_cmd(ctx: click.Context, address,bee_key_path) -> None:
    status=pledge_status(address,bee_key_path)
    if status[0]==0:
        pledge_num=show_pledge(address,bee_key_path)
        print(f"In pledge:{Web3.fromWei(pledge_num,'ether')} nbzz, unpack num: 0 nbzz, unpack block: 0")
    else:
        print(f"In pledge: 0 nbzz, unpack num: {Web3.fromWei(status[0],'ether')} nbzz, unpack block: {status[1]}")