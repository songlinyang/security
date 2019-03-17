from selenium import webdriver
from time import sleep
import unittest

class MySeleniumTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.base_url = "http://127.0.0.1:8000/"
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_login_null(self):
        self.driver.get(self.base_url)
        self.driver.find_element_by_name("username").send_keys('')
        self.driver.find_element_by_name("password").send_keys('')
        self.driver.find_element_by_id('LoginButton').click()
        sleep(2)
        hint = self.driver.find_element_by_tag_name("p").text
        print(hint)
        self.assertEqual("用户名或者密码不能为空！", hint)


    def test_login_error(self):
        self.driver.get(self.base_url)
        self.driver.find_element_by_name("username").send_keys('error')
        self.driver.find_element_by_name("password").send_keys('error')
        self.driver.find_element_by_id('LoginButton').click()
        sleep(2)
        hint = self.driver.find_element_by_tag_name("p").text
        print(hint)
        self.assertEqual("用户名或者密码错误！", hint)

    def test_login_success(self):
        self.driver.get(self.base_url)
        self.driver.find_element_by_name("username").send_keys('admin')
        self.driver.find_element_by_name("password").send_keys("admin123456")
        self.driver.find_element_by_id('LoginButton').click()
        sleep(5)


if __name__ == '__main__':
    unittest.main()










