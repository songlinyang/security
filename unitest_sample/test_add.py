import unittest
from count import Count

#1. 创建的测试类必须要集成unittest.TestCase
class MyTest(unittest.TestCase):

    def setUp(self):
        self.c = Count()

    def tearDown(self):
        pass

    #2.测试用例必须以"test"开头
    def test_add(self):
        print("add")
        result = self.c.add(4, 5)
        self.assertEqual(result, 9)

    def test_add2(self):
        print("add2")
        result = self.c.add(4.1, 5.2)
        self.assertEqual(result, 9.3)

if __name__ == '__main__':
    unittest.main()
    #运行一组测试用例的集合 筷笼
    suit = unittest.TestSuite()
    suit.addTest(MyTest("test_add2"))
    suit.addTest(MyTest("test_add"))

    runner = unittest.TextTestRunner()
    runner.run(suit)





