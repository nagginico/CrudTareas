from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = 'index' ),
    path('task/', views.task, name = 'task'),
    path('task/<int:id_task>',views.task_detail, name = 'task_detail'),
    path('task/<int:id_task>/delete',views.task_delete, name = 'task_delete'),
    path('task/<int:id_task>/complete',views.task_complete, name = 'task_complete'),
    path('task/<int:id_task>/not_complete', views.task_not_complete, name = 'task_not_complete'),
    path('task/complete/all',views.task_complete_all, name = 'task_complete_all'),
    path('task/create', views.create_task, name = 'create'),
    path('logout/', views.signout, name = 'signout'),
    path('signin/', views.signin, name = 'signin'),
    path('signup/', views.signup, name = 'signup'),
]
