from django.urls import path
from . import views

urlpatterns = [
    path('entities/', views.entity_list, name='entity_list'),
    # path('entity-list/', views.entity_list, name='entity_list'),
]