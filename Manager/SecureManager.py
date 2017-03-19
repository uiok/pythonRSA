from itsdangerous import TimestampSigner, TimedJSONWebSignatureSerializer as Serializer
import hashlib
from Helpers.RSATool import *
from Helpers.AESTool import *

import json, SystemConfig

class SecureManager:



    def ReceiverProcess(self,privateKeyB,publicKeyA,encString,signture,aesString):

        rasTool = RSATool()
        aecTool = AESCipher()
        # 設私鑰
        aesDecString = rasTool.Decrypt(privateKeyB, aesString)
        # aes內文
        targetData = aecTool.decrypt(encString,aesDecString)
        # 金公鑰
        status = rasTool.VerifyDigitalSignture(publicKeyA , targetData, signture)

        if status:
            return True, json.loads(targetData)['arg']
        else:
            return False

    def ReturnProcess(self,privateKeyA,publicKeyB,returnString):

        rasTool = RSATool()
        aecTool = AESCipher()
        randomeAESKey = aecTool.GenerateKey()
        returnObj = {
            'arg': returnString
        }

        targetData = aecTool.encrypt(json.dumps(returnObj), randomeAESKey)
        # 設公鑰
        rsaStringForaes = rasTool.Encrypt(publicKeyB,randomeAESKey)
        #金私鑰
        rsaSignture = rasTool.DigitalSignture(privateKeyA, json.dumps(returnObj))

        return str(targetData, 'utf-8'), rsaSignture, rsaStringForaes


