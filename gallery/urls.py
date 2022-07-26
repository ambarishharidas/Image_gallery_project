from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index),
    path('load/',views.load),
    path('displaybig/',views.displaybig),
]