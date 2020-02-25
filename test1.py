import json

import requests


data = {}
payload  = {}
payload['payload'] = data
data['id'] = 2
data['lastname'] = '1'
data['firstname'] = '2'
data['patr'] = '3'
data['email'] = '3'
data['birthday'] = '4'
data['nickname'] = '5'
data['password'] = '123321'
print(payload)
print(requests.put('http://127.0.0.1:5000/v1/user/2', payload ,headers=None).text)