import os
from xml.dom.minidom import parse
from time import sleep
import  threading
import json
import sys
from testTask_app.models import TestTask, TaskResult
from testcase_app.models import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = BASE_DIR.replace("\\","/")
sys.path.append(BASE_PATH)
extend_dir = BASE_PATH + "/extend/"

print("===================>>>",extend_dir)

class TaskThread():
    def __init__(self,task_id):
        self.tid = task_id

    def run_cases(self):
        task = TestTask.objects.get(id=self.tid)
        caselist = json.loads(task.cases)

        test_data = {}
        for cid in caselist:
            print("wtf ", cid)
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
            test_data[case.id] = {
                "url": case.url,
                "methods": methods,
                "headers": case.headers,
                "parameter_type": case.parameter_type,
                "parameter_body": case.parameter_body,
                "assert_type": case.assert_type,
                "assert_body": case.assert_body,
            }
        case_data = json.dumps(test_data)
        with(open(extend_dir + "test_data_list.json", "w")) as f:
            f.write(case_data)

        cmdconfig = "python " + extend_dir + "run_task.py"
        print("运行命令: " ,cmdconfig)
        os.system(cmdconfig)  # 运行
        sleep(3)
        self.save_result()
        task = TestTask.objects.get(id=self.tid)
        task.status=2
        task.save()

    def save_result(self):
        dom = parse(extend_dir + 'results.xml')
        root = dom.documentElement
        testsuite = root.getElementsByTagName('testsuite')
        error = testsuite[0].getAttribute('errors')
        failures = testsuite[0].getAttribute('failures')
        name = testsuite[0].getAttribute('name')
        skipped = testsuite[0].getAttribute('skipped')
        tests = testsuite[0].getAttribute('tests')
        run_time = testsuite[0].getAttribute('time')
        f = open(extend_dir + "results.xml", "r",encoding="utf-8")
        result = f.read()

        print("=============>" ,error)
        print("=============>" ,failures)
        print("=============>" ,name)
        print("=============>" ,skipped)
        print("=============>" ,run_time)

        TaskResult.objects.create(
            task_id = self.tid,
            name=name,
            error = int(error),
            failure = int(failures),
            skipped = int(skipped),
            tests = int(tests),
            run_time = run_time,
            result = result
        )

    def run_tasks(self):
        print("创建任务线程")
        sleep(2)
        threads = []
        t1 = threading.Thread(target=self.run_cases)
        threads.append(t1)
        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def run(self):
        threads = []
        t = threading.Thread(target=self.run_tasks)
        threads.append(t)

        for t in threads:
            t.start()

if __name__ == '__main__':
    TaskThread(1).run()