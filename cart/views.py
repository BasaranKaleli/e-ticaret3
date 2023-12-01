from django.shortcuts import render, redirect,  get_object_or_404
from .models import ShoppingCart, ShoppingCartItem

def shopping_cart_item_add(request, cart_item_id):
    if request.user.is_authenticated:
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user, status="waiting")
        if  shopping_cart.count() > 0:
            shopping_cart = shopping_cart.last()
        else:
            shopping_cart = ShoppingCart.objects.create(user=user)
        
        shopping_cart.session_key = request.session.session_key
        item = ShoppingCartItem.objects.get(pk=cart_item_id)
        print(item)
        shopping_cart.items.add(item)
        shopping_cart.total_price_update()
        shopping_cart.save()
    return redirect('/')

def shopping_cart_item_delete(request, cart_item_id):
    if request.user.is_authenticated:
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user, status="waiting").last()
        if shopping_cart:
            item = get_object_or_404(ShoppingCartItem, pk=cart_item_id)
            shopping_cart.items.remove(item)
            shopping_cart.total_price_update()
            shopping_cart.save()
    return redirect('cart_view')

def shopping_cart_item_edit(request, cart_item_id):
    if request.user.is_authenticated:
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user, status="waiting").last()
        if shopping_cart:
            item = get_object_or_404(ShoppingCartItem, pk=cart_item_id)
            
            if request.method == 'POST':
                quantity = request.POST.get('quantity')
                item.quantity = quantity
                item.save()
            shopping_cart.total_price_update()
            shopping_cart.save()
    return redirect('cart_view')