from Crypto.Hash import SHA3_256
from web3 import Web3

def hash_random(block_hash,node_set,commit_block):
    commit_eth_list=[]

    check_list=[(ieth,SHA3_256.new(block_hash+ieth).digest()) for ieth in node_set]
    check_list.sort(key=lambda x :x[1])
    if len(check_list)>commit_block:
        while check_list[commit_block-1][1]==check_list[commit_block][1]:
            check_list=[(ieth,SHA3_256.new(block_hash+ieth).digest()) for ieth in node_set]
            check_list.sort(key=lambda x :x[1])
    
    for i in check_list[:commit_block]:
        reth_address=Web3.toChecksumAddress("0x"+i[0].hex())
        print(reth_address)
        commit_eth_list.append(reth_address)
    
    return commit_eth_list