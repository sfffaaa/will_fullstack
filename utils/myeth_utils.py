#!/usr/bin/env python3
# encoding: utf-8

import os
import ethereum


def GenerateRandomPrivateKeyInBytes():
    return ethereum.utils.sha3(os.urandom(4096))


def PrivToAddr(private_key):
    print(private_key)
    return ethereum.utils.privtoaddr(private_key)


def SortedPrivateKeys(other_private_keys_dict, reverse=True):
    wait_sorted_pairs = [(int(k), v) for k, v in other_private_keys_dict.items()]
    sorted_pairs = sorted(wait_sorted_pairs, key=lambda x: x[0], reverse=reverse)
    return [_[1] for _ in sorted_pairs]
