from django.shortcuts import render,redirect
from django.http import JsonResponse
from .forms import ProductForm,Profileform
from django.contrib import messages
from .models import Product
import json
import datetime
from .decorators import unauthenticated_user,allowed_users

from .models import *

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {"products":products, "cartItems":cartItems}
    return render(request, 'index.html',context)


def store(request):
    return render(request, 'shop/store.html')

def cart(request):
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
    return render(request, 'cart.html', context)



def checkout(request):
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
    
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            shippingAddress = Shipping.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                    )
    else:
        print('User is not logged in..')
    return JsonResponse('Payment submitted..', safe=False)



def profile(request):
    user=request.user
    profile,created=Profile.objects.get_or_create(name=user)
    context={
        "profile":profile
    }
    return render(request,'profile.html',context)


def settings(request):
    user=request.user
    profile,created=Profile.objects.get_or_create(name=user)
    form=Profileform(instance=profile)
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('settings')
    context={
        "forms":form
    }
    return render(request,'setting.html',context)


def helpcenter(request):
    return render(request,'help-center.html')



@allowed_users(allowed_roles=['admin'])
def add_items(request):
    form=ProductForm
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,'Item added successfully')
            return redirect('all_products')
    context={
        "forms":form
    }
    return render(request,'add_product.html',context)



@allowed_users(allowed_roles=['admin'])
def update(request,pk):
    item=Product.objects.get(id=pk)
    form=ProductForm(instance=item)
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            messages.info(request,'Item updated successfully')
            return redirect('all_products')
    context={
        "forms":form
    }
    return render(request,'update_product.html',context)

def transactions(request):
    return render(request,'transactions.html')


@allowed_users(allowed_roles=['admin'])
def all_products(request):
    items=Product.objects.all()
    context={
        "items":items
    }
    return render(request,'all_products.html',context)

@allowed_users(allowed_roles=['admin'])
def delete(request,pk):
    item=Product.objects.get(id=pk)
    item.delete()
    messages.success(request,'Item deleted successfully')
    return redirect('all_products')