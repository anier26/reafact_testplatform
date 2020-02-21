from django.shortcuts import render
import requests
import json
from django.http import JsonResponse

from model_app.forms import ModelForm
from model_app.models import Module
from testcase_app.models import TestCase #abc


def case_manage(request):
    #用例列表
    case_list=TestCase.objects.all()
    return render(request,"case_list.html",{"cases": case_list})

def case_add(request):
    return render(request, "case_add.html")




def debug(request):
    if request.method=="POST":
        url=request.POST.get("url","")
        method=request.POST.get("method","")
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

        if method =="get":
            if header == "":
                r=requests.get(url,params=payload)
                result_text=r.text
            else:
                r=requests.get(url,params=payload,headers=header)
                result_text = r.text
        if method =="post":
            if type_ =="form_data":
                if header == "":
                    r=requests.post(url,data=payload)
                    result_text = r.text
                else:
                    r = requests.post(url, params=payload, headers=header)
                    print("结果", r.text)
            if type_ == "json_data":
                if header == "":
                    r = requests.post(url, data=payload)
                    print("结果", r.text)
                else:
                    r = requests.post(url, params=payload, headers=header)
                    result_text = r.text

        return JsonResponse({"result":r.text})
    else:
        return JsonResponse({"result": "请求错误"})

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

# 保存用例
def save_case(request):
    if request.method == "POST":
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        header = request.POST.get("header", "")
        parameter_type = request.POST.get("parameter_type", "")
        parameter_body = request.POST.get("parameter_body", "")
        assert_body = request.POST.get("assert_body", "")
        assert_type = request.POST.get("assert_type", "")
        module_id = request.POST.get("mid", "")
        name = request.POST.get("name", "")


        print("url",url)
        print("method",method)
        print("header",header)
        print("parameter_type",parameter_type)
        print("parameter_body",parameter_body)
        print("assert_body",assert_body)
        print("assert_type",assert_type)
        print("module_id",module_id)
        print("name",name)
        print("=================================")

        if name == "":
             return JsonResponse({"statusCode": 10103, "status": "error", "err_msg": "用例名不能为空"})

        if assert_type == "":
            return JsonResponse({"statusCode": 10103, "status": "error","err_msg":"断言类型不能为空"})

        if module_id == "":
            return JsonResponse({"statusCode": 10103, "status": "error","err_msg":"模块id不能为空"})

        if method =="get":
            module_number =1
        elif method == "post":
            module_number =2
        elif method =="put":
            module_number =3
        elif method == "delete":
            module_number =4
        else:
            return JsonResponse({"status": 10100, "message": "error! 未知的请求方法体 "})

        #请求类型:
        if parameter_type == "form_data":
            parameter_number = 1
        elif parameter_type == "json_data":
            parameter_number = 2
        else:
            return JsonResponse({"status": 10100, "message": "error! 未知的请求类型 "})

        # 断言类型:
        if assert_type == "contains":
            assert_number = 1
        elif assert_type == "matches":
            assert_number = 2
        else:
            return JsonResponse({"status": 10000, "message": "error! 未知的断言类型"})
        TestCase.objects.create(name=name,module_id=module_id,
                            url=url,methods=module_number,headers=header,
                            parameter_type=parameter_number,parameter_body=parameter_body,
                            assert_type=assert_number,assert_body=assert_body);
        return JsonResponse({"status": 10200, "message": "create success!"})
    else:
        return JsonResponse({"status": 10100, "message": "error"})
