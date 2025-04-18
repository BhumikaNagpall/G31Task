from django.urls import path
from DashboardApp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.dashboard_page,name="dashboard_page"),
    path('addtask/',views.add_task_view,name="addtask"),
    path('deletetask/<int:id>/',views.delete_task_view, name="deletetask"),
    path("task/<int:task_id>/edit_progress/", views.edit_progress, name="edit_progress"),
    path('completed/', views.completed_tasks, name='completed_tasks'),
    path('updatetask/<int:id>/',views.update_task_view,name="updatetask"),
    path('taskcalender/',views.calender_view,name="taskcalender"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tasks/', views.task_list, name='task_list'),
    # path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:id>/',views.delete_task_view_new,name='delete_task'),
    path('admin/tasks/', views.admin_tasks_view, name='admin_tasks'),  
    path('admin/user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('staff/tasks/', views.staff_tasks_view, name='staff_tasks_view'),
    path('admin/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/tasks/edit_task/<int:id>/', views.edit_task, name='edit_task'),  
    # path('dashboard/admin/tasks/edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
]

