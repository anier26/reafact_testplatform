from django.urls import path
from testcase_app import views

urlpatterns = [

    #用例管理
    path('', views.case_manage),
    path('debug', views.debug),
    path('case_add', views.case_add),
    path('case_edit/<int:cid>/', views.case_edit),
    path('case_del/<int:cid>/', views.case_del),

    path('case_list', views.case_manage),
    path('asserts', views.asserts),
    path('save_case', views.save_case),

    path('get_case_info', views.get_case_info),
    path('get_select_data', views.get_select_data),
]