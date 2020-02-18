from django.urls import path
from project_app import views

urlpatterns = [

    #项目管理
    path('', views.project_manage),
    path('add_project/', views.add_project),
    path('del_project/<int:pid>/', views.del_project),
    path('edit_project/<int:pid>/', views.edit_project),
]