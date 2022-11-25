from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    path('add_project', views.add_project, name='add_project'),
    path('projects', views.projects, name='projects'),
    path('update_project/<int:pk>', views.update_project, name='update_project'),
    path('delete_project/<int:pk>', views.delete_project, name='delete_project'),
    path('add_report', views.add_reports, name='add_report'),
    path('add_employee', views.add_employees, name='add_employee'),
    path('employees', views.employees, name='employees'),
    path('delete_employee/<int:pk>', views.delete_employee, name='delete_employee'),
    path('update_employee/<int:pk>', views.update_employee, name='update_employee'),
    path('reports', views.reports, name="reports"),
    path('reporte_udp/<int:pk>', views.reporte_udp, name="reporte_udp"),
    path('reporte_udp/reporte_udp2/<int:rep_key>', views.reporte_udp2, name="reporte_udp2"),
    path('charges', views.charges, name="charges"),
    path('add_charge', views.add_charge, name="add_charge"),
    path('update_charge/<int:pk>', views.update_charge, name="update_charge"),
    path('delete_charge/<int:pk>', views.delete_charge, name="delete_charge"),
    path('photos', views.photos, name="photos"),
    path('add_photos/', views.add_photos, name="add_photo_single"),
    path('reporte_udp/add_photo', views.add_photo, name="add_photo"),
    path('reporte_udp/add_photo2/<int:ph_fk_ph_key>', views.add_photo2, name="add_photo2"),
    path('delete_photo/<int:pk>', views.delete_photo, name="delete_photo"),
    path('update_photo/<int:pk>', views.update_photo, name="update_photo"),
    path('certification', views.certification, name="certification"),
    path('add_cert', views.add_cert, name="add_cert"),
    path('update_cert/<int:pk>', views.update_cert, name="update_cert"),
    path('delete_cert/<int:pk>', views.delete_cert, name="delete_cert"),
    path('delete_report/<int:pk>', views.delete_report),
    path('load_update_report_form/<int:pk>', views.load_update_report_form ),
    path('load_update_report_form/update_report/<int:pk>', views.update_report, name="update_report"),
    path('emailMessage', views.emailMessage, name="emailMessage"),
 
    
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

