from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from personal.models.model import Module
from personal.forms import ModelForm
from django.http import HttpResponse,HttpResponseRedirect


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