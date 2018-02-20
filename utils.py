#!/usr/bin/env python3
# encoding: utf-8

import os
import ethereum


def GenerateRandomPrivateKeyInBytes():
    return ethereum.utils.sha3(os.urandom(4096))
