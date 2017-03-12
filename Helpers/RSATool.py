from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
import base64

class RSATool:

    def Generator(self):
        random_generator = Random.new().read
        private_key = RSA.generate(1024, random_generator)
        return  str(base64.b64encode(private_key.publickey().exportKey()), 'utf-8'), str(base64.b64encode(private_key.exportKey()), 'utf-8')

    def Encrypt(self,publicKey,targetDate):
        publicKey_b = base64.b64decode(bytes(publicKey, 'utf-8'))
        RSAObj = RSA.importKey(publicKey_b)
        enc_data = RSAObj.encrypt(targetDate.encode('utf-8'), 32)
        return str(base64.b64encode(enc_data[0]), 'utf-8')


        # public_key = private_key.publickey()
        # pp = public_key.exportKey()
        # private_key = RSA.generate(1024)
        # public_key = private_key.publickey()
        # pp = public_key.exportKey()
        # pv =   RSA.importKey(private_key.exportKey())
        # enc_data = public_key.encrypt('encrypt this message'.encode('utf-8'), 32)
        # pv.decrypt(enc_data)
        #轉字串(進資料庫,丟給平台)
        # str(base64.b64encode(public_key.exportKey()), 'utf-8')
        # 解回來(取出來再轉回byte)
        # base64.b64decode(bytes(str(base64.b64encode(public_key.exportKey()), 'utf-8'), 'utf-8'))
        # return str(base64.b64encode(enc_data[0]), 'utf-8')


    def Decrypt(self,privateKey,targetData):
        privateKey_b = base64.b64decode(bytes(privateKey, 'utf-8'))
        RSAObj = RSA.importKey(privateKey_b)
        dec_data = RSAObj.decrypt(base64.b64decode(targetData))
        return str(dec_data, 'utf-8')

    def DigitalSignture(self,privateKey,targetData):
        # RSA物件
        privateKey_b = base64.b64decode(bytes(privateKey, 'utf-8'))
        RSAObj = RSA.importKey(privateKey_b)

        # 簽章物件
        targetData_encode = targetData.encode('utf-8')
        hashObj = SHA256.new(targetData_encode)
        signer = PKCS1_v1_5.new(RSAObj)
        signature = signer.sign(hashObj)

        return str(base64.b64encode(signature), 'utf-8')

    def VerifyDigitalSignture(self,publicKey,targetData,signature):
        # RSA物件
        publicKey_byte = base64.b64decode(bytes(publicKey,'utf-8'))
        RSAObj = RSA.importKey(publicKey_byte)

        # 簽章物件
        targetData_encode = targetData.encode('utf-8')
        hashObj = SHA256.new(targetData_encode)
        signature_byte = base64.b64decode(signature)
        verifier = PKCS1_v1_5.new(RSAObj)

        return verifier.verify(hashObj, signature_byte)

