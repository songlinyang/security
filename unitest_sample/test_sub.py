import unittest
from count import Count

#1. 创建的测试类必须要集成unittest.TestCase
class MyTest(unittest.TestCase):

    def setUp(self):
        self.c = Count()

    def tearDown(self):
        pass

    #2.测试用例必须以"test"开头
    def test_sub(self):
        print("sub")
        result = self.c.sub(4, 5)
        self.assertEqual(result, -1)


if __name__ == '__main__':
    unittest.main()

"""
a~z   A~Z, 0~9

aa/
    test_ab.py
       MyAAA
          test_aaa
          test_bbb
       MyBBB
          test_ccc
          test_bbb
    test_aaaaaa.py
bb/
"""



