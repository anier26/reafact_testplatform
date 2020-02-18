from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from personal.models.project import Project
from django.http import HttpResponse,HttpResponseRedirect

#登录成功默认项目管理页
@login_required
def project_manage(request):
    project_all=Project.objects.all()
    return render(request,"project.html",{"projects":project_all,"type":"list"})

#添加项目
@login_required
def add_project(request):
    if request.method =="GET":
        return render(request,"project.html",{"type":"add"})
    elif request.method =="POST":
        name=request.POST.get("name","")
        describe=request.POST.get("describe","")
        status=request.POST.get("status","")
        if(name == "" ):
            return render(request, "project.html", {"type": "add","name_err":"项目名不能为空"})
        Project.objects.create(name=name,describe=describe,status=status)
        return HttpResponseRedirect("/project/")



#编辑项目
@login_required
def edit_project(request):
    if request.method =="GET":
        return render(request,"project.html",{"type":"edit"})
