from web3 import Web3, IPCProvider
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

pragma solidity ^0.4.17;

contract Will {

    mapping(string => string) userData;

    function Retrieve(string user_addr) public constant returns (string data) {
        data = userData["asdf"];
    }

    function Create(string user_addr, string data) public {
        userData[user_addr] = data;
    }

    function Update(string user_addr, string data) public {
        Create(user_addr, data);
    }

    function Delete(string user_addr) public {
        delete userData[user_addr];
    }
}'''

compiled_sol = compile_source(contract_source_code)  # Compiled source code
contract_interface = compiled_sol['<stdin>:Will']

# web3.py instance
w3 = Web3(IPCProvider('/Users/jaypan/private-eth/test1/node1/geth.ipc'))

# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 910000})
w3.miner.start(1)

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
import time
time.sleep(30)
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']
w3.miner.stop()

# Contract instance in concise mode
contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('Contract value: {}'.format(contract_instance.Retrieve('aaa')))
# contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
# print('Setting value to: Nihao')
# time.sleep(30)
# print('Contract value: {}'.format(contract_instance.greet()))
