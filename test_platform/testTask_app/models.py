from django.db import models


class TestTask(models.Model):
    name = models.CharField(max_length=100,blank=False, null=False)
    describe = models.TextField(default="")
    status = models.IntegerField("状态", default=0)
    cases = models.TextField(default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name

class TaskResult(models.Model):
    name = models.CharField(max_length=100, blank=False, default="")
    task = models.ForeignKey(TestTask, on_delete=models.CASCADE)
    error = models.IntegerField("状态", default=0)
    failure = models.IntegerField("失败用例")
    skipped = models.IntegerField("跳过用例")
    tests = models.IntegerField("总用例数")
    run_time = models.FloatField("运行时长")
    result = models.TextField("结果", default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name