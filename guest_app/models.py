from django.db import models

#selct * from table_name where name like '%小米%'
#python代码      数据库驱动 pymysql    mysql数据库


# Create your models here. ORM 关系对象模型
class Event(models.Model):
    """活动表"""
    name = models.CharField("名称", max_length=50)
    status = models.BooleanField("状态", default=True)
    limit = models.IntegerField("人数")
    address = models.CharField("地址", max_length=100)
    start_time = models.DateTimeField('时间')
    create_time = models.DateTimeField(auto_now_add=True)  # 更新时间（自动获取当前时间）

    def __str__(self):
        return self.name


class Guest(models.Model):
    """嘉宾表"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # 关联发布会id
    real_name = models.CharField("姓名", max_length=64)  # 姓名
    phone = models.CharField("手机",max_length=16)     # 手机号
    email = models.EmailField("邮箱")                 # 邮箱
    sign = models.BooleanField("签到", default=False)                # 签到状态
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间（自动获取当前时间）

    def __str__(self):
        return self.real_name

#e2 = Event.objects.select_for_update().get(id=5).update(name="荣耀手机发布会")
#e1 = Event.objects.create(name="荣耀手机", address="深圳",limit=2000, start_time="2018-12-12 12:00:00")

"""
测试微信公众号，活动，抽奖，转发。

抽奖接口

活动的页面有很大的差别。

设计，前端  web页面 -- 一周以上  + 两天 --》测试 （3~5） 两天，

后端接口， 两、三天 --》先测接口，接口框架，反馈

测试流程总结：

1、整个项目时间缩短（测试的提前介入）
2、测试更全面，深入
3、发现更深入问题、安全的问题

java Interface == 抽象的定义


interfa car{
    可以跑
}

具体的汽车  集成 car {
    可以跑｛
     发动机
    ｝
}

自行车  集成 car {
    可以跑｛
     用腿去凳
    ｝
}

"""












