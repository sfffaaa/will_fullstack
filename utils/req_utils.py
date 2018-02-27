#!/usr/bin/env python3
# encoding: utf-8

from utils import myeth_utils
import json


def CheckCreateInput(num_signature, raw_data):
    num_signature = int(num_signature)
    if num_signature <= 0:
        raise IOError('number of signature fail {0} <= 0'.format(num_signature))


def _CheckPrivateKey(key):
    myeth_utils.PrivToAddr(key)
    if len(bytes.fromhex(key)) != 32:
        raise IOError('value {0} isn\t 32 bytes after convert to hex mode'.format(key))


def ConvertOtherPrivateKeysStr(other_private_keys_str):
    other_private_keys_dict = json.loads(other_private_keys_str)

    other_private_keys = myeth_utils.SortedPrivateKeys(other_private_keys_dict)
    return [bytes.fromhex(_) for _ in other_private_keys]


def _CheckReqPrivateAndOtherPrivateKey(my_private_key, other_private_keys_str):
    other_private_keys_dict = json.loads(other_private_keys_str)
    if not other_private_keys_dict:
        raise IOError('We don\'t have any other private keys')

    for k, v in other_private_keys_dict.items():
        _CheckPrivateKey(v)

    _CheckPrivateKey(my_private_key)


def CheckUpdateInput(my_private_key, other_private_keys_str, raw_data):
    _CheckReqPrivateAndOtherPrivateKey(my_private_key, other_private_keys_str)


def CheckRetrieveInput(my_private_key, other_private_keys_str):
    _CheckReqPrivateAndOtherPrivateKey(my_private_key, other_private_keys_str)


def CheckDeleteInput(my_private_key):
    _CheckPrivateKey(my_private_key)
