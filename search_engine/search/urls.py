from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('results/', views.search_results, name='search_results'),
    path('item/<str:item_code>/', views.item_detail, name='item_detail'),
]
