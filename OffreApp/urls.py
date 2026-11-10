from django.urls import path
from .views import *

urlpatterns = [
    path('offre_list/', Offre_list.as_view(), name='offre_list'),
    path('offre_detail/<int:pk>/', Offre_Details.as_view(), name='offre_detail'),
    path('offre_create/', Offre_Create.as_view(), name='offre_create'),
    path('offre_update/<int:pk>/', Offre_Update.as_view(), name='offre_update'),
    path('offre_delete/<int:pk>/', Offre_Delete.as_view(), name='offre_delete'),
]
