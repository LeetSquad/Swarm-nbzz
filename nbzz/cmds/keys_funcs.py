from typing import List


from nbzz.util.bee_key import keyfile

def show_swarm_key(bee_key_path):
    address= keyfile(bee_key_path)["address"]
    print(address)
    return address