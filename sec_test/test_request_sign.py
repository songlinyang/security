
import unittest
import requests
import json
import time
import hashlib
"""这是一个md5鉴权的接口测试"""


class AddEventTest(unittest.TestCase):

    def setUp(self):
        #思路：1.客户端需要有appkey 2.需要客户端当前时间戳clienttime 3.需要客户端通过appkey+clienttime生成的md5加密串
        self.url = "http://127.0.0.1:8000/api/add_event_sec"
        #1.
        appkey ="&Guest-Bugmaster"
        #2.
        now_time = time.time()
        self.client_now_time = str(now_time).split('.')[0]
        #3.签名
        md5 = hashlib.md5()
        sign_str = self.client_now_time + appkey
        sign_byte_utf8 = sign_str.encode(encoding="utf-8")
        md5.update(sign_byte_utf8)
        self.sign_md5 = md5.hexdigest()



    def tearDown(self):
        pass

    def test_add_event_timeout(self):
        """签名参数超时"""
        timeout = str(int(self.client_now_time)-1000)
        pay_load = {
            "name": "某某xxx1的发布会",
            "address": "深圳",
            "start_time": "2019-3-17 21:44:03",
            "time": timeout,
            "sign": self.sign_md5
        }
        req = requests.post(self.url,json=pay_load)
        result = req.json()
        print(result)

    def atest_add_event_ok(self):
        """签名参数正确"""
        now_time = str(int(self.client_now_time))
        pay_load = {
            "name":"某某的发布会",
            "address":"深圳",
            "start_time":"2019-3-17 21:44:03",
            "time":now_time,
            "sign":self.sign_md5
        }
        req = requests.post(self.url,json=pay_load)
        result = req.json()
        print(result)
