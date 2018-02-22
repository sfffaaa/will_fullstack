#!/usr/bin/env python3

import base64
from Crypto.Cipher import AES
from Crypto import Random

# reference: https://gist.github.com/swinton/8409454

_BS = 16


def _str_to_bytes(data):
    u_type = type(b''.decode('utf8'))
    if isinstance(data, u_type):
        return data.encode('utf8')
    return data


def _pad(s):
    return s + (_BS - len(s) % _BS) * _str_to_bytes(chr(_BS - len(s) % _BS))


def _unpad(s):
    return s[0:-ord(s[len(s) - 1:])]


def AESEncrypt(key, raw):
    raw = _pad(_str_to_bytes(raw))
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')


def AESDecrypt(key, enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[16:])).decode('utf-8')


if __name__ == '__main__':
    key = bytes.fromhex('0b610c1345cd058dd9c9d7496960d86b085488dc494de7a85d4a2ec6fc00b90a')
    print(len(key))
    raw = 'Yoyoyo test for me!!!'
    enc_data = AESEncrypt(key, raw)
    enc_data = AESEncrypt(key, enc_data)
    dec_data = AESDecrypt(key, enc_data)
    dec_data = AESDecrypt(key, dec_data)
    assert dec_data == raw
    print('dec success "{0}"'.format(raw))
