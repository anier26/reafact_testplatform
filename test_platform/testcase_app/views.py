from django.shortcuts import render
import requests
import json
from django.http import HttpResponse,JsonResponse

# Create your views here.

def testcase_manage(request):
    return render(request,"testcase.html",{"type":"debug"})

def debug(request):
    if request.method=="POST":
        url=request.POST.get("url")
        moethd=request.POST.get("moethd")
        header=request.POST.get("header")
        parameter=request.POST.get("parameter")
        json_par=parameter.replace("\'","\"")
        payload=json.loads(json_par)
        print(payload)
        if moethd =="get":
            r=requests.get(url,params=payload)
            print("结果",r.text)
        if moethd =="post":
            r=requests.post(url,data=payload)
            print(r.text)
        return JsonResponse({"result":r.text})
    else:
        return JsonResponse({"result": "test_fail"})