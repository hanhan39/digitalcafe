from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, CartItem, Transaction, LineItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import (
    login, logout, authenticate
)
from django.contrib import messages
import datetime as dt

# Create your views here.
@login_required
def index(request):
    products = Product.objects.all()
    context = {
        "user": request.user,
        "product_data": products,
    }
    return render(request, 'core/index.html', context)

@login_required
def product_detail(request, product_id):
    if request.method == 'GET':
        p = Product.objects.get(id=product_id)
        context = {
            "product": p
        }
        return render(request, 'core/product_detail.html', context)
    elif request.method == 'POST':
        submitted_quantity = request.POST['quantity']
        submitted_product_id = request.POST['product_id']
        product = Product.objects.get(id=submitted_product_id)
        user = request.user
        cart_item = CartItem(user=user, product=product, quantity=submitted_quantity)
        cart_item.save()
        messages.add_message(
            request,
            messages.INFO,
            f'Added {submitted_quantity} of {product.name} to your cart'
        )
        return redirect('index')

def checkout(request):
    if request.method == 'GET':
        cart_items = CartItem.objects.filter(user=request.user)
        context = {
            'cart_items': list(cart_items),
        }
        return render(request, 'core/checkout.html', context)
    elif request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        created_at = dt.datetime.now(tz=dt.timezone.utc)
        transaction = Transaction(user=request.user, created_at=created_at)
        transaction.save()
        for cart_item in cart_items:
            line_item = LineItem(
                transaction=transaction,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )
            line_item.save()
            cart_item.delete()
        messages.add_message(request, messages.INFO, f'Thank you for your purchase!')
        return redirect('index')

@login_required
def transaction_history(request):
    history = Transaction.objects.filter(user=request.user)
    lineitems = LineItem.objects.all()
    context = {
        'user': request.user,
        'history': list(history),
        'lineitems': lineitems,
    }
    return render(request, 'core/transaction_history.html', context)

def login_view(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'core/login_view.html', context)
    elif request.method == 'POST':
        submitted_username = request.POST['username']
        submitted_password = request.POST['password']
        user_object = authenticate(
            username=submitted_username,
            password=submitted_password
        )
        if user_object is None:
            messages.add_message(request, messages.INFO, 'Invalid login.')
            return redirect(request.path_info)
        login(request, user_object)
        return redirect('index')