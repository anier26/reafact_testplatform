from django.urls import path
from testcase_app import views

urlpatterns = [

    #项目管理
    path('', views.testcase_manage),
    path('debug', views.debug),
    path('asserts', views.asserts),
    path('save_case', views.save_case),
]