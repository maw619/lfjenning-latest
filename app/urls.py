from django.urls import path
from . import views
from django.views import View


urlpatterns = [
 
    path('render_pdf_view/<rep_key>', views.render_pdf_view, name="render_pdf_view"),
]
