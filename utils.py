#!/usr/bin/env python
# encoding: utf-8

import os
import ethereum


def GenerateRandomPrivateKey():
    return ethereum.utils.sha3(os.urandom(4096)).encode('hex')
