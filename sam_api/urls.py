from django.urls import path
from . import views

urlpatterns = [
    path('entities/', views.entity_list, name='entity_list'),
    path('fetch_opportunities/', views.fetch_opportunities_view, name='fetch_opportunities'),
    # path('entity-list/', views.entity_list, name='entity_list'),
]