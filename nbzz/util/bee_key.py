import eth_keyfile
import scrypt
from Crypto.Hash import SHA3_256
from Crypto.Cipher import AES
from Crypto.Util import Counter

def keyfile(key_path):
    keyfile=eth_keyfile.load_keyfile(key_path)
    return keyfile
def decrypt_privatekey_from_bee_keyfile(key_path,password:str):
    keyfile=eth_keyfile.load_keyfile(key_path) 
    crypto=keyfile["crypto"]

    kdfparams=crypto["kdfparams"]
    derivedKey=scrypt.hash(password.encode("utf-8"),bytes.fromhex(kdfparams["salt"]),kdfparams["n"],kdfparams["r"],kdfparams["p"],kdfparams["dklen"])

    ciphertext=bytes.fromhex(crypto["ciphertext"])
    mac=SHA3_256.SHA3_256_Hash(derivedKey[16:32]+ciphertext,update_after_digest=False) #mac校验
    if mac.hexdigest() == crypto["mac"]:
        print("password right")
    else:
        print("password error")
        exit(1)
    key=derivedKey[:16]
    iv=int("0x"+crypto["cipherparams"]["iv"],16)
    ctr = Counter.new(128, initial_value=iv)
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    privatekey=aes.decrypt(ciphertext).hex()
    return privatekey