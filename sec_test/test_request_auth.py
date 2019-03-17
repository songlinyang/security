__author__ = "slyang"
"""这是一个【增加用户认证接口】的测试用例集"""

import requests
import unittest
import json

class GetEventListTest(unittest.TestCase):

    # def setUpClass(cls):
    #     pass
    #
    # def tearDownClass(cls):
    #     pass


    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/get_all_event_sec"

    def tearDown(self):
        pass

    """
    认证接口的测试用例：
    1/用户认证用户密码为空，不能正常登陆
    2/用户认证用户密码错误，不能正常登陆
    3/认证通过，发布会id正确，正常查询出对应id的发布会信息
    4/认证通过，发布会name正确，正常查询出对应name的发布会信息
    5/认证通过，发布会id/name不传，提示必传参数有误
    6/认证通过，发布会id/name均为空，提示必传参数不能为空
    
    
    """
    def test_get_event_list_auth_null(self):
        '''认证参数为空'''
        data_load = {
            "eid":1
        }
        req = requests.get(url=self.url,params=data_load)
        result = req.json()
        print(result)
        self.assertEqual(result['status'],100306)
        self.assertEqual(result['message'],"user auth null")


    def test_get_event_list_auth_error(self):
        '''认证参数有误'''
        data_load = {
            "eid":1
        }
        req = requests.get(url=self.url,params=data_load,auth=("error","1234"))
        result = req.json()
        print(result)
        self.assertEqual(result['status'],100307)
        self.assertEqual(result['message'],'user auth fail')

    def test_get_event_list_auth_ok_eventID(self):
        '''认证通过，发布会id正确，正常查询出对应id的发布会信息'''
        data_load = {
            "eid": 1
        }
        req = requests.get(url=self.url, params=data_load,auth=("admin","admin123456"))
        result = req.json()
        print(result)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['data']['name'],'小米MIX4发布会')

    def atest_get_event_list_auth_ok_eventName_ok(self):
        pass

    def atest_get_event_list_auth_ok_idName_null(self):
        pass

    def atest_get_event_list_auth_ok_idName_error(self):
        pass

