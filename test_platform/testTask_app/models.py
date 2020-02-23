from django.db import models

class TestTask(models.Model):
    name = models.CharField(max_length=100,blank=False, null=False)
    describe = models.TextField(default="")
    status = models.IntegerField("状态", default=0)
    cases = models.TextField(default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)



    def __str__(self):
        return self.name