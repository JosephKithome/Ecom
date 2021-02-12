from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import *
import datetime
from django.contrib.auth.models import User, auth


# Create your views here.
def duka(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    products = Product.objects.all()

    context = {'products': products,
               'cartItems': cartItems}
    return render(request, 'duka/duka.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "duka/checkout.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        try:
            carte = json.loads(request['cart'])
        except TypeError:
            carte = {}
        print('Cart:', carte)

        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

        for i in carte:
            cartItems += carte[i]["quantity"]

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "duka/cart.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

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

    return JsonResponse('Added to cart', safe=False)


def processOrder(request):
    # print('Data:', request.body)
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

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                address=data['shipping']['address'],
                zipcode=data['shipping']['zipcode'],
                # country=data['shipping']['country'],

            )

    else:
        print('User is not logged in...')
    return JsonResponse('Payment complete!', safe=False)

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         firstname = request.POST['firstname']
#         lastname = request.POST['lastname']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         email = request.POST['email']
#         # user = User.objects.create_user(username=username, firstname=firstname, lastname=lastname, password=password1,
#         #                                 email=email)
#         user.save()
#         print('User created successfully:')
#         return redirect('login')
#     else:
#         return render(request, 'duka/register.html')
