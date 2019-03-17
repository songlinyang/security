from django.http import JsonResponse
import json

# 返回成功
def response_success(status=None, message=None, data=None):
	if status is None:
		status = 10200
	if message is None:
		message = "success"
	if data is None:
		data = {}
	resp = {
		"status": status,
		"message": message,
		"data": data
	}
	return JsonResponse(resp)


# 返回失败
def response_fail(status=None, message=None, data=None):
	if status is None:
		status = 10404
	if message is None:
		message = "fail"
	resp = {
		"status": status,
		"message": message,
	}
	return JsonResponse(resp)


# 将文本转为字典
def json_to_dict(body):
	print("body", body)
	body_str = str(body, encoding="utf-8")
	print("body_str", body_str)
	try:
		body_dict = json.loads(body_str)
	except json.decoder.JSONDecodeError:
		body_dict = {}
	return body_dict


# 通过key取字典里面的value
def get_request_key(request, key):
	try:
		value = request[key]
	except KeyError:
		value = None
	return value
