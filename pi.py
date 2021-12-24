import re

import requests
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import etree
from django.template.defaultfilters import striptags



headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def roominfostr(ridd):
    ridd=str(ridd)

    response = requests.get("https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id=" + ridd,
                            headers=headers, timeout=10)
    live_status = json.loads(response.text)['data']['room_info']['live_status']  # 开播状态 1为已开播
    room_id = json.loads(response.text)['data']['room_info']['room_id']
    uid = json.loads(response.text)['data']['room_info']['uid']
    title = json.loads(response.text)['data']['room_info']['title']
    description = json.loads(response.text)['data']['room_info']['description']
    live_start_time = json.loads(response.text)['data']['room_info']['live_start_time']
    online = json.loads(response.text)['data']['room_info']['online']

    # 使用time
    timeStamp = live_start_time
    timeArray = time.localtime(timeStamp)

    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    otherStyleTime = str(otherStyleTime)
    online = str(online)
    online = online + '人'
    room_id = str(room_id)
    uid = str(uid)
    description = str(description)
    description = striptags(description)

#     response = etree.HTML(text=description)
#     # print(dir(response))
#     # print(response.xpath('string(.)'))
#     line = response.xpath('string(.)')
#     # line = '<p>宁波大学</p>'

#     regex = r'</?p>'

#     result = re.sub(regex, "", line, re.I)

#     # print(result)

#     description = result

    if live_status == 1:
        live_status = '已开播'
    else:
        live_status = '未开播'
        otherStyleTime = ''

    roominfostr =  '本次直播主题：' + title + '\n' + '直播间简介：' + description   + '\n'+ '本次开播时间：' + otherStyleTime + '\n' + '当前直播人气：' + online + '\n' + '房间号：' + room_id + '\n' + '用户UID：' + uid + '\n' + '开播状态：' + live_status + '\n'

    print(roominfostr)
    return roominfostr


def roominfotitle(ridd):
    ridd = str(ridd)

    response = requests.get("https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id=" + ridd,
                            headers=headers, timeout=10)

    title = json.loads(response.text)['data']['room_info']['title']
    title=str(title)
    title=striptags(title)
    return title

