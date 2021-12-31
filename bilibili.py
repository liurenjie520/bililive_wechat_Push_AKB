# 获取哔哩哔哩直播的真实流媒体地址，默认获取直播间提供的最高画质
# qn=150高清
# qn=250超清
# qn=400蓝光
# qn=10000原画
import json
import time
import pi
import requests


class BiliBili:

    def __init__(self, rid):
        """
        有些地址无法在PotPlayer播放，建议换个播放器试试
        Args:
            rid:
        """
        rid = rid
        self.header = {
            'User-Agent': 'Mozilla/5.0 (iPod; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) CriOS/87.0.4280.163 Mobile/15E148 Safari/604.1',
        }
        # 先获取直播状态和真实房间号
        r_url = 'https://api.live.bilibili.com/room/v1/Room/room_init'
        param = {
            'id': rid
        }
        with requests.Session() as self.s:
            res = self.s.get(r_url, headers=self.header, params=param).json()
            time.sleep(2)
        if res['msg'] == '直播间不存在':
            raise Exception(f'房间号 {rid} {res["msg"]}')
        live_status = res['data']['live_status']
        time.sleep(2)
        if live_status != 1:
            raise Exception(f'房间号 {rid} 未开播')
        self.real_room_id = res['data']['room_id']

    def get_real_url(self, current_qn: int = 10000) -> dict:
        url = 'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo'
        param = {
            'room_id': self.real_room_id,
            'protocol': '0,1',
            'format': '0,1,2',
            'codec': '0,1',
            'qn': current_qn,
            'platform': 'h5',
            'ptype': 8,
        }
        res = self.s.get(url, headers=self.header, params=param).json()
        stream_info = res['data']['playurl_info']['playurl']['stream']
        time.sleep(2)
        qn_max = 0

        for data in stream_info:
            accept_qn = data['format'][0]['codec'][0]['accept_qn']
            time.sleep(2)
            for qn in accept_qn:
                qn_max = qn if qn > qn_max else qn_max
        if qn_max != current_qn:
            param['qn'] = qn_max
            res = self.s.get(url, headers=self.header, params=param).json()
            time.sleep(2)
            stream_info = res['data']['playurl_info']['playurl']['stream']

        stream_urls = {}
        # flv流无法播放，暂修改成获取hls格式的流，
        for data in stream_info:
            format_name = data['format'][0]['format_name']
            if format_name == 'ts':
                base_url = data['format'][-1]['codec'][0]['base_url']
                url_info = data['format'][-1]['codec'][0]['url_info']
                for i, info in enumerate(url_info):
                    host = info['host']
                    extra = info['extra']
                    time.sleep(4)
                    stream_urls[f'[线路{i + 1}]:'] = f'{host}{base_url}{extra}'
                    time.sleep(4)
                break
        return stream_urls


def get_real_url(rid):
    try:
        bilibili = BiliBili(rid)
        return bilibili.get_real_url()


    except Exception as e:
        print('Exception：', e)
        return False



def binali(rid):

    rel = get_real_url(rid)
    # 21314309
    s = ''
    p = ''

    for key in rel:
        xl = key  # 拿到key
        dz = rel[key]  # 拿到value，实现对value的遍历
        s = '\n' + xl + '\n' + dz + '\n'
        time.sleep(2)
        p += s
        time.sleep(2)

    return p




#
# if __name__ == '__main__':
#     # print(binali())
#     try:
#         fasongneir3 = str(binali(921076))
#
#         imgpost = 'https://push.bot.qw360.cn/send/e54011f0-f9aa-11eb-806f-9354f453c154'
#         headers = {'Content-Type': 'application/json'}
#
#         infoo = pi.roominfostr(921076)
#         infoo = str(infoo)
#
#         fasongneir = infoo + '真实地址:\n' + fasongneir3
#         postdata = json.dumps({"msg": fasongneir})
#         time.sleep(4)
#         repp = requests.post(url=imgpost, data=postdata, headers=headers)
#     except:
#         print("未开播")




def bililive(roomid):

    try:

        fasongneir3 = str(binali(roomid))

        imgpost = 'https://push.bot.qw360.cn/send/e54011f0-f9aa-11eb-806f-9354f453c154'
        headers = {'Content-Type': 'application/json'}

        infoo = pi.roominfostr(roomid)
        infoo = str(infoo)

        fasongneir = infoo + '真实地址:\n' + fasongneir3
        postdata = json.dumps({"msg": fasongneir})
        time.sleep(4)
        repp = requests.post(url=imgpost, data=postdata, headers=headers)
    except:
        print("未开播")
