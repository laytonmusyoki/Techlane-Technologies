from .models import Profile,Order
from django.shortcuts import render,redirect


def profile_image(request):
    user=request.user
    if user.is_authenticated:
        profile,created=Profile.objects.get_or_create(name=user)
        return {"profile":profile}


""" def cartitems(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {"items":items, "order":order, "cartItems":cartItems}
    return render(request, 'cart.html', context) """


