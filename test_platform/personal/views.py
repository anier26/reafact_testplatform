#encoding=utf8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def say_hello(request):
    name=request.GET.get("name","")
    if name=="":
        return HttpResponse("请输入?name=name")
    return render(request,"index.html",{'name': name})

def index(request):
    if request.method == "GET":
        return render(request,"index.html")
    else:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            return render(request, "index.html", {
                "error": "用户名或密码为空"})
        user=auth.authenticate(username=username,password=password)
        print(user)
        if user is None:
            return render(request, "index.html", {
                "error": "用户名或密码错误"})
        else:
            auth.login(request,user)
            return HttpResponseRedirect("/project/")

# 用户登录
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/index/")

#登录成功默认项目管理页
@login_required
def project_manage(request):
    return render(request,"project.html")

# 模块管理
@login_required
def model_manage(request):
    return render(request,"model.html")
