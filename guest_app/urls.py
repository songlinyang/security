from django.urls import path
from guest_app.views import event_api
from guest_app.views import guest_api
from guest_app.views import view_api_sec

urlpatterns = [
    # guest system interface:
    # ex : api/get_all_event 获取所有的发布会数据
    path('get_all_event', event_api.get_all_event),
   	# ex : api/add_event 添加发布会
    path('add_event', event_api.add_event),
    # ex : api/get_guest 获取某嘉宾信息
    path('get_guest', guest_api.get_guest),
    # ex : api/add_guest 添加嘉宾
    path('add_guest', guest_api.add_guest),

    # ex : api/user_sign 添加嘉宾
    path('user_sign', guest_api.user_sign),


    #ex : 安全认证的接口
    path('get_all_event_sec',view_api_sec.get_all_event_sec),
    path('add_event_sec',view_api_sec.add_event_sec),
    path('user_sign',view_api_sec.user_sign),
]
