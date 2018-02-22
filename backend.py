#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask, abort, request
import myeth_utils
import aes_utils
import onchain_utils
import json

app = Flask(__name__)


@app.route('/')
def index():
    return "<p>Yaaaaa! You can encrypt all data here!!</p>"


# Note the order is very important
@app.route("/will/create", methods=['POST'])
def create_will():
    num_signature = int(request.form.get('num_sig'))
    raw_data = request.form.get('raw_data')

    my_private_key = myeth_utils.GenerateRandomPrivateKeyInBytes()
    private_keys = [myeth_utils.GenerateRandomPrivateKeyInBytes() for _ in range(num_signature)]

    encrypt_data = str(raw_data)
    for enc_private_key in private_keys:
        encrypt_data = aes_utils.AESEncrypt(enc_private_key, encrypt_data)

    onchain_utils.CreateWillToOnchain(myeth_utils.PrivToAddr(my_private_key),
                                      encrypt_data)

    return json.dumps({
        'my_private_key': my_private_key.hex(),
        'others_private_key': dict(zip(range(num_signature), [_.hex() for _ in private_keys])),
        'encrypt_data': encrypt_data
    })


@app.route("/will/update", methods=['POST'])
def update_will():
    abort(400)
    return 'OK'


@app.route("/will/delete", methods=['POST'])
def delete_will():
    abort(400)
    return 'OK'


@app.route("/will/retrieve", methods=['POST'])
def retrieve_will():
    my_private_key = request.form.get('my_private_key')
    encrypt_data = onchain_utils.RetrieveWillToOnchain(myeth_utils.PrivToAddr(my_private_key))

    other_private_keys_dict = json.loads(request.form.get('others_private_key'))

    other_private_keys = myeth_utils.SortedPrivateKeys(other_private_keys_dict)
    other_private_keys = [bytes.fromhex(_) for _ in other_private_keys]

    for decrypt_private_key in other_private_keys:
        encrypt_data = aes_utils.AESDecrypt(decrypt_private_key, encrypt_data)

    return json.dumps({
        'raw_data': encrypt_data
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=31313, debug=True)
