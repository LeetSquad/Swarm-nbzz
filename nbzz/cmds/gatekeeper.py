import click
from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile
from nbzz.util.config import load_config
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.rpc.xdai_rpc import connect_w3,node_filter,get_model_contract
from nbzz.simulator.hash_random import hash_random
import time

@click.command("gatekeeper", short_help="Coin guard")
@click.option("-b", "--begain-user", default=5000, help="The height of the block at which the coin starts", show_default=True)
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee", help="password of bee")
@click.pass_context
def gatekeeper_cmd(ctx: click.Context, begain_user, password, bee_key_path) -> None:
    spilt_block=32
    commit_block=1

    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

    w3=connect_w3(config["swap_endpoint"])

    privatekey = decrypt_privatekey_from_bee_keyfile(bee_key_path, password)
    my_local_acc = w3.eth.account.from_key(privatekey)

    model_contract,model_contract_height=get_model_contract(w3)
    print(f'model contract: {model_contract.address}')

    start_block_number=model_contract.functions.startBlockHeight().call()

    last_send_block_number=max(model_contract.functions.trustNode(my_local_acc.address).call()[2],start_block_number)
    all_last_send_block_number=model_contract.functions.lastBlockNumber().call()
    pledge_set ,trust_node_set= set(),set()
    print(f"begin_block: {start_block_number},{last_send_block_number},{all_last_send_block_number}")
    if start_block_number==0: #sync account before last_send_block_number ,and wait start

        now_block_number=model_contract_height

        while True:
            max_block_num=(w3.eth.get_block_number() - 8)

            while now_block_number<max_block_num:
                node_filter(model_contract,now_block_number,pledge_set,trust_node_set)
                if len(pledge_set)>begain_user: break

                now_block_number+=1 

            if len(pledge_set)>=begain_user: break

            time.sleep(2)

        last_send_block_number=now_block_number-spilt_block+1
    else:
        block_step_list=[i for i in range(model_contract_height,last_send_block_number+spilt_block,1)]#do not -1

        for now_block_number in block_step_list:
            node_filter(model_contract,now_block_number,pledge_set,trust_node_set) 

    right_eth_list=[]

    while(True):
        max_block_num=w3.eth.get_block_number()-8
        while(now_block_number<max_block_num):

            now_block_number+=1

            now_block_hash=w3.eth.get_block(now_block_number)["hash"]
            print(f"height:{now_block_number}",now_block_number-(last_send_block_number+spilt_block-1))

            commit_eth_list=hash_random(now_block_hash,pledge_set,commit_block)
            right_eth_list.extend(commit_eth_list)

            if ( now_block_number==last_send_block_number+spilt_block*2-1): 
                if (my_local_acc.address == hash_random(now_block_hash,trust_node_set,1)[0]) and (not model_contract.functions.BlockReleaseState(now_block_number-spilt_block+1).call()) : #only for gatekepper
                    print(now_block_number-spilt_block+1)
                    while True:
                        try:
                    # Submit the transaction that deploys the contract
                            construct_txn  = model_contract.functions.toDailyoutput(right_eth_list[-commit_block*spilt_block:],now_block_number-spilt_block+1).buildTransaction({"nonce":w3.eth.getTransactionCount(my_local_acc.address),"gas":1690_0000})#,"gasPrice": 10_000_000_000})#0.17xdai
                            print(construct_txn)
                            signed =my_local_acc.sign_transaction(construct_txn)

                            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
                            # Wait for the transaction to be mined, and get the transaction receipt
                            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash,timeout=3600)

                            print(tx_receipt)
                            last_send_block_number=now_block_number-spilt_block+1
                            break
                        except Exception as ex:
                            print("send transation error:",ex)
                        time.sleep(40)
                else:
                    last_send_block_number=now_block_number-spilt_block+1

            node_filter(model_contract,now_block_number,pledge_set,trust_node_set)
   
        time.sleep(2)