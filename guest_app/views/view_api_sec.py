from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib import auth as django_auth
from guest_app.models import Event,Guest
from django.forms.models import model_to_dict
import base64
from mysite import common
import time
import hashlib
from django.core.exceptions import ValidationError
import traceback
#=======用户认证===============
def user_auth(request):

    try:
        get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
        base64str = str(get_http_auth).split(" ")[1]
        print('base64str', base64str)
    except IndexError:
        return "error"
    try:
        print("解密64:",base64.b64decode(base64str))
        ret = base64.b64decode(base64str).decode('utf-8')
        print(ret)

    except UnicodeDecodeError:
        return "error"
    else:
        auth_path = ret.partition(':')
        userid,password = auth_path[0],auth_path[2]
        print(userid)
        print(password)
        user = django_auth.authenticate(username=userid,password=password)
        print(user)
        if user is not None and user.is_active:
            django_auth.login(request,user)
            return 'success'
        else:
            return 'fail'

def get_all_event_sec(request):
    # 创造一个接口：提交数据方式applicat/x-www-form-urlencode
    #---------------------------
    # 增加用户认证 + 参数eid或name查询指定发布会信息
    #---------------------------
    result = user_auth(request)
    if request.method == "GET":
        if result == 'error':
            return JsonResponse({"status":100306,"message":"user auth null"})
        if result == 'fail':
            return JsonResponse({"status":100307,"message":"user auth fail"})
            #return HttpResponseRedirect("/event_manage/")
        eid = request.GET.get("eid")
        name = request.GET.get("name")
        if eid==None and name==None:
            return common.response_fail(status=100404,message="必传字段有误")
        if eid=="" and name=="":
            return common.response_fail(status=100405,message="必传字段不能为空")
        if eid!=None and eid!="":
            event = Event.objects.get(id=eid)
            event_data = model_to_dict(event)
            return common.response_success(status=200,message="",data=event_data)
        if name!=None and name!="":
            event = Event.objects.get(name=name)
            event_data = model_to_dict(event)
            return common.response_success(status=200,message="",data=event_data)
            # print(event_dict)

    else:
        return HttpResponse("请求方法失败！")


#=======用户签名+时间戳===============

# 用户签名+时间戳
def user_sign(request):

    if request.method == 'POST':
        req = common.json_to_dict(request.body)
        client_time = common.get_request_key(req,"time")   # 客户端时间戳
        client_sign = common.get_request_key(req,"sign")   # 客户端签名
    else:
        return "error"
    body_str
    if client_time == '' or client_sign == '':
        return "sign null"

    # 服务器时间
    now_time = time.time()    # 例：1466426831
    server_time = str(now_time).split('.')[0]
    # 获取时间差
    time_difference = int(server_time) - int(client_time)
    print(">>>>>server_time",server_time)
    print(">>>>>>client_time",client_time)
    if time_difference >= 60 :
        return "timeout"

    # 签名检查
    md5 = hashlib.md5()
    sign_str = client_time + "&Guest-Bugmaster"
    sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)
    sever_sign = md5.hexdigest()
    if sever_sign != client_sign:
        return "sign fail"
    else:
        return "sign right"


# 添加发布会接口
def add_event_sec(request):
    #添加md5鉴权
    sign_result = user_sign(request)
    if request.method == "POST":
        if sign_result == "error":
            return common.response_fail(status=1011,message='request error')
        if sign_result == "sign null":
            return common.response_fail(status=1012,message='user sign null')
        if sign_result == "timeout":
            return common.response_fail(status=1013,message='user sign timeout')
        if sign_result == "sign fail":
            return common.response_fail(status=1014,message='user sign error')

        req = common.json_to_dict(request.body)
        name = common.get_request_key(req, "name")
        address = common.get_request_key(req, "address")
        start_time = common.get_request_key(req, "start_time")
        status = common.get_request_key(req, "status")
        limit = common.get_request_key(req, "limit")

        # 判断必传字段
        if name is None or address is None or start_time is None:
            return common.response_fail(status=10201, message="必传字段为空")

        # 重复的发布会名称不能创建
        event = Event.objects.filter(name=name)
        if len(event) != 0:
            return common.response_fail(status=10202, message="发布会名称已存在")

        # 如果状态不填的默认值
        if status is None:
            status = 1

        # 如果人数不填的默认值
        if limit is None:
            limit = 0
        print("name", name)
        print("limit", limit)
        print("address", address)
        print("status", status)
        print("start_time", start_time)

        try:
            Event.objects.create(name=name, limit=limit, address=address,
                                 status=int(status), start_time=str(start_time))
        except ValidationError:
            error = "日期格式错误, 必须是：'YYYY-MM-DD HH:MM:SS'."
            return common.response_fail(status=10202, message=error)
        else:
            return common.response_success(message="添加发布成功！")

    else:
        return common.response_fail(message="请求失败")


def user_sign(request):
    if request.method == "POST":
        pass
