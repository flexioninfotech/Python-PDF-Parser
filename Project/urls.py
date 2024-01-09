from django.urls import path
from .views import *
urlpatterns = [
    path('parse/',ParsePDFView.as_view()),
]
