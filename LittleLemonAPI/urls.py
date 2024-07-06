from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

router.register('menu-item-viewset', views.MenuItemsViewSet)
urlpatterns = [
    path('api/menu-items/', views.menu_items, name='menu_items'),
    path('api/secret/', views.secret, name='secret'),
    path('api/manager-view/', views.manager_view),
    path('api/api-token-auth/', obtain_auth_token),
    path('api/single-items/<int:id>/', views.single_item, name='single_item'),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
    path('api/', include(router.urls)),

]
