from django.urls import path
from testTask_app import views

urlpatterns = [
    #任务管理管理
    path('', views.task_manage),
    path('task_add', views.task_add),
    path('edit_task/<int:tid>/', views.edit_task),
    path('del_task/<int:tid>/', views.del_task),
    path('save_task', views.save_task),
    path('result/<int:tid>/', views.result),

    path('get_case_tree', views.get_cases_tree),
    path('run_task', views.run_task),
]