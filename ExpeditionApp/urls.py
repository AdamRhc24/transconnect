from django.urls import path
from .views import *

urlpatterns = [
    path("home/", home, name="home"),
    path("welcome/<str:name>", welcome, name="welcome"),
    path("list/", listExpeditions, name="list"),
    path("details/<int:pk>", detailsExpedition, name="details"),
    path(
        "delete/<int:pk>",
        delete,
        name="delete",
    ),
    path('expedition_list/', Expedition_list.as_view(), name='expedition_list'),
    path('expedition_detail/<int:pk>/', Expedition_Details.as_view(), name='expedition_detail'),
    path('expedition_delete/<int:pk>/', Expedition_Delete.as_view(), name='expedition_delete'),
    path('expedition_create/', Expedition_Create.as_view(), name='expedition_create'),
    path('expedition_update/<int:pk>/', Expedition_Update.as_view(), name='expedition_update'),
]
