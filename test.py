#!/usr/bin/env python3
# encoding: utf-8

import requests

# test create
create_data = {
    'num_sig': 3,
    'raw_data': 'aabbcc'
}
r = requests.post('http://localhost:30303/will/create', data=create_data)
print(r.text)
assert r.text == 'OK'

# test update
update_data = {
    'num_sig': 3,
    'raw_data': 'aabbcc',
    'private_sig': '1234567890'
}
print(requests.post('http://localhost:30303/will/update', data=update_data))

# test delete
delete_data = {
    'private_sig': '1234567890'
}
print(requests.post('http://localhost:30303/will/delete', data=delete_data))


# test retrieve
retrieve_data = {
    'private_sig': '1234567890'
}
print(requests.post('http://localhost:30303/will/retrieve', data=retrieve_data))
