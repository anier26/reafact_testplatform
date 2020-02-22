from django.urls import path
from testtask_app import views

urlpatterns = [
    #任务管理管理
    path('', views.task_manage),
    path('task_add', views.task_add),
    # path('task_edit', views.task_edit),
    # path('task_del', views.task_del),
    path('get_case_tree', views.get_cases_tree),
]