import requests

parload={"key1": "value1", "key2": "value2"}
r=requests.get("http://httpbin.org/get",params=parload)
print(r.json)