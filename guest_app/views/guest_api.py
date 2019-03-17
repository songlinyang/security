import time
from mysite import common
from guest_app.models import Guest, Event
from django.forms.models import model_to_dict
# 关于嘉宾相关接口

# 获取一条嘉宾数据
# 1、请求方法错误
# 2、必传参数不传
# 3、参数类型不对
# 4、查询为空，id不存在
# 5、查询成功
def get_guest(request):
    if request.method == "POST":
        gid = request.POST.get("guest_id", "")
        if gid == "":
            return common.response_fail(status=10201, message="嘉宾的id不能为空")
        try:
            int(gid)
        except ValueError:
            return common.response_fail(status=10202, message="嘉宾的id类型错误")

        # guests = Guest.objects.filter(id=gid)
        # guest_list = []
        # for guest in guests:
        #     guest_dict = model_to_dict(guest)
        #     guest_list.append(guest_dict)
        try:
            guest = Guest.objects.get(id=gid)
            guest_dict = model_to_dict(guest)
        except Guest.DoesNotExist:
            return common.response_success(message="查询结果为空")
        else:
            return common.response_success(message="查询成功", data=guest_dict)

    else:
        return common.response_fail(message="请求方法错误")


# 添加嘉宾接口
def add_guest(request):
    if request.method == "POST":
        req = common.json_to_dict(request.body)
        event_id = common.get_request_key(req, "event_id")
        real_name = common.get_request_key(req, "real_name")
        phone = common.get_request_key(req, "phone")
        email = common.get_request_key(req, "email")

        # 判断必传字段
        if event_id is None or real_name is None or phone is None or email is None:
            return common.response_fail(status=10201, message="必传字段为空")

        try:
            event_obj = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return common.response_fail(message="发布会id不存在")

        Guest.objects.create(event=event_obj, real_name=real_name,
                                     phone=phone, email=email)

        return common.response_success(message="添加发布成功！")

    else:
        return common.response_fail(message="请求失败")

# URL, 请求方法，参数

# 嘉宾签到接口
def user_sign(request):
    if request.method == "POST":
        req = common.json_to_dict(request.body)
        event_id = common.get_request_key(req, "event_id")
        phone = common.get_request_key(req, "phone")

        # 判断必传字段
        if event_id is None or phone is None:
            return common.response_fail(status=10201, message="必传字段为空")

        event_obj = Event.objects.filter(id=event_id)
        if len(event_obj) == 0:
            return common.response_fail(status=10202, message="发布会id不存在")

        guest_obj = Guest.objects.filter(phone=phone)
        if len(guest_obj) == 0:
            return common.response_fail(status=10203, message="嘉宾手机号不存在")

        guest_obj = Guest.objects.filter(event_id=event_id, phone=phone)
        if len(guest_obj) == 0:
            return common.response_fail(status=10204, message="发布会id或嘉宾手机号错误")

        event = Event.objects.get(id=event_id)

        time_array = time.strptime(str(event.start_time), "%Y-%m-%d %H:%M:%S")
        start_time = int(time.mktime(time_array))
        now_time = int(time.time())

        if start_time < now_time:
            return common.response_fail(status=10205, message="发布会签到时间已经结束")

        guest = Guest.objects.get(event_id=event_id, phone=phone)
        if guest.sign:
            return  common.response_fail(status=10206, message="嘉宾已签到")
        else:
            guest.sign = True
            guest.save()
            return common.response_success(message="签到成功")

    else:
        return common.response_fail(message="请求失败")

