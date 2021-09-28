import click
from web3 import Web3
from nbzz.cmds.wallet_funcs import wallet_transfer

@click.group("wallet", short_help="Manage your wallet") 
def wallet_cmd() -> None:
    pass

@wallet_cmd.command("transfer", short_help="Get all transactions")
@click.option("-p", "--password",  type=str, prompt="input password of bee", help="password of bee")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-a", "--amount", help="How much nbzz to send, in XDAI", type=int, required=True)
@click.option("-g","--gas",help="Set the fees for the transaction, in XDAI",type=int,default=0,show_default=True,)
@click.option("-t", "--address", help="Address to send the nbzz", type=str, required=True)
# @click.option("-o", "--override", help="Submits transaction without checking for unusual values", is_flag=True, default=False)
def transfer_cmd(password,bee_key_path,amount: int, gas: int, address: str) -> None:
    wallet_transfer(password,bee_key_path,amount, gas, address)


@wallet_cmd.command("private", short_help="Get a wallet private address")
@click.option("-p", "--password",  type=str, prompt="input password of bee", help="password of bee")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
def private_cmd(password,bee_key_path):
    from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile
    privatekey = decrypt_privatekey_from_bee_keyfile(bee_key_path, password)
    print(privatekey)


@wallet_cmd.command("public", short_help="Get a wallet public address")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
def public_cmd(bee_key_path) -> None:
    from .wallet_funcs import show_swarm_key
    show_swarm_key(bee_key_path)

@wallet_cmd.command("balance", short_help="Get a wallet public address")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
def public_cmd(bee_key_path) -> None:
    from .wallet_funcs import wallet_balance
    balance=wallet_balance(bee_key_path)
    print(f"Balance: {Web3.fromWei(balance,'ether')} nbzz")


