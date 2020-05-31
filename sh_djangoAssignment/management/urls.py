from django.urls import path
from . import views

app_name = 'management'
urlpatterns = [
    path('user/', views.user_homepage, name='user-homepage'),
    path('', views.homepage, name='homepage'),
    path('malfunction_reports/', views.list_malfunction, name='list-malfunction'),
    path('improvement_reports/', views.list_improvement, name='list-improvement'),
    path('<int:report_id>/detail_malfunction/', views.detail_malfunction, name='detail-malfunction'),
    path('<int:report_id>/detail_improvement/', views.detail_improvement, name='detail-improvement'),
    path('<int:report_id>/<str:validity>/malfunction/', views.validate_malfunction, name='validate-malfunction'),
    path('<int:report_id>/<str:validity>/improvement/', views.validate_improvement, name='validate-improvement'),
    path('report_malfunction/', views.create_malfunction, name='create-malfunction'),
    path('report_improvement/', views.create_improvement, name='create-improvement'),
    path('<int:task_id>/', views.task_completion, name='task-completion'),
    path('<int:investigate_id>/create_malfunction_task/', views.create_malfunction_task, name='create-malfunction-task'),

]