from django.urls import path
from testcase_app import views

urlpatterns = [

    #项目管理
    path('', views.case_manage),
    path('debug', views.debug),
    path('case_add', views.case_add),
    path('case_list', views.case_manage),
    path('asserts', views.asserts),
    path('save_case', views.save_case),
]