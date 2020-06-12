#!/usr/bin/env python3
#_*_coding:utf-8 _*_
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json
import sys
import re

pattern = re.compile('ItemID:(\d+)', re.S)
itemid = re.findall(pattern, sys.argv[3])[0]
graphs_url = "http://zabbix.xxxx.com/chart.php?period=3600&itemids%%5b%%5d=%s" % itemid #使用自己的zabbix地址
new_details = '%s 手机点击链接，右上角更多，用浏览器打开，先用浏览器登陆zabbix以后保存密码。' % graphs_url


def sign():
    timestamp = str(round(time.time() * 1000))
    secret = 'xxxx' #替换成自己的钉钉机器人密钥
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp,sign

headers = {'Content-Type': 'application/json;charset=utf-8'}
api_url = "https://oapi.dingtalk.com/robot/send?access_token=xxxx&timestamp=%s&sign=%s" % (sign()[0],sign()[1]) #替换成自己钉钉地址

def msg(Subject,Message,mobiles,mobiles2):
    json_text = {
        "msgtype": "text",
        "at": {
            "atMobiles": [
                mobiles,
                mobiles2
            ],
            "isAtAll": False
        },
        "text": {
            "content": Subject + '\n' + Message + '\n' + new_details
        }
    }
    x = requests.post(api_url, json.dumps(json_text), headers=headers).content
    return x

if __name__ == '__main__':
    Subject = str(sys.argv[2])
    Message = str(sys.argv[3])

    if 'xx' in Subject:  
        msg(Subject,Message,mobiles,mobiles1) #mobiles,mobiles1 替换成自己需要的手机号码
    elif 'xx' in Subject:
        msg(Subject,Message,mobiles,mobiles1)
    elif 'xx' in Subject:
        msg(Subject,Message,mobiles,mobiles1)
    else:
        msg(Subject,Message,mobiles,mobiles1)
