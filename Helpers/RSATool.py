from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
import base64

class RSATool:

    def Generator(self):
        random_generator = Random.new().read
        private_key = RSA.generate(2048, random_generator)
        return  str(base64.b64encode(private_key.publickey().exportKey()), 'utf-8'), str(base64.b64encode(private_key.exportKey()), 'utf-8')

    def Encrypt(self,publicKey,targetDate):
        publicKey_b = base64.b64decode(bytes(publicKey, 'utf-8'))
        RSAObj = RSA.importKey(publicKey_b)
        enc_data = RSAObj.encrypt(targetDate.encode('utf-8'), 32)
        return str(base64.b64encode(enc_data[0]), 'utf-8')

    def Decrypt(self,privateKey,targetData):
        privateKey_b = base64.b64decode(bytes(privateKey, 'utf-8'))
        RSAObj = RSA.importKey(privateKey_b)
        dec_data = RSAObj.decrypt(base64.b64decode(targetData))
        return str(dec_data, 'utf-8')

    def DigitalSignture(self,privateKey,targetData):

        privateKey_b = base64.b64decode(bytes(privateKey, 'utf-8'))
        RSAObj = RSA.importKey(privateKey_b)


        targetData_encode = targetData.encode('utf-8')
        hashObj = SHA256.new(targetData_encode)
        signer = PKCS1_v1_5.new(RSAObj)
        signature = signer.sign(hashObj)

        return str(base64.b64encode(signature), 'utf-8')

    def VerifyDigitalSignture(self,publicKey,targetData,signature):

        publicKey_byte = base64.b64decode(bytes(publicKey,'utf-8'))
        RSAObj = RSA.importKey(publicKey_byte)


        targetData_encode = targetData.encode('utf-8')
        hashObj = SHA256.new(targetData_encode)
        signature_byte = base64.b64decode(signature)
        verifier = PKCS1_v1_5.new(RSAObj)

        return verifier.verify(hashObj, signature_byte)

