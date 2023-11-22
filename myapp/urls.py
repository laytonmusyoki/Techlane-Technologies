from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('profile/',profile,name='profile'),
    path('settings/',settings,name='settings'),
    path('helpcenter/',helpcenter,name='helpcenter'),
    path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),
    path('update_item/', updateItem, name="update_item"),
    path('process_order/', processOrder, name="process_order"),
    path('add_items/', add_items, name="add_items"),
    path('all_products/', all_products, name="all_products"),
    path('transactions/', transactions, name="transactions"),
    path('update/<str:pk>/', update, name="update"),
    path('delete/<str:pk>/', delete, name="delete")
]

