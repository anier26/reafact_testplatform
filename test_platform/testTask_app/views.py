import json
from unittest import TestResult

from testTask_app.extend.task_thread import TaskThread
from django.shortcuts import render
from project_app.models import Project
from model_app.models import Module
from django.http import JsonResponse,HttpResponseRedirect
from testTask_app.models import TestTask, TaskResult
from testcase_app.models import TestCase


def task_manage(request):
    tasks_list=TestTask.objects.all()
    return render(request,"task_list.html",{"type":"list","tasks":tasks_list})

def task_add(request):
    return render(request,"task_add.html",{"type":"add"})

def edit_task(request,tid):
    return render(request, "task_edit.html",{"type":"edit"})

def del_task(request,tid):
    task=TestTask.objects.get(id=tid)
    task.delete()
    return HttpResponseRedirect("/testTask/")


def run_task(request):
    if request.method == "POST":
        tid=request.POST.get("task_id","")
        if tid == "":
            return JsonResponse({"status":10202,"message": "task id is not null"})

        tasks=TestTask.objects.all()
        for i in tasks:
            if i.status == 1:
                return JsonResponse({"status": 10201, "message": "任务执行中请稍等..."})

        task = TestTask.objects.get(id=tid)
        task.status = 1
        task.save()
        TaskThread(tid).run()
        return JsonResponse({"status": 10200, "message": "开始执行"})
    else:
        return JsonResponse({"status": 10203, "message": "执行失败"})


# 保存任务: 创建和编辑taskid= 0 创建,id不等于更新
def save_task(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id","");
        name= request.POST.get("name","")
        desc =request.POST.get("desc","")
        cases=request.POST.get("cases","")
        print("name",name,desc)
        print("用例",type(cases),cases)
        if name == "" or cases =="":
            return JsonResponse({"status":10102,"message":"参数不能为空"})

        if task_id == "0":
            TestTask.objects.create(name=name,describe=desc,cases=cases)
        else:
            task=TestTask.objects.get(id=task_id)
            task.name=name
            task.describe=desc
            task.cases=cases
            task.save()
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


def result(request,tid):
    results = TaskResult.objects.filter(task_id=tid).order_by("-create_time")
    return render(request, "task_result.html",{"results": results,"type":"result"})


def see_log(request):
    if request.method == "POST":
        rid = request.POST.get("result_id", "")
        if rid == "":
            return JsonResponse({"status": 10105, "message": "任务id不能为空"})
        result = TaskResult.objects.get(id = rid)
        result.result
        return JsonResponse({"status": 10200, "message": "success","data":result.result})
    else:
        return JsonResponse({"status": 10101, "message": "请求方法错误"})