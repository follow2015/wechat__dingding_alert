#_*_coding:utf-8 _*_
import requests
import json
from tenacity import *
import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler

LOG_FILE = "/var/log/zabbix_wechat/zabbix_alert.log"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = TimedRotatingFileHandler(LOG_FILE,when='D',interval=1,backupCount=30)
datefmt = '%Y-%m-%d %H:%M:%S'
format_str = '%(asctime)s %(levelname)s %(message)s '
formatter = logging.Formatter(format_str, datefmt)
fh.setFormatter(formatter)
logger.addHandler(fh)

def access_token(Corpid,Secret):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    querystring = {"corpid": Corpid, "corpsecret": Secret}
    response = requests.request("GET", url, params=querystring)
    if response.json()['errcode'] != 0:
        return False
    else:
        access_token = response.json()['access_token']
        with open('/tmp/zabbix_access_token.json','w') as file:
            file.write(response.text)
            file.close()
        return access_token

def is_ok(value):
     return value is False

@retry(retry=retry_if_result(is_ok),stop=stop_after_attempt(4),wait=wait_fixed(2))
def SendMessage(Subject,Content):
    try:
        file = open('/tmp/zabbix_access_token.json','r')
        Token = json.load(file)['access_token']
        file.close()
    except:
        Token = access_token()

    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
    querystring = {"access_token": Token}
    payload = {
        "toparty": 部门ID,                                #https://work.weixin.qq.com/api/doc/90000/90135/90665#secret
        "msgtype": "text",
        "agentid": 应用ID,                                #https://work.weixin.qq.com/api/doc/90000/90135/90665#secret
        "text":
        {
              "content": Subject + '\n' + Content
        },
        "safe": 0
    }
    response = requests.post(url, data=json.dumps((payload),ensure_ascii=False).encode("utf-8").decode("latin1"), params=querystring)
    if response.json()["errcode"] == 40014 or response.json()["errcode"] == 42001:
        file = '/tmp/zabbix_access_token.json'
        if os.path.exists(file):
            os.remove(file)
        else:
            access_token()
        return False
    elif response.json()["errcode"] != 0:
        return False
    else:
        return response.json()

if __name__ == '__main__':
    Subject = str(sys.argv[2])
    Content = str(sys.argv[3])
    Corpid = "企业ID"                                #https://work.weixin.qq.com/api/doc/90000/90135/90665#corpid
    Secret = "应用密钥"                              #https://work.weixin.qq.com/api/doc/90000/90135/90665#secret
    logging.info(SendMessage(Subject,Content))
