import pandas as pd
import requests
import json

# import pandas
# import openpyxl
import constant


def list_qun():
    print('### 搜索团长列表')
    myUrl = 'https://apipro.qunjielong.com/ghome-major/gh_home/follow/subscrib_gh_home_list?page=1&pageSize=100'
    headers = {
        'Host': 'apipro.qunjielong.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': constant.AUTHORIZATION,
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
        'appid': 'wx059cd327295ab444'
    }
    ret = requests.get(url=myUrl, headers=headers)
    if ret.status_code == 200:
        myRet = json.loads(ret.text)
        searchData = myRet['data']
        return searchData
    else:
        print("Error {}".format(ret.text))
        return []





if __name__ == '__main__':
    tuanzhangs = list_qun()
    print("*** 群接龙团长们: ")
    print(tuanzhangs["entityList"])
