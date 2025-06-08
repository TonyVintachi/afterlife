from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('case/<int:case_id>/report/autopsy/', views.autopsy_report_detail_view, name='autopsy_report_detail'),
    path('case/<int:case_id>/toxicology/', views.toxicology_report_list_view, name='toxicology_report_list'),
    path('toxicology/<int:report_id>/', views.toxicology_report_detail_view, name='toxicology_report_detail'),
]
