from django.test import TestCase
from datetime import datetime
from guest_app.models import Event, Guest
from django.contrib.auth.models import User
import unittest

# Create your tests here.
# django项目如何测试？

class TestModels(TestCase):

    def setUp(self):
        Event.objects.create(name="测试发布会", status=True,
                             limit=1000, address="北京",
                             start_time=datetime(2019, 8, 10, 14, 0, 0))

    def test_event_select(self):
        """查询"""
        event = Event.objects.get(name="测试发布会")
        self.assertEqual(event.address, "北京")

    def test_event_delete(self):
        """删除"""
        event = Event.objects.get(name="测试发布会")
        event.delete()
        event = Event.objects.filter(name="测试发布会")
        print(len(event))
        self.assertEqual(len(event), 0)

    def test_event_update(self):
        """更新"""
        event = Event.objects.get(name="测试发布会")
        event.address = "上海"
        event.save()
        event = Event.objects.get(name="测试发布会")
        print(event.address)
        self.assertEqual(event.address, "上海")

    def test_event_create(self):
        """创建"""
        Event.objects.create(name="创建发布会", status=True,
                             limit=1000, address="北京",
                             start_time=datetime(2019, 8, 10, 14, 0, 0))
        event = Event.objects.get(name="创建发布会")
        print(event.address)
        print(event.start_time)
        self.assertEqual(event.address, "北京")
        self.assertEqual(event.start_time, datetime(2019, 8, 10, 14, 0))


class TestIndex(TestCase):

    def test_index_page_renders_index_template(self):
        ''' 断言是否用给定的index.html模版响应'''
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class TestLoginAction(TestCase):

    def setUp(self):
        User.objects.create_user('error', 'admin@mail.com', 'error123')
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    # @unittest.skip("这是正确的跳过用例的方法")
    def test_username_password_null(self):
        '''用户名密码空'''
        test_data = {"username": "", "password": ""}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 200)
        resp_html = response.content.decode(encoding="utf-8")
        self.assertIn("用户名或者密码不能为空", resp_html)

    def test_username_password_error(self):
        '''用户名密码错误'''
        test_data = {"username": "error", "password": "error456"}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 200)
        resp_html = response.content.decode(encoding="utf-8")
        self.assertIn("用户名或者密码错误", resp_html)

    def test_success(self):
        '''登录成功'''
        test_data = {"username": "admin", "password": "admin123456"}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code, 302)

class TestEventMange(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name="小米8发布会", limit=2000, address='北京',
                             status=1, start_time='2018-5-10 12:30:00')
        test_data = {"username": "admin", "password": "admin123456"}
        self.client.post('/login_action/', data=test_data)
        # 测试接口：URL路径， 请求方法get/post, 参数类型

    def test_event_manage(self):
        '''发布会管理页面'''
        response = self.client.get('/event_manage/')
        self.assertEqual(response.status_code, 200)
        resp_html = response.content.decode(encoding="utf-8")
        self.assertIn("欢迎", resp_html)
        self.assertIn("退出", resp_html)
        self.assertIn("小米8发布会", resp_html)

    def test_search_name(self):
        '''搜索发布会名称'''
        response = self.client.get('/event_manage/search_name/',
                                   data={"name": "小米8"})
        self.assertEqual(response.status_code, 200)
        resp_html = response.content.decode(encoding="utf-8")
        self.assertIn("欢迎", resp_html)
        self.assertIn("退出", resp_html)
        self.assertIn("小米8发布会", resp_html)


class TestSignAction(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="小米8发布会", limit=2000, address='北京',
                             status=1, start_time='2018-8-10 12:30:00')
        Event.objects.create(id=2, name="oneplus4", limit=2000, address='shenzhen',
                             status=1, start_time='2017-6-10 12:30:00')
        Guest.objects.create(real_name="alen", phone=18611001100,
                             email='alen@mail.com', sign=1, event_id=1)
        Guest.objects.create(real_name="una", phone=18611001101,
                             email='una@mail.com', sign=0, event_id=2)
        test_data = {"username": "admin", "password": "admin123456"}
        self.client.post('/login_action/', data=test_data)
        # 测试接口：URL路径， 请求方法get/post, 参数类型

    def test_phone_error(self):
        '''手机号不存在'''
        response = self.client.post('/sign_action/1',
                                    data={"phone": "13413414134"})
        self.assertEqual(response.status_code, 200)
        resp_html = response.content.decode(encoding="utf-8")
        self.assertIn("phone error", resp_html)

    def test_event_or_guest_error(self):
        '''发布会或者嘉宾错误
        18611001101 所属发布会id=2
        '''
        response = self.client.post('/sign_action/1',
                                    data={"phone": "18611001101"})
        self.assertEqual(response.status_code, 200)
        resp_html = response.content.decode(encoding="utf-8")
        self.assertIn("event id or phone error.", resp_html)

    def test_guest_has_sign(self):
        '''嘉宾已经签到
        18611001100 嘉宾sign=1(1表示已签到)
        '''
        response = self.client.post('/sign_action/1',
                                    data={"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        resp_html = response.content.decode(encoding="utf-8")
        self.assertIn("user has sign in.", resp_html)

    def test_sign_success(self):
        '''签到成功
        event_id=2, sign=0
        '''
        response = self.client.post('/sign_action/2',
                                    data={"phone": "18611001101"})
        self.assertEqual(response.status_code, 200)
        resp_html = response.content.decode(encoding="utf-8")
        self.assertIn("sign in success", resp_html)


# 针对django的单元/模块， UI 测试
# excel 表格
# 缺陷管理系统：用例管理

# 底层测试 ~ 功能实现细节~ 功能测试

# * django测试的运行，是独立的环境，不会使用数据库中的数据

"""
1、名称、步骤、预期，结果 原因
2、

代码的方法：

用例应该怎么创建？

class MyTest:
    def test_function(self):
        1.
        2.
        3.
if __name__ == '__main__':
    test = MyTest()
    test.test_function()
    test.test_function()
    .... 测试报告
"""