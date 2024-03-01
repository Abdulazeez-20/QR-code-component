from django.urls import path
from . import views

urlpatterns = [
    # path('menu-item', views.menuItem),
    path('menu-item', views.MenuItemSet.as_view({'get': 'list'})),
    path('menu-item/<int:pk>', views.MenuItemSet.as_view({'get': 'retrieve'})),
    path('menu', views.menu)
]
