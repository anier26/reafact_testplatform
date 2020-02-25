import json
from django.shortcuts import render
from project_app.models import Project
from model_app.models import Module
from django.http import JsonResponse
from testTask_app.models import TestTask
from testcase_app.models import TestCase


def task_manage(request):
    tasks_list=TestTask.objects.all()
    return render(request,"task_list.html",{"type":"list","tasks":tasks_list})

def task_add(request):
    return render(request,"task_add.html",{"type":"add"})

def edit_task(request,tid):
    return render(request, "task_edit.html",{"type":"edit"})


# 保存任务:
def save_task(request):
    if request.method == "POST":
        name= request.POST.get("name","")
        desc =request.POST.get("desc","")
        cases=request.POST.get("cases","")
        print("name",name,desc)
        print("用例",type(cases),cases)
        if name == "" or cases =="":
            return JsonResponse({"status":10102,"message":"参数不能为空"})
        TestTask.objects.create(name=name,describe=desc,cases=cases)
        return JsonResponse({"status":10200,"message":"success"})
    else:
        return JsonResponse({"status":10101,"message":"请求方法错误"})

def get_cases_tree(request):
    if request.method == "GET":
        projects = Project.objects.all()
        data_list = []
        for project in projects:
            project_dict = {
                "name": project.name,
                "isParent": True
            }
            modules = Module.objects.filter(project_id=project.id)
            module_list = []
            for module in modules:
                module_dict = {
                    "name": module.name,
                    "isParent": True
                }
                cases = TestCase.objects.filter(module_id=module.id)
                case_list = []
                for case in cases:
                    case_dict = {
                        "name": case.name,
                        "isParent": False,
                        "id": case.id
                    }
                    case_list.append(case_dict)
                module_dict["children"] = case_list
                module_list.append(module_dict)
            project_dict["children"] = module_list
            data_list.append(project_dict)
        return JsonResponse({"status": 10200, "message": "success", "data": data_list})
    if request.method=="POST":
        tid=request.POST.get("tid","")
        print("tid: " ,tid)
        if tid == "":
            return JsonResponse({"status": 10101, "message": "error!任务id不能为空"})

        task = TestTask.objects.get(id=tid)
        caselist=json.loads(task.cases)
        task_data = {
            "name":task.name,
            "desc":task.describe
        }
        projects = Project.objects.all()
        data_list = []
        for project in projects:
            project_dict = {
                "name": project.name,
                "isParent": True
            }
            modules = Module.objects.filter(project_id=project.id)
            module_list = []
            for module in modules:
                module_dict = {
                    "name": module.name,
                    "isParent": True
                }
                cases = TestCase.objects.filter(module_id=module.id)
                case_list = []
                for case in cases:
                    if case.id in caselist:
                        case_dict = {
                            "name": case.name,
                            "isParent": False,
                            "id": case.id,
                            "checked":True,
                        }
                    else:
                        case_dict = {
                            "name": case.name,
                            "isParent": False,
                            "id": case.id,
                            "checked": False,
                        }
                    case_list.append(case_dict)
                module_dict["children"] = case_list
                module_list.append(module_dict)
            project_dict["children"] = module_list
            data_list.append(project_dict)
        task_data["cases"] = data_list
        return JsonResponse({"status": 10200, "message": "success", "data": task_data})









