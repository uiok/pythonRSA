from itsdangerous import TimestampSigner, TimedJSONWebSignatureSerializer as Serializer
import hashlib
from Helpers.RSATool import *
from Helpers.AESTool import *

import json, SystemConfig

class SecureManager:



    def ReceiverProcess(self,privateKeyB,publicKeyA,encString,signture,aesString):

        rasTool = RSATool()
        aecTool = AESCipher()

        aesDecString = rasTool.Decrypt(privateKeyB, aesString)

        targetData = aecTool.decrypt(encString,aesDecString)

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

        rsaStringForaes = rasTool.Encrypt(publicKeyB,randomeAESKey)

        rsaSignture = rasTool.DigitalSignture(privateKeyA, json.dumps(returnObj))

        return str(targetData, 'utf-8'), rsaSignture, rsaStringForaes


