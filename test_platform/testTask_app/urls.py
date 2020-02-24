from django.urls import path
from testTask_app import views

urlpatterns = [
    #任务管理管理
    path('', views.task_manage),
    path('task_add', views.task_add),
    path('edit_task/<int:tid>/', views.edit_task),
    # path('task_del', views.task_del),
    path('save_task', views.save_task),
    path('get_case_tree', views.get_cases_tree),
]