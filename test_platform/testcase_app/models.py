from django.db import models
from model_app.models import Module

class TestCase(models.Model):
    # 测试用例表表
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称",max_length=50, null=False)
    url = models.TextField("URL",null=False)
    methods=models.IntegerField("请求方法",null=False) # 1:GET,2:POST,3:DELETE,4:PUT
    headers = models.TextField("请求头", null=False)
    parameter_type = models.IntegerField("参数类型", null=False)# 1.form-data 2. json
    parameter_body = models.TextField("参数内容", null=False)
    result_body=models.TextField("result", null=False)
    assert_type=models.IntegerField("assert", null=False) # 1.包含 2.匹配
    assert_body = models.TextField("结果", null=False)
    create_time=models.DateTimeField("创建时间",auto_now_add=True)


    def __str__(self):
        return self.name