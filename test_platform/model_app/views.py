from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from model_app.models import Module
from model_app.forms import ModelForm
from django.http import HttpResponseRedirect, JsonResponse


# 模块管理
@login_required
def model_manage(request):
    if request.method=="GET":
        model_all=Module.objects.all()
        return render(request,"model.html",{"type":"list","models":model_all})

# 添加模块
@login_required
def add_model(request):
    if request.method =="GET":
        model_form=ModelForm()
        return render(request,"model.html",{"form":model_form,"type":"add"})
    elif request.method == "POST":
        form = ModelForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            Module.objects.create(project=project,name=name,describe=describe)
        return HttpResponseRedirect("/model/")

#编辑模块
def edit_model(request,mid):
    if request.method=="GET":
        model=Module.objects.get(id=mid)
        model_form=ModelForm(instance=model)
        return render(request,"model.html",{"form":model_form,"type":"edit","id":model.id})
    elif request.method == "POST":
        form=ModelForm(request.POST)
        if form.is_valid():
            project=form.cleaned_data['project']
            name=form.cleaned_data['name']
            describe=form.cleaned_data['describe']
            m=Module.objects.get(id=mid)
            m.project=project
            m.name=name
            m.describe=describe
            m.save()
        return HttpResponseRedirect("/model/")

#删除模块
def del_model(request,mid):
    if request.method == "GET":
        try:
            model = Module.objects.get(id=mid)
        except Module.DoesNotExist:
            return HttpResponseRedirect("/model/")
        else:
            model.delete()
        return HttpResponseRedirect("/model/")
    else:
        return HttpResponseRedirect("/model/")


# 根据项目id返回对应模块列表
def get_model_list(request):
    if request.method == "POST":
        pid = request.POST.get("pid", "")
        if pid == "":
            return JsonResponse({"status": 10101, "message": "error! projectId不能为空" })
        models = Module.objects.filter(project=pid)
        modle_list = []
        for mod in models:
            model_dict = {
                "id": mod.id,
                "name": mod.name
            }
            modle_list.append(model_dict)
        return JsonResponse({"status": 10800, "message": "success", "data": modle_list})
    else:
        return JsonResponse({"status": 10100, "message": "error"})