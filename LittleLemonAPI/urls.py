from django.urls import path
from . import views

urlpatterns = [
    path('api/menu-items/', views.menu_items, name='menu_items'),
    path('api/single-items/<int:id>/', views.single_item, name='single_item'),
]
