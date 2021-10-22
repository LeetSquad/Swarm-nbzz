from web3 import Web3
import web3
from web3.middleware import geth_poa_middleware
from nbzz.util.config import load_config
from typing import Dict
from nbzz.util.default_root import DEFAULT_ROOT_PATH
from nbzz.util import nbzz_abi
import pickle
import plyvel
from pathlib import Path
import string
import contextlib
def connect_w3(swap_url,timeout=30):
    if "http" == swap_url[:4]:
        w3 = Web3(Web3.HTTPProvider(swap_url,request_kwargs={'timeout': timeout}))
    elif "ws" == swap_url[:2]:
        w3 = Web3(Web3.WebsocketProvider(swap_url,websocket_kwargs={"max_size":1_000_000_000},websocket_timeout=timeout))
    elif "ipc" ==swap_url[-3:]:
        w3 = Web3(Web3.IPCProvider(swap_url,timeout=timeout))
    else:
        print(f"swap_url format error. swap_url: {swap_url} ")

    w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # inject poa middleware
    if not w3.isConnected():
        print("can't connect to swap endpoint")
        exit(1)
    return w3
class filter_cache:
    def __init__(self,db_name,cache_path=Path("./nodecache/")):
        self.root_path=Path(cache_path)/str(db_name)
        if not self.root_path.exists():
            self.root_path.mkdir(parents=True)
        self.db=plyvel.DB(str(self.root_path/"event_cache"),create_if_missing=True)
    def _key(self,*args):
        r=""
        for s in args:r+="_"+str(s)
        return r.encode("utf-8")
    def put(self,keys:tuple,value):
        self.db.put(self._key(*keys),pickle.dumps(value))
    def get(self,keys:tuple):
        res=self.db.get(self._key(*keys))
        if res is None: return None
        else: return pickle.loads(res)
    def close(self):
        for k,v in self.db.items():
            if not v.closed:
                v.close()

def get_one_filter(event_ff,block_number,cache_cls:filter_cache=None,filter_func=lambda event: bytes.fromhex(event["args"]["_address"][2:]),c_lock=contextlib.nullcontext())->set():
    address_set=set()
    if (cache_cls is None) or ((all_events:=cache_cls.get((event_ff.__name__,block_number))) is None):
        with c_lock:
            transfer_filter = event_ff.createFilter(fromBlock=block_number, toBlock=block_number,)
            all_events=transfer_filter.get_all_entries()
        cache_cls.put((event_ff.__name__,block_number),all_events)

    for event in all_events:
        address_set.add(filter_func(event))
    return address_set
    
def node_filter(contract,block_number,node_set,trust_node_set,cache_cls:filter_cache):
    node_set |= get_one_filter(contract.events.nodeConfirmOf,block_number,cache_cls)
    node_set -= get_one_filter(contract.events.nodeOnlineOf,block_number,cache_cls)
    node_set -= get_one_filter(contract.events.nodeOfflineOf,block_number,cache_cls)
    
    trust_node_set |=get_one_filter(contract.events.addingATrustNode,block_number,cache_cls)
    trust_node_set -=get_one_filter(contract.events.deletingATrustedNode,block_number,cache_cls)
    
    print(f"block_num:{block_number} , pledge_num:{len(node_set)} ,trust_node_set:{len(trust_node_set)}")

def check_node_status(model_contract,model0_contract,node_set)->set:
    offline_set=set()
    for one_adress in node_set:
        turn_adress=Web3.toChecksumAddress(one_adress.hex())
        node_old_state=model0_contract.functions.nodeState(turn_adress).call()
        node_state=model_contract.functions.nodeState(turn_adress).call()
        if not (node_state[0] and node_old_state[3]==node_state[3].hex()):
            offline_set.add(one_adress)
    return offline_set

def get_node_info(glod_contract,model_contract,node_list:list)->set:
    send_arg=([],[],[])
    for one_adress in node_list:
        one_adress=Web3.toChecksumAddress(one_adress.hex())

        node_info=model_contract.functions.nodeState(one_adress).call()
        if glod_contract.functions.balancesPledge(one_adress).call()>=Web3.toWei(15,"ether"):
            if len(node_info[3])==64 and all(c in string.hexdigits for c in node_info[3]):
                send_arg[0].append(one_adress)
                send_arg[1].append(Web3.toChecksumAddress(node_info[2]))
                send_arg[2].append('0x'+node_info[3])
            else:
                print(node_info[3],len(node_info[3]))

    return send_arg

def get_contract_info(contract_name):
    config: Dict = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    any_contract_address=config["network_overrides"]["constants"][config["selected_network"]][contract_name]
    return any_contract_address
def get_model0_contract(w3):
    contract_address=get_contract_info("CONTRACT_MODEL0")
    model_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.MODEL0_ABI)
    return model_contract
def get_model0_contract_height(w3):
    model_contract_height = get_contract_info("BLOCKHEIGHT0")
    return model_contract_height

def get_model_contract(w3):
    contract_address=get_contract_info("CONTRACT_MODEL")
    model_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.MODEL_ABI)
    return model_contract

def get_model_contract_height(w3):
    model_contract_height = get_contract_info("BLOCKHEIGHT")
    return model_contract_height

def get_lock_contract(w3):
    contract_address=get_contract_info("CONTRACT_LOCK")
    lock_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.LOCK_ABI)
    return lock_contract

def get_alias_contract(w3):
    contract_address=get_contract_info("CONTRACT_ALIAS")
    alias_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.ALIAS_ABI)
    return alias_contract

def get_glod_contract(w3):
    contract_address=get_contract_info("CONTRACT_GLOD")
    glod_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.GLOD_ABI)
    return glod_contract

def get_proxy_contract(w3):
    contract_address=get_contract_info("CONTRACT_PROXY")
    proxy_contract=w3.eth.contract(address=contract_address,abi=nbzz_abi.PROXY_ABI)
    return proxy_contract

def send_transaction(w3:Web3,construct,account:web3.Account,gas=None,print_info=True,timeout=120):

    tran_dict={"from":account.address,"nonce":w3.eth.getTransactionCount(account.address)}
    if gas: tran_dict["gas"] = gas

    construct_txn  = construct.buildTransaction(tran_dict)
    if print_info:
        print(construct_txn)
    signed =account.sign_transaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash,timeout)

    return tx_receipt
    
def eth_transfer_all(w3:Web3,from_account,to_address):
        value=w3.eth.get_balance(from_account.address)-100_0000*w3.eth.gasPrice
        if value<0: raise ValueError("all blance < 0")
        construct_txn=dict(
                    nonce=w3.eth.getTransactionCount(from_account.address),
                    gasPrice = w3.eth.gasPrice, 
                    chainId= w3.eth.chain_id ,#xdai
                    gas = 100_0000,
                    to=to_address,
                    value=value
                )
        gas=w3.eth.estimate_gas(construct_txn)
        construct_txn["gas"]=gas
        construct_txn["value"]=w3.eth.get_balance(from_account.address)-gas*w3.eth.gasPrice
        gas=w3.eth.estimate_gas(construct_txn)
        if gas != construct_txn["gas"]:
            raise ValueError("gas change")
        
        signed = from_account.signTransaction(construct_txn)
        tx_hash=w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt