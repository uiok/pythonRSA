from Manager.SecureManager import *
from Helpers.RSATool import *
from flask import *

app = Flask(__name__)
app.secret_key = "nkjbgbggvhgvh"
app.config





@app.route('/', methods=['GET'])
def FirstProcess():

    publicKeyA,privateKeyA = RSATool().Generator()

    publicKeyB, privateKeyB = RSATool().Generator()

    return render_template('/form.html', **locals())


@app.route('/process/ecrypt', methods=['POST'])
def SecondProcess():

    try:
        publicKeyB =  request.json.get('publicKeyB')
        privateKeyA =  request.json.get('privateKeyA')
        pure = request.json.get('pure')
        targetData, rsaSignture, rsaStringForaes = SecureManager().ReturnProcess(privateKeyA,publicKeyB,pure)

        return json.dumps({
            'content':targetData,
            'rsaSignture':rsaSignture,
            'rsaStringForaes':rsaStringForaes
        })
    except Exception as e:
        return None


@app.route('/process/decrypt', methods=['POST'])
def ThirdProcess():

    try:
        publicKeyA =  request.json.get('publicKeyA')
        privateKeyB =  request.json.get('privateKeyB')
        content = request.json.get('content')
        rsaSignture = request.json.get('rsaSignture')
        rsaStringForaes = request.json.get('rsaStringForaes')

        status,targetData= SecureManager().ReceiverProcess(privateKeyB,publicKeyA,content,rsaSignture,rsaStringForaes)

        return json.dumps({
            'descript':targetData
        })
    except Exception as e:
        return None


if __name__ == '__main__':
    app.run(port=5000, debug=True)
