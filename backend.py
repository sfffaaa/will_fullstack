#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask
import flask
from utils import myeth_utils
from utils import aes_utils
from utils import onchain_utils
from utils import req_utils
import json
import traceback
import sys

app = Flask(__name__)


@app.route('/')
def index():
    return flask.send_from_directory('static', 'index.html')


@app.route('/app/<path:filename>')
def serve_static(filename):
    return flask.send_from_directory('static', filename)


# Note the order is very important
@app.route("/will/create", methods=['POST'])
def create_will():
    num_signature = flask.request.form.get('num_sig')
    raw_data = flask.request.form.get('raw_data')
    try:
        req_utils.CheckCreateInput(num_signature, raw_data)
    except Exception:
        traceback.print_exc()
        exc_tuple = sys.exc_info()
        return json.dumps({
            'success': False,
            'error': str(exc_tuple[1]).strip()
        })

    num_signature = int(num_signature)

    my_private_key = myeth_utils.GenerateRandomPrivateKeyInBytes()
    private_keys = [myeth_utils.GenerateRandomPrivateKeyInBytes() for _ in range(num_signature)]

    encrypt_data = str(raw_data)
    for enc_private_key in private_keys:
        encrypt_data = aes_utils.AESEncrypt(enc_private_key, encrypt_data)

    onchain_utils.CreateWillToOnchain(myeth_utils.PrivToAddr(my_private_key),
                                      encrypt_data)

    return json.dumps({
        'success': True,
        'my_private_key': my_private_key.hex(),
        'others_private_key': dict(zip(range(num_signature), [_.hex() for _ in private_keys])),
        'encrypt_data': encrypt_data
    })


@app.route("/will/update", methods=['POST'])
def update_will():
    my_private_key = flask.request.form.get('my_private_key')
    raw_data = flask.request.form.get('raw_data')
    other_private_keys_dict = flask.request.form.get('others_private_key')
    try:
        req_utils.CheckUpdateInput(my_private_key, other_private_keys_dict, raw_data)
    except Exception:
        traceback.print_exc()
        exc_tuple = sys.exc_info()
        return json.dumps({
            'success': False,
            'error': str(exc_tuple[1]).strip()
        })

    other_private_keys = req_utils.ConvertOtherPrivateKeysStr(other_private_keys_dict)

    encrypt_data = str(raw_data)
    for enc_private_key in other_private_keys:
        encrypt_data = aes_utils.AESEncrypt(enc_private_key, encrypt_data)

    onchain_utils.UpdateWillToOnchain(myeth_utils.PrivToAddr(my_private_key),
                                      encrypt_data)

    return json.dumps({
        'success': True,
        'my_private_key': my_private_key,
        'others_private_key': other_private_keys_dict,
        'encrypt_data': encrypt_data
    })


@app.route("/will/delete", methods=['POST'])
def delete_will():
    my_private_key = flask.request.form.get('my_private_key')
    try:
        req_utils.CheckDeleteInput(my_private_key)
    except Exception:
        traceback.print_exc()
        exc_tuple = sys.exc_info()
        return json.dumps({
            'success': False,
            'error': str(exc_tuple[1]).strip()
        })

    onchain_utils.DeleteWillToOnchain(myeth_utils.PrivToAddr(my_private_key))
    return json.dumps({
        'success': True
    })


@app.route("/will/retrieve", methods=['POST'])
def retrieve_will():
    my_private_key = flask.request.form.get('my_private_key')
    other_private_keys_dict = flask.request.form.get('others_private_key')
    try:
        req_utils.CheckRetrieveInput(my_private_key, other_private_keys_dict)
    except Exception as e:
        traceback.print_exc()
        exc_tuple = sys.exc_info()
        return json.dumps({
            'success': False,
            'error': str(exc_tuple[1]).strip()
        })

    encrypt_data = onchain_utils.RetrieveWillToOnchain(myeth_utils.PrivToAddr(my_private_key))

    if not encrypt_data:
        return json.dumps({
            'success': True,
            'raw_data': ''
        })

    other_private_keys = req_utils.ConvertOtherPrivateKeysStr(other_private_keys_dict)

    try:
        for decrypt_private_key in other_private_keys:
            encrypt_data = aes_utils.AESDecrypt(decrypt_private_key, encrypt_data)
    except Exception:
        traceback.print_exc()
        exc_tuple = sys.exc_info()
        return json.dumps({
            'success': False,
            'error': str(exc_tuple[1]).strip()
        })

    return json.dumps({
        'success': True,
        'raw_data': encrypt_data
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=31313, debug=True)
