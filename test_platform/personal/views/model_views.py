from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# 模块管理
@login_required
def model_manage(request):
    return render(request,"model.html")