import json
import os
from django.shortcuts import render
from project_app.models import Project
from model_app.models import Module
from django.http import JsonResponse,HttpResponseRedirect
from testTask_app.models import TestTask
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
            return JsonResponse({"status":10101,"message": "task id is not null"})
        task=TestTask.objects.get(id=tid)
        caselist=json.loads(task.cases)
        print(caselist)
        test_data={}
        for cid in caselist:
            print("wtf " , cid)
            case = TestCase.objects.get(id=cid)
            if case.methods == 1:
                methods = "get"
            if case.methods == 2:
                methods = "post"
            else:
                methods = "null"
            if case.parameter_type == 1:
                parameter_type = "form_data"
            else:
                parameter_type = "json_data"

            if case.assert_type == 1:
                assert_type = "contains"
            else:
                assert_type = "matches"
            test_data[case.id] ={
                "url":case.url,
                "methods":methods,
                "headers":case.headers,
                "parameter_type":case.parameter_type,
                "parameter_body":case.parameter_body,
                "assert_type":case.assert_type,
                "assert_body":case.assert_body,
            }
        print("任务下用例: ", json.dumps(test_data))
        from test_platform import settings
        ex_dir = settings.BASE_DIR +"\\testTask_app\\extend\\"
        print("==================>>>",ex_dir)
        with(open(ex_dir + "test_data_list.json","w")) as f:
            f.write(json.dumps(test_data))
        cmdconfig = "pytest -vs " + ex_dir + "run_task.py --junitxml=" +ex_dir+"./log.xml"
        print("==================>>>", cmdconfig)
        os.system(cmdconfig)
        return JsonResponse({"status": 10200, "message": "success"})
    else:
        return JsonResponse({"status": 10200, "message": "faild"})


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









