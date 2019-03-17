from django.http import JsonResponse
from mysite import common
from guest_app.models import Event
from django.forms.models import model_to_dict
import json
from django.core.exceptions import ValidationError, ObjectDoesNotExist

# 关于发布会相关接口

# 查询发布会接口
def get_all_event(request):
	if request.method == "GET":
		events = Event.objects.get()
		print("发布会对象", events)
		event_list = []
		for event in events:
			# event_dict = {
			# 	"id": event.id,
			# 	"name": event.name,
			# 	"address": event.address,
			# 	"start_time": event.start_time.strftime('%Y-%m-%d %H:%I:%S')
			# }
			event_dict = model_to_dict(event)			
			event_list.append(event_dict)
		return common.response_success(data=event_list)
	else:
		return common.response_fail(message="请求失败")


# 添加发布会接口
def add_event(request):
	if request.method == "POST":
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
			Event.objects.create(name=name,limit=limit,address=address,
								 status=int(status),start_time=str(start_time))
		except ValidationError:
			error = "日期格式错误, 必须是：'YYYY-MM-DD HH:MM:SS'."
			return common.response_fail(status=10202, message=error)
		else:
			return common.response_success(message="添加发布成功！")
		
	else:
		return common.response_fail(message="请求失败")







# 接口（POST）的参数类型
# none : 没有参数
# form-data : key: value  
# x-www-form-urlencode: key: value
# raw:文本：xml, * json 
# binary : 文件
# json? xml文本格式
# body = request.body
# body_str = str(body, encoding="utf-8")
# body_dict = json.loads(body_str)
# name = body_dict["name"]
# address = body_dict["address"]

# print(body_dict)
# print(type(body_dict))

# form-data/x-wwww-from-urlencode
# name = request.POST.get("name", "")
# address = request.POST.get("address", "")



