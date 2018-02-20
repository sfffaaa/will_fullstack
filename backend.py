#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, abort, request
import utils
import aes_utils
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

    my_private_key = utils.GenerateRandomPrivateKey()
    private_keys = [utils.GenerateRandomPrivateKey() for _ in range(num_signature)]

    encrypt_data = str(raw_data)
    for _ in [my_private_key] + private_keys:
        encrypt_data = aes_utils.AESEncrypt(my_private_key.decode('hex'), encrypt_data)

    # Write down data to ethereum block

    return json.dumps({
        'my_private_key': my_private_key,
        'others_private_key': dict(zip(range(num_signature), private_keys)),
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
    abort(400)
    return 'OK'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=30303, debug=True)
