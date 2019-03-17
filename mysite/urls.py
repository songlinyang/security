"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from guest_app.views import views
from guest_app.views import views_api


# 用来配置路由
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index', views.index),
    path('accounts/login/', views.index),
    path('login_action/', views.login_action),
    path('event_manage/', views.event_manage),
    path('logout', views.logout),
    path("event_manage/search_name/", views.search_name),
    path("guest_manage/", views.guest_manage),
    path("sign_index/<int:eid>",views.sign_index),
    path("sign_action/<int:eid>", views.sign_action),

    # 接口的调用
    path('api/', include('guest_app.urls'))
    
    
    # 前端代码调用的后端接口
    # path('api/', views_api.login), 

    # 创建一个接口
    # path('api/user', views_api.user),

]
# 实现接口：动作

# 获取某一个用户接口：

# api/get_user/

# 获取所有用户的接口

# api/get_all_user/

# 删除用户

# api/delete_user/

# 更新

# api/update_user/
