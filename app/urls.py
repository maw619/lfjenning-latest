from django.urls import path
from . import views
from django.views import View


urlpatterns = [
    path('app/', views.venue_pdf, name="venue_pdf"),
    path('app/', views.render_pdf_view, name="generate_pdf"),
]
