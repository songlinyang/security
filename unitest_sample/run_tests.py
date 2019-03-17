import  unittest
from HTMLTestRunner import HTMLTestRunner


suit = unittest.defaultTestLoader.discover(start_dir="./",
                                    pattern="test_*.py")

report = open("./report.html", "wb")
runner = HTMLTestRunner(stream=report,
                        title="unittest自动化测试",
                        description="这只是一个简单的例子")
runner.run(suit)
report.close()

# main 和 discover 不能控制用例顺序，该名字