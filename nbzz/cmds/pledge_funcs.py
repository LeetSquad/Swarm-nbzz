
from nbzz.util.bee_key import decrypt_privatekey_from_bee_keyfile,keyfile
from nbzz.util.config import load_config
from web3 import Web3
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.rpc.xdai_rpc import connect_w3,get_glod_contract,get_model_contract,get_proxy_contract,send_transaction

def add_pledge(number,password,bee_key_path):
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("Wait for pledge")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    w3=connect_w3(config["swap_endpoint"])

    my_local_acc=w3.eth.account.from_key(privatekey)

    proxy_contract=get_proxy_contract(w3)
    glod_contract=get_glod_contract(w3)
    
    nbzz_balance=Web3.fromWei(proxy_contract.functions.balanceOf(my_local_acc.address).call(),"ether")
    if nbzz_balance<number:
        print(f"ERROR: The balance of nbzz is {nbzz_balance} and less than {number}, which cannot be pledged")
        exit(1)
    #approve
    tx_receipt=send_transaction(w3,proxy_contract.functions.approve(glod_contract.address,Web3.toWei(number,"ether")),my_local_acc,print_info=False)
    #print(tx_receipt)
    if tx_receipt["status"] !=1:
        print( "Approve fail ")
    else:
        print( "Approve success ")
    
    tx_receipt = send_transaction(w3,glod_contract.functions.thePledge(Web3.toWei(number,"ether")),my_local_acc,print_info=False)

    if tx_receipt["status"] !=1:
        print( "Pledge fail ")
    else:
        print( "Pledge success ")

def unpack_pledge(password,bee_key_path):
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("Wait for unpack")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    w3=connect_w3(config["swap_endpoint"])

    my_local_acc=w3.eth.account.from_key(privatekey)

    model_contract=get_model_contract(w3)

    #approve
    tx_receipt=send_transaction(w3,model_contract.functions.theUnpack(),my_local_acc,gas=40_0000)
    #print(tx_receipt)
    if tx_receipt["status"] !=1:
        print( "Unpack fail ")
    else:
        print( "Unpack success ")

def disunpack_pledge(password,bee_key_path):
    privatekey=decrypt_privatekey_from_bee_keyfile(bee_key_path,password)
    print("Wait for disunpack")
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    w3=connect_w3(config["swap_endpoint"])

    my_local_acc=w3.eth.account.from_key(privatekey)

    model_contract=get_model_contract(w3)

    #approve
    tx_receipt=send_transaction(w3,model_contract.functions.cancelTheUnpack(),my_local_acc,gas=40_0000)
    #print(tx_receipt)
    if tx_receipt["status"] !=1:
        print( "Disunpack fail ")
    else:
        print( "Disunpack success ")

def show_pledge(address,bee_key_path):
    if address =="":
        address= keyfile(bee_key_path)["address"]

    address=Web3.toChecksumAddress(address)

    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

    w3=connect_w3(config["swap_endpoint"])
    
    glod_contract=get_glod_contract(w3)

    pledge_num=glod_contract.functions.balancesPledge(address).call()
    return pledge_num
def pledge_status(address,bee_key_path):
    if address =="":
        address= keyfile(bee_key_path)["address"]

    address=Web3.toChecksumAddress(address)

    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")

    w3=connect_w3(config["swap_endpoint"])
    
    glod_contract=get_glod_contract(w3)

    status=glod_contract.functions.unpackState(address).call()
    return status