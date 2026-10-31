from django.urls import path
from .views import *

urlpatterns = [
    path("home/", home, name="home"),
    path("welcome/<str:name>", welcome, name="welcome"),
    path('list/', listExpeditions, name="list"),
    path('details/<int:pk>', detailsExpedition, name="details")
    path('delete/<int:pk>', )
]
