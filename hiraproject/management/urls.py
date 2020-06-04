from django.urls import path
from . import views
from .views import UserHomepage,Homepage,MalfunctionList,ImprovementList,MalfunctionDetail,ImprovementDetail,\
    MalfunctionCreate,ImprovementCreate,MalfunctionTaskCreate,TaskCompletion

app_name = 'management'
urlpatterns = [
    path('', UserHomepage.as_view(), name='user-homepage'),
    path('staff/', Homepage.as_view(), name='homepage'),
    path('malfunction_reports/', MalfunctionList.as_view(), name='list-malfunction'),
    path('improvement_reports/', ImprovementList.as_view(), name='list-improvement'),

    path('detail_malfunction/<int:report_id>/', MalfunctionDetail.as_view(), name='detail-malfunction'),
    path('detail_improvement/<int:report_id>', ImprovementDetail.as_view(), name='detail-improvement'),

    path('<int:report_id>/<str:validity>/malfunction/', views.MalfunctionValidate.as_view(), name='validate-malfunction'),
    path('<int:report_id>/<str:validity>/improvement/', views.ImprovementValidate.as_view(), name='validate-improvement'),

    path('report_malfunction/', MalfunctionCreate.as_view(), name='create-malfunction'),
    path('report_improvement/', ImprovementCreate.as_view(), name='create-improvement'),

    path('<int:task_id>/', TaskCompletion.as_view(), name='task-completion'),
    path('<int:investigate_id>/create_malfunction_task/', MalfunctionTaskCreate.as_view() , name='create-malfunction-task'),
]
