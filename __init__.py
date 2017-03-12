from Manager.SecureManager import *
from Helpers.RSATool import *
from flask import *

app = Flask(__name__)
app.secret_key = "nkjbgbggvhgvh"
app.config





@app.route('/', methods=['GET'])
def FirstProcess():

    publicKey,privateKey = RSATool().Generator()

    return render_template('/form.html', **locals())


# @app.route('/process', methods=['POST'])
# def SecondProcess():
#
#     try:
#         secureManager = SecureManager(json_get('plateFormCode'))
#         status, targetData = secureManager.ReceiverProcess(json_get('content'))
#         if status:
#             pureString = ''
#
#             plateFormCustomerKeyTable = PaymentGatwayManager.GetPlateFormCustomerKeyTable(targetData['customerId'])
#             cashier = CashierTool(targetData['thirdPlateFormCode'],plateFormCustomerKeyTableObj).GetCashier()
#
#             if '信用卡':
#                 pureString = cashier.CreditCradProcess()
#             elif 'ATM':
#                 pureString = cashier.ATMProcess()
#             elif '超商':
#                 pureString = cashier.CreditCradProcess()
#             else:
#                 raise Exception
#             decString = secureManager.ReturnProcess(pureString)
#
#             return json.dumps(ProcessSuccess(decString))
#         else:
#             raise Exception
#
#     except Exception:
#         return json.dumps(ProcessError())




if __name__ == '__main__':
    app.run(port=5000, debug=True)
