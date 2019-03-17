import unittest
import HTMLTestRunner
sec_suite = unittest.defaultTestLoader.discover(start_dir="./",pattern="test_*.py")
sec_report = open("./sec_report.html",'wb')
runner = HTMLTestRunner.HTMLTestRunner(stream=sec_report, verbosity=2, title="加密接口测试报告", description=None)
runner.run(sec_suite)