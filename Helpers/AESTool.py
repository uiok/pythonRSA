import base64, hashlib
from Crypto.Cipher import AES
from Crypto import Random


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]


class AESCipher:
    def encrypt(self, raw, key):
        key_byte = hashlib.sha256(key.encode("utf-8")).digest()
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key_byte, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc, key):
        key_byte = hashlib.sha256(key.encode("utf-8")).digest()
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(key_byte, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode("utf-8")

    def GenerateKey(self):

        return str(base64.b64encode(Random.new().read(AES.block_size)), 'utf-8')