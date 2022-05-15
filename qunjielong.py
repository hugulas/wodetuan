import pandas as pd
import requests
import json
import constant
from mdutils.mdutils import MdUtils

mdFile = MdUtils(file_name=constant.TITLE, title=constant.TITLE)


def getStock(tuanzhang):
    print('### 获取团长: {} 物资列表'.format(tuanzhang["ghName"]))
    myUrl = 'https://apipro.qunjielong.com/ghome-feed/ghome_feed/query_ghome_feed_v2'
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
    ret = requests.post(url=myUrl, headers=headers,
                        json={"page": 1, "pageSize": 100, "ghId": tuanzhang["ghId"], "ghType": tuanzhang["ghType"]})
    if ret.status_code == 200:
        myRet = json.loads(ret.text)
        searchData = myRet['data']
        items = searchData["feedItemDTOList"]
        goods = []
        for item in items:
            itemContent = item["actItemDTO"]
            status = itemContent["activityStatus"]
            statusStr = "未知状态"
            if status == 10:
                statusStr = "接龙中"
            elif status == 5:
                statusStr = "结束"
            if "actInfoTextStr" in itemContent:
                actInfoTextStr = itemContent["actInfoTextStr"]
            else:
                actInfoTextStr = ""
            good = {"团长": itemContent["nickName"], '货物': itemContent["activityName"], '描述': actInfoTextStr,
                    '状态': statusStr, '状态码': itemContent["activityStatus"]}
            goods.append(good)
        return goods
    else:
        print("Error {}".format(ret.text))
        return []


def list():
    print('### 搜索团长列表')
    myUrl = 'https://apipro.qunjielong.com/ghome-major/gh_home/follow/subscrib_gh_home_list?page=1&pageSize=100'
    headers = {
        'Host': 'apipro.qunjielong.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': AUTHORIZATION,
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


def get_goods_df():
    # tuanzhangs = list()
    # print(tuanzhangs)
    entities = constant.QUNTUANZHANG
    goods_all = []
    for tuanzhang in entities:
        goods = getStock(tuanzhang)
        goods_all += goods
    goods_df = pd.DataFrame.from_dict(goods_all)
    goods_df["来源"] = "群接龙"
    goods_df = goods_df.sort_values("团长")
    return goods_df


def print_row(row):
    mdFile.new_header(level=2, title='货物: {}'.format(row["货物"]))
    mdFile.new_line(row["描述"])


def to_markdown(df):
    df = df.sort_values("团长")
    df = df[df['状态码'] == 10]
    for name, sub_df in df.groupby("团长"):
        mdFile.new_header(level=1, title='{}团'.format(name))
        sub_df.apply(print_row, axis=1)
    mdFile.new_table_of_contents(table_title='团长清单', depth=1)
    mdFile.create_md_file()


if __name__ == '__main__':
    goods_df = get_goods_df()
    to_markdown(goods_df)
    with pd.ExcelWriter('{}.xlsx'.format(constant.TITLE)) as writer:
        goods_df.to_excel(writer, sheet_name="所有团购物资")
        goods_df[goods_df['状态码'] == 10].to_excel(writer, sheet_name="可购买团购物资")
        pd.DataFrame.from_dict(constant.QUNTUANZHANG)[["ghName"]].to_excel(writer, sheet_name="群接龙关注的团长")
