# -*-coding=utf-8-*-
__author__ = 'aqua'

import requests
import json

response = requests.get('http://webapi.http.zhimacangku.com/getip?num=5&type=2&pro=0&city=0&yys=100017&port=11&time=4&ts=1&ys=1&cs=1&lb=1&sb=0&pb=45&mr=1&regions=310000,320000,330000,350000,440000')
result = json.loads(response.text)
print(result)

