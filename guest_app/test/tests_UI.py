from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from time import sleep
from django.contrib.auth.models import User

class MySeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login_null(self):
        # self.driver.get('%s%s' % (self.live_server_url, '/'))
        self.driver.get(self.live_server_url + "/")
        self.driver.find_element_by_name("username").send_keys('')
        self.driver.find_element_by_name("password").send_keys('')
        self.driver.find_element_by_id('LoginButton').click()
        sleep(2)
        hint = self.driver.find_element_by_tag_name("p").text
        print(hint)
        self.assertEqual("用户名或者密码不能为空！", hint)


    def test_login_error(self):
        # self.driver.get('%s%s' % (self.live_server_url, '/'))
        self.driver.get(self.live_server_url + "/")
        self.driver.find_element_by_name("username").send_keys('error')
        self.driver.find_element_by_name("password").send_keys('error')
        self.driver.find_element_by_id('LoginButton').click()
        sleep(2)
        hint = self.driver.find_element_by_tag_name("p").text
        print(hint)
        self.assertEqual("用户名或者密码错误！", hint)

    def test_login_success(self):
        # self.driver.get('%s%s' % (self.live_server_url, '/'))
        self.driver.get(self.live_server_url + "/")
        self.driver.find_element_by_name("username").send_keys('admin')
        self.driver.find_element_by_name("password").send_keys("admin123456")
        self.driver.find_element_by_id('LoginButton').click()
        sleep(5)


