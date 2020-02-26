import sys
import json
import unittest

from ddt import ddt,data,file_data,unpack
import requests
import xmlrunner
from os.path import dirname,abspath
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
BASE_PATH = BASE_DIR.replace("\\","/")
sys.path.append(BASE_PATH)

#定义任务目录:
TASK_PATH = BASE_PATH + "/testTask_app/extend/"
print(TASK_PATH)
@ddt
class InterfaceTest(unittest.TestCase):
    @unpack
    @file_data(TASK_PATH + "test_data_list.json")
    def test_run_cases(self,url,methods,headers,parameter_type,parameter_body,assert_type,assert_body):
        if headers == "{}":
            headers_dict ={}
        else:
            headers_str = headers.replace("\'","\"")
            headers_dict = json.loads(headers_str)
        if parameter_body == "{}":
            parameter_dict = {}
        else:
            parameter_str = parameter_body.replace("\'","\"")
            parameter_dict = json.loads(parameter_str)
        if methods == "get":
            if parameter_body == "from_data":
                r = requests.get(url, headers=headers_dict,params=parameter_dict)
                # self.assertIn(assert_body,r.text)
        if methods == "post":
            if parameter_body == "from_data":
               r = requests.get(url, headers=headers_dict,params=parameter_dict)
               # self.assertIn(assert_body,r.text)
            elif parameter_type == "json_data":
                r = requests.post(url, headers=headers_dict, data=parameter_dict)
                # self.assertIn(assert_body, r.text)

# 运行测试用例:
# def run_case():
#     with open(TASK_PATH + "results.xml", "wb") as output:
#         unittest.main(
#             testRunner=xmlrunner.XMLTestRunner(output=output),
#             failfast=False,buffer=False,catchbreak=False)

if __name__ == '__main__':
    # run_case()
    unittest.main()

