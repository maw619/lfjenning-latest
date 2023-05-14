from django.urls import path
from . import views
from django.views import View


urlpatterns = [
 
    path('render_pdf_view/<pk>', views.render_pdf_view, name="render_pdf_view"),
    path('render_pdf_view_standalone/<pk>', views.render_pdf_view_standalone, name="render_pdf_view_standalone"),

]
