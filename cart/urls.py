from django.urls import path
from .views import (
    shopping_cart_item_add, shopping_cart_item_delete, shopping_cart_item_edit
)


urlpatterns = [
    path('add/<int:cart_item_id>/', shopping_cart_item_add, name='shopping_cart_item_add'),
    path('remove/<int:cart_item_id>/', shopping_cart_item_delete, name='shopping_cart_item_remove'),
    path('edit/<int:cart_item_id>/', shopping_cart_item_edit, name='shopping_cart_item_edit'),  
] 
