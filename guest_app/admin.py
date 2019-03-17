from django.contrib import admin
from guest_app.models import Event, Guest

# Register your models here.
# 把 models.py 中的表设置到admin后台
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'address','start_time', 'limit','id']
    search_fields = ['name']    # 搜索功能
    list_filter = ['status']    # 过滤器


class GuestAdmin(admin.ModelAdmin):
    list_display = ['real_name', 'phone','email', 'create_time','event_id', "sign"]
    list_display_links = ['real_name', 'phone']  # 显示链接
    search_fields = ['real_name','phone']       # 搜索功能
    list_filter = ['event_id']                 # 过滤器


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)