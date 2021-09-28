import click
from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile
from nbzz.util.config import load_config
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.rpc.xdai_rpc import connect_w3,get_model_contract,send_transaction

@click.command("stop", short_help="stop bzz")
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee",help="password of bee")
@click.pass_context
def stop_cmd(ctx: click.Context, password,bee_key_path) -> None:
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("wait for stop")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    w3=connect_w3(config["swap_endpoint"])

    my_local_acc=w3.eth.account.from_key(privatekey)
    model_contract,_=get_model_contract(w3)

    nodestate=model_contract.functions.nodeState(my_local_acc.address).call()
    if not nodestate[0]:
        print("Nbzz already stop")
        exit(0)

    tx_receipt=send_transaction(w3,model_contract.functions.nodeOffline(),my_local_acc,gas=40_0000)

    if tx_receipt["status"] !=1:
        print( "stop fail ")
    else:
        print( "stop success ")
