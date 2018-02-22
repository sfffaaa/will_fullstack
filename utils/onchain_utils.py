#!/usr/bin/env python3
# encoding: utf-8


from web3 import Web3
from web3.contract import ConciseContract
import configparser
import json
import os
import time

CONFIG_PATH = 'etc/config.conf'
MINER_WAIT_TIME = 3


def _GetChainConfig(section, key):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config.get(section, key)


def _GetContractInfo():
    file_path = _GetChainConfig('Output', 'file_path')
    file_path = os.path.abspath(file_path)
    with open(file_path) as f:
        contract_info = json.load(f)
    return contract_info


def CreateWillToOnchain(public_key, encrypt_data):
    print('==== CreateWillToOnchain start ====')

    file_ipc = _GetChainConfig('Ethereum', 'file_ipc')
    w3 = Web3(Web3.IPCProvider(file_ipc))

    contract_info = _GetContractInfo()
    contract_abi = contract_info['abi']
    contract_address = contract_info['address']

    contract_inst = w3.eth.contract(contract_address,
                                    abi=contract_abi,
                                    ContractFactoryClass=ConciseContract)
    tx_hash = contract_inst.Create(public_key, encrypt_data,
                                   transact={'from': w3.eth.accounts[0]})

    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    w3.miner.start(1)
    retry_time = 0
    while not tx_receipt and retry_time < 10:
        print('    wait for miner!')
        time.sleep(MINER_WAIT_TIME)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        retry_time += 1

    w3.miner.stop()
    if not tx_receipt:
        raise IOError('still cannot get contract result')

    print(tx_receipt)
    print('==== CreateWillToOnchain finish ====')


def RetrieveWillToOnchain(public_key):
    print('==== RetrieveWillToOnchain start ====')

    file_ipc = _GetChainConfig('Ethereum', 'file_ipc')
    w3 = Web3(Web3.IPCProvider(file_ipc))

    contract_info = _GetContractInfo()
    contract_abi = contract_info['abi']
    contract_address = contract_info['address']
    contract_inst = w3.eth.contract(contract_address,
                                    abi=contract_abi,
                                    ContractFactoryClass=ConciseContract)
    retrieve_data = contract_inst.Retrieve(public_key)
    print('==== RetrieveWillToOnchain finish ====')
    return retrieve_data


if __name__ == '__main__':
    pass
