from Manager.SecureManager import *
from Helpers.RSATool import *
from flask import *

import SystemConfig, uuid
payment_url = Blueprint('payment_url', __name__)



@payment_url.route('/', methods=['GET'])
def FirstProcess():

    publicKey,privateKey = RSATool().Generator()

    return render_template('/form.html',**local)


@payment_url.route('/process', methods=['POST'])
def SecondProcess():

    try:
        secureManager = SecureManager(json_get('plateFormCode'))
        status, targetData = secureManager.ReceiverProcess(json_get('content'))
        if status:
            pureString = ''

            plateFormCustomerKeyTable = PaymentGatwayManager.GetPlateFormCustomerKeyTable(targetData['customerId'])
            cashier = CashierTool(targetData['thirdPlateFormCode'],plateFormCustomerKeyTableObj).GetCashier()

            if '信用卡':
                pureString = cashier.CreditCradProcess()
            elif 'ATM':
                pureString = cashier.ATMProcess()
            elif '超商':
                pureString = cashier.CreditCradProcess()
            else:
                raise Exception
            decString = secureManager.ReturnProcess(pureString)

            return json.dumps(ProcessSuccess(decString))
        else:
            raise Exception

    except Exception:
        return json.dumps(ProcessError())






