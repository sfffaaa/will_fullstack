#!/usr/bin/env python3
# encoding: utf-8

import requests
import json


RAW_DATA = 'aabbcc'

# test create
create_data = {
    'num_sig': 3,
    'raw_data': RAW_DATA
}
r = requests.post('http://localhost:31313/will/create', data=create_data)
create_resp = json.loads(r.text)

# # test update
# update_data = {
#     'num_sig': 3,
#     'raw_data': 'aabbcc',
#     'private_sig': '1234567890'
# }
# print(requests.post('http://localhost:31313/will/update', data=update_data))
#
# # test delete
# delete_data = {
#     'private_sig': '1234567890'
# }
# print(requests.post('http://localhost:31313/will/delete', data=delete_data))
#
#
# test retrieve
retrieve_data = {
    'my_private_key': create_resp['my_private_key'],
    'others_private_key': json.dumps(create_resp['others_private_key'])
}
r = requests.post('http://localhost:31313/will/retrieve', data=retrieve_data)
retrieve_resp = json.loads(r.text)
assert RAW_DATA == retrieve_resp['raw_data']

print(retrieve_resp)

# test delete
delete_data = {
    'my_private_key': create_resp['my_private_key'],
}
r = requests.post('http://localhost:31313/will/delete', data=delete_data)
assert 'OK' == r.text

retrieve_data = {
    'my_private_key': create_resp['my_private_key'],
    'others_private_key': json.dumps(create_resp['others_private_key'])
}
r = requests.post('http://localhost:31313/will/retrieve', data=retrieve_data)
retrieve_resp = json.loads(r.text)
assert '' == retrieve_resp['raw_data']
