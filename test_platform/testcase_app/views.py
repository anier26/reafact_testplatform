from django.shortcuts import render
import requests
import json
from django.http import HttpResponse,JsonResponse

# Create your views here.

def testcase_manage(request):
    return render(request,"testcase.html",{"type":"debug"})

def debug(request):
    if request.method=="POST":
        url=request.POST.get("url","")
        moethd=request.POST.get("moethd","")
        header=request.POST.get("header","")
        type_=request.POST.get("type","")
        parameter=request.POST.get("parameter","")
        json_header=header.replace("\'","\"")
        try:
            header=json.loads(json_header)
        except json.decoder.JSONDecodeError:
            return  JsonResponse({"result":"headers错误"})


        json_par=parameter.replace("\'","\"")
        try:
            payload=json.loads(json_par)
        except json.decoder.JSONDecodeError:
            return  JsonResponse({"result":"参数类型错误"})

        if moethd =="get":
            if header == "":
                r=requests.get(url,params=payload)
                print("结果",r.json())
            else:
                r=requests.get(url,params=payload,headers=header)
                print("结果",r.json())
        if moethd =="post":
            if header == "":
                r=requests.post(url,data=payload)
                print(r.text)
            else:
                r = requests.post(url, params=payload, headers=header)
                print("结果", r.text)

        if type_ == "json":
            if header == "":
                r = requests.post(url, data=payload)
                print(r.text)
            else:
                r = requests.post(url, params=payload, headers=header)
                print("结果", r.text)
        return JsonResponse({"result":r.text})
    else:
        return JsonResponse({"result": "test_fail"})

def asserts(request):
    if request.method=="POST":
        result_text = request.POST.get("result", "")
        assert_text = request.POST.get("asserts", "")
        assert_type = request.POST.get("assert_type", "")
        if result_text == "" or assert_text =="":
            return JsonResponse({"result": "断言的文本不能为空"})

        if  assert_type == "contains":
            if assert_text not in result_text:
                return JsonResponse({"result": "assert fail"})
            else:
                return JsonResponse({"result": "assert success"})
        elif assert_type == "matches":
            if assert_text != result_text:
                return JsonResponse({"result": "assert fail"})
            else:
                return JsonResponse({"result": "assert success"})
    else:
        return JsonResponse({"result": "请求错误"})