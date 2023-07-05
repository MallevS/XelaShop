from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CheckoutForm, ItemForm
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
import random


# Create your views here.
def index(request):
    return render(request, "index.html")


def men_product(request):
    query = request.GET.get('search_query', '')
    category = request.GET.get('category')  # Use getlist to get multiple values
    material = request.GET.getlist('material')
    color = request.GET.getlist('color')
    size = request.GET.getlist('size')
    men_products = MenProduct.objects.filter(gender='M')

    if query:
        men_products = men_products.filter(category__name__icontains=query)
    if category:  # Use the plural form for the variable
        men_products = men_products.filter(category__in=category)
    if material:
        men_products = men_products.filter(material__in=material)
    if color:
        men_products = men_products.filter(color__in=color)
    if size:
        men_products = men_products.filter(size__in=size)

    return render(request, 'men.html', {'men_products': men_products, 'query': query, 'selected_categories': category,
                                        'selected_material': material, 'selected_color': color, 'selected_size': size,
                                        'user': request.user})


def women_product(request):
    query = request.GET.get('search_query', '')
    category = request.GET.get('category')
    material = request.GET.getlist('material')
    color = request.GET.getlist('color')
    size = request.GET.getlist('size')
    women_products = WomenProduct.objects.filter(gender='F')

    if query:
        women_products = women_products.filter(category__name__icontains=query)
    if category:
        women_products = women_products.filter(category__in=category)
    if material:
        women_products = women_products.filter(material__in=material)
    if color:
        women_products = women_products.filter(color__in=color)
    if size:
        women_products = women_products.filter(size__in=size)

    return render(request, 'women.html',
                  {'women_products': women_products, 'query': query, 'selected_categories': category,
                   'selected_material': material, 'selected_color': color, 'selected_size': size,
                   'user': request.user})


def search(request):
    search_query = request.GET.get('q')

    search_results = MenProduct.objects.filter(gender='M', name__icontains=search_query)

    return render(request, 'men.html', {'search_results': search_results, 'search_query': search_query})


def search_women(request):
    search_query = request.GET.get('q')

    search_results = WomenProduct.objects.filter(gender='F', name__icontains=search_query)

    return render(request, 'women.html', {'search_results': search_results, 'search_query': search_query})


@login_required(login_url='login')
def men_product_details(request, product_id):
    men_products = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        color = request.POST.get('color')
        size = request.POST.get('size')

        if quantity <= men_products.quantity:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=men_products)
            cart_item.quantity = quantity
            cart_item.color = color
            cart_item.size = size
            cart_item.save()
            return redirect('checkout')
        else:
            return HttpResponse("Insufficient quantity available")
    return render(request, 'menproduct.html', {'men_products': men_products})


@login_required(login_url='login')
def women_product_details(request, product_id):
    women_products = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        color = request.POST.get('color')
        size = request.POST.get('size')

        if quantity <= women_products.quantity:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=women_products)
            cart_item.quantity = quantity
            cart_item.color = color
            cart_item.size = size
            cart_item.save()
            return redirect('checkout')
        else:
            return HttpResponse("Insufficient quantity available")
    return render(request, 'womenproduct.html', {'women_products': women_products})


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    item.delete()
    return redirect('checkout')


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Product, item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menproduct', product_id=item.id)
        else:
            form = ItemForm(instance=item)
        return render(request, 'edit_product.html', {'form': form, 'item': item})


@login_required(login_url='login')
def add_item(request):
    items = CartItem.objects.filter(cart__user=request.user)
    cart_total = sum(item.product.price * item.quantity for item in items)
    context = {
        'cart_items': items,
        'total': cart_total,
        'colors': set(item.color for item in items),
        'sizes': set(item.size for item in items),
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def delete_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('checkout')


@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.cart = request.user.cart
            order.total_amount = order.calculate_total_amount()
            order.save()

            items = order.cart.items.all()
            for cart_item in items:
                cart_item.product.quantity -= cart_item.quantity
                cart_item.product.save()

            request.user.cart.items.all().delete()

            return redirect('final_site')
    else:
        form = CheckoutForm()

    cart_items = request.user.cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {'form': form, 'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def final_site(request):
    return render(request, 'order_confirmation.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password. Please try again.'})
    return render(request, 'login.html')


def generate_random_number():
    order_number = random.randint(100000, 999999)
    while Order.objects.filter(order_number=order_number).exists():
        order_number = random.randint(100000, 999999)
    return order_number


@login_required
def process_order(request):
    if request.method == 'POST':
        total_price = Decimal(request.POST.get('total_price'))
        payment_method = request.POST.get('payment_method')
        shipping_address = request.POST.get('shipping_address')
        product_ids = request.POST.getlist('products')
        products = Product.objects.filter(id__in=product_ids)
        customer = request.user

        order = Order(
            user=customer,
            order_number=generate_random_number(),
            cart=request.user.cart,
            total_amount=total_price,
            created_at=timezone.now(),
            status='Pending',
            payment_method=payment_method,
            shipping_method='Express',
            shipping_address=shipping_address,
        )
        order.save()

        order.products.set(products)

        order.total_amount = order.calculate_total_amount()
        order.save()

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html')


@login_required
def add_to_bag(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        quantity = int(request.POST.get('quantity'))

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return redirect('checkout')

    return HttpResponse('Invalid request')


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})
