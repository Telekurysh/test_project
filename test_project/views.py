from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Order, OrderItem, Category, Review, UserProfile


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'review_list.html', {'reviews': reviews})


def profile_detail(request, user_id):
    profile = UserProfile.objects.get(user_id=user_id)
    return render(request, 'profile_detail.html', {'profile': profile})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})


def create_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    order = Order.objects.create(user=request.user, total_price=cart.total_price, status='pending')
    for cart_item in cart.cartitem_set.all():
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
    cart.delete()
    return redirect('order_confirmation')


def order_confirmation(request):
    return render(request, 'order_confirmation.html')
