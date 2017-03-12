from itsdangerous import TimestampSigner, TimedJSONWebSignatureSerializer as Serializer
import hashlib
from Helpers.RSATool import *
from Helpers.AESTool import *

import json, SystemConfig

class SecureManager:

    def __init__(self,plateFormCode):
        plateFormAccount = PaymentGatwayManager.GetPlateFormAccount(plateFormCode)
        self.AESCipher = AESCipher(plateFormAccount['AES'])
        self.privateKey = plateFormAccount['RSA']['privateKey']
        self.publicKey = plateFormAccount['RSA']['privateKey']

    def ReceiverProcess(self,encString):
        origionalJsonObj = json.dumps(RSATool.Decrypt(SystemConfig.PaymentGatwayKey['RSA']['privateKey'], encString))
        targetData = self.AESCipher.decrypt(origionalJsonObj['args'])
        status = RSATool.VerifyDigitalSignture(self.privateKey , targetData, origionalJsonObj['checkValue'])
        if status:
            return True, json.dumps(targetData)
        else:
            return False

    def ReturnProcess(self,returnString):

        aesString = self.AESCipher.decrypt(returnString)
        rsaSignture = RSATool.DigitalSignture(SystemConfig.PaymentGatwayKey['RSA']['privateKey'], returnString)

        returnObj = {
            'arg': aesString,
            'checkValue': rsaSignture
        }
        return RSATool.Encrypt(self.privateKey , json.dumps(returnObj))