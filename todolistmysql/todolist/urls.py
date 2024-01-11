from todolist import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'todolist'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('accounts/profile/',views.task_list,name='task_logged'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'),name='logout'),
    path('signup/',views.SingUp.as_view(),name='signup'),
    path('add/', views.create_task, name='add'),
    path('task_list/', views.task_list, name='task_list'),
    path('task_list/<int:task_id>/make_completed/', views.task_completed,name='task_completed'),
    path('task_list/<int:task_id>/delete_task/', views.delete_task,name='delete_task'),
    path('task_list/<int:task_id>/edit/', views.TaskEditView.as_view(), name='edit_task'),
    
]