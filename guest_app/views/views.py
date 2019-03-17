from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from guest_app.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
# 返回登录首页
def index(request):
    return render(request, "index.html")

# 处理登录的动作
def login_action(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        print(user_name)
        print(pass_word)
        if user_name == "" or pass_word == "":
            return render(request, "index.html", {
                "hint": "用户名或者密码不能为空！"
            })
        user = auth.authenticate(username=user_name, password=pass_word)
        if user is not None:
            auth.login(request, user)
            # return render(request, "event_manage.html")
            response =  HttpResponseRedirect("/event_manage/")
            # cookie写到了浏览器的cookie
            #response.set_cookie("user01", user, 10)
            # sessionID写到了浏览器的cookie
            request.session['user02'] = user_name
            return response
        else:
            return render(request, "index.html", {
                "hint": "用户名或者密码错误！"
            })
    else:
        return HttpResponse("404")


# 发布会管理页面
@login_required
def event_manage(request):
    # 到浏览器的cookie读取
    # username = request.COOKIES.get('user01', '')
    # 到浏览器的cookie读取sessionID
    event_list = Event.objects.all()

    username = request.session.get('user02', '')
    print("user02", username)
    return render(request, "event_manage.html",{
        "user": username,
        "events": event_list
    })

def search_name(request):
    """搜索活动名称"""
    if request.method == "GET":
        name = request.GET.get("name", "")
        print("发布会名称", name)
        event_list = Event.objects.filter(name__contains=name)
        return render(request, "event_manage.html", {
            "events": event_list
        })
    else:
        return HttpResponseRedirect("/event_manage/")


def guest_manage(request):
    """嘉宾管理"""
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html",
                  {"guests": contacts})


def sign_index(request, eid):
    """签到页面"""
    print("签到的活动id", eid)
    event = get_object_or_404(Event, id=eid)

    guest_list = Guest.objects.filter(event_id=eid)
    guest_data = str(len(guest_list))  # 签到人数
    sign_data = 0  # 已签到人数
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1
    return render(request, 'sign_index.html', {
        'event': event, 'guest': guest_data, 'sign': sign_data})


def sign_action(request, eid):
    if request.method == "POST":
        phone = request.POST.get("phone", "")
        print("活动id", eid)
        print("手机号", phone)

        event = get_object_or_404(Event, id=eid)

        result = Guest.objects.filter(phone=phone)
        if not result:
            return render(request, 'sign_index.html',
                          {'event': event, 'hint': 'phone error.'})

        result = Guest.objects.filter(phone=phone, event_id=eid)
        if not result:
            return render(request, 'sign_index.html',
                          {'event': event, 'hint': 'event id or phone error.'})

        result = Guest.objects.get(event_id=eid, phone=phone)
        if result.sign is True:
            return render(request, 'sign_index.html',
                          {'event': event, 'hint': "user has sign in."})
        else:
            result = Guest.objects.get(event_id=eid, phone=phone) #.update(sign='1')
            result.sign=1
            result.save()
            return render(request, 'sign_index.html',
                          {'event': event, 'hint': 'sign in success!',
                                                       'user': result,
                                                       })


def logout(request):
    auth.logout(request)  # 退出登录
    return HttpResponseRedirect('/')



"""
业务：

签到 测试沙龙，测试技术大会，活动的通知：时间、地点

* 活动：时间、地点、状态、名称、id、人数

* 参加人员：名称、手机号、邮箱、签到

入口：电脑，界面：手机号、
/event_manage/search_name?name=小米
"""


