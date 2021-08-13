import click
from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile
from nbzz.util.config import load_config
from web3 import Web3
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.util.nbzz_abi import NBZZ_ABI
from web3.middleware import geth_poa_middleware
import time

from Crypto.Hash import SHA3_256

@click.command("gatekeeper", short_help="Coin guard")
@click.option("-b", "--begain-user", default=2000, help="The height of the block at which the coin starts", show_default=True)
@click.option("--bee-key-path", default="./keys/swarm.key", help="Config file root", type=click.Path(exists=True), show_default=True)
@click.option("-p", "--password",  type=str, prompt="input password of bee", help="password of bee")
@click.pass_context
def gatekeeper_cmd(ctx: click.Context, begain_user, password, bee_key_path) -> None:
    
    a_gatekeeper = False
    privatekey = decrypt_privatekey_from_bee_keyfile(bee_key_path, password)
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    swap_url = config["swap_endpoint"]
    if "http" == swap_url[:4]:
        w3 = Web3(Web3.HTTPProvider(swap_url))
    elif "ws" == swap_url[:2]:
        w3 = Web3(Web3.WebsocketProvider(swap_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # 注入poa中间件
    if not w3.isConnected():
        print("can't connect to swap endpoint")
        exit(1)
    my_local_acc = w3.eth.account.from_key(privatekey)
    w3.eth.default_account = my_local_acc.address
    print(config["network_overrides"]["constants"][config["selected_network"]]["CONTRACT"])
    nbzz_contract=w3.eth.contract(address=config["network_overrides"]["constants"][config["selected_network"]]["CONTRACT"],abi=NBZZ_ABI)

    nbzz_contract_height = config["network_overrides"]["constants"][config["selected_network"]]["BLOCKHEIGHT"]

    trustnode_list = nbzz_contract.functions.trustNodes(0).call() # TODO fix this bug 

    if my_local_acc.address == trustnode_list:
        a_gatekeeper = True
        print("i'm a gatekeeper")

    startblockheight = nbzz_contract.functions.startBlockHeight().call()    
    last_send_block_number=nbzz_contract.functions.lastBlockNumber().call()

    
    pledge_set = set()
    #同步startblockheight前的质押账户,如果当前区块小于开始区块,则等待
    if startblockheight==0:  # 未开始,只同步质押数据
        if not a_gatekeeper:
            print(
                "The contract has not started, please pledge in advance and wait patiently")
            exit(1)
        now_block_number = w3.eth.get_block_number()-8
        block_step_list=[i for i in range(nbzz_contract_height,now_block_number,100)]
        block_step_list.append(now_block_number)

        block_number_list=[(block_step_list[i],block_step_list[i+1]-1)   for i in range(len(block_step_list)-1)]
        for fromblock,toblock in block_number_list:
            transfer_filter = nbzz_contract.events.Transfer.createFilter(fromBlock=fromblock, toBlock=toblock, argument_filters={'_to': '0x1111111111111111111111111111111111111111'})
            all_event=transfer_filter.get_all_entries()
            [pledge_set.add(bytes.fromhex(event["args"]['_from'][2:])) for event in all_event ]
            print(f"from { fromblock} to {toblock} add pledge address num :{len(all_event)}")

        last_check_block_number=now_block_number-1

        while len(pledge_set)<begain_user:
            now_block_number=(w3.eth.get_block_number() - 8)

            if now_block_number>last_check_block_number:
                print(f"now_block:{now_block_number},last_check_block:{last_check_block_number}")
                transfer_filter = nbzz_contract.events.Transfer.createFilter(fromBlock=last_check_block_number+1, toBlock=now_block_number, argument_filters={'_to': '0x1111111111111111111111111111111111111111'})
                for event in transfer_filter.get_all_entries():
                    pledge_set.add(bytes.fromhex(event["args"]['_from'][2:]))
                    print("add pledge address ",event["args"]['_from'],",all pledge:",len(pledge_set))
                last_check_block_number=now_block_number
            time.sleep(10)
        last_send_block_number=now_block_number-64+1
    else:
        block_step_list=[i for i in range(nbzz_contract_height,last_send_block_number+64,100)]#do not -1
        block_step_list.append(last_send_block_number+64)

        block_number_list=[(block_step_list[i],block_step_list[i+1]-1)   for i in range(len(block_step_list)-1)]
        for fromblock,toblock in block_number_list:
            transfer_filter = nbzz_contract.events.Transfer.createFilter(fromBlock=fromblock, toBlock=toblock, argument_filters={'_to': '0x1111111111111111111111111111111111111111'})
            all_event=transfer_filter.get_all_entries()
            [pledge_set.add(bytes.fromhex(event["args"]['_from'][2:])) for event in all_event ]
            print(f"from { fromblock} to {toblock} add pledge address num :{len(all_event)}")
        now_block_number=last_send_block_number+64-1
        last_check_block_number=now_block_number

    right_eth_list=[]
    while(True):
        max_block_num=w3.eth.get_block_number()-8
        while(now_block_number<max_block_num):
            now_block_number+=1
            now_block_hash=w3.eth.get_block(now_block_number)["hash"]
            print(f"height:{now_block_number}",now_block_number-(last_send_block_number+63))
            check_list=[(ieth,SHA3_256.new(now_block_hash+ieth).digest()) for ieth in pledge_set]
            check_list.sort(key=lambda x :x[1])
            for i in check_list[:4]:
                reth_address=Web3.toChecksumAddress("0x"+i[0].hex())
                print(reth_address)
                right_eth_list.append(reth_address)

            if a_gatekeeper and ( now_block_number==last_send_block_number+64*2-1): #only for gatekepper
                # Submit the transaction that deploys the contract
                construct_txn  = nbzz_contract.functions.toDailyoutput(right_eth_list[-4*64:],now_block_number-64+1).buildTransaction({"nonce":w3.eth.getTransactionCount(my_local_acc.address),"gas":1000_0000})#0.5eth
                print(construct_txn)
                signed =my_local_acc.sign_transaction(construct_txn)

                tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
                # Wait for the transaction to be mined, and get the transaction receipt
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

                print(tx_receipt)
                last_send_block_number=now_block_number-64+1

            transfer_filter = nbzz_contract.events.Transfer.createFilter(fromBlock=last_check_block_number+1, toBlock=now_block_number, argument_filters={'_to': '0x1111111111111111111111111111111111111111'})
            for event in transfer_filter.get_all_entries():
                pledge_set.add(bytes.fromhex(event["args"]['_from'][2:]))
                print("add pledge address ",event["args"]['_from'],",all pledge:",len(pledge_set))
            last_check_block_number=now_block_number

            
        time.sleep(7)


