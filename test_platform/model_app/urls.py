from django.urls import path
from model_app import views

urlpatterns = [
    #模块管理
    path('', views.model_manage),
    path('add_model/', views.add_model),
    path('del_model/<int:mid>/', views.del_model),
    path('edit_model/<int:mid>/', views.edit_model),

    #模块接口
    path('get_model_list/', views.get_model_list),

]