from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem, Order, OrderItem, Category, Review, UserProfile


def product_list(request):
    products = Product.objects.all()
    data = {"products": list(products.values())}
    return JsonResponse(data)


def category_list(request):
    categories = Category.objects.all()
    data = {"categories": list(categories.values())}
    return JsonResponse(data)


def review_list(request):
    reviews = Review.objects.all()
    data = {"reviews": list(reviews.values())}
    return JsonResponse(data)


def profile_detail(request, user_id):
    profile = get_object_or_404(UserProfile, user_id=user_id)
    data = {"profile": model_to_dict(profile)}
    return JsonResponse(data)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    data = {"product": model_to_dict(product)}
    return JsonResponse(data)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return JsonResponse({"status": "success"})


def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = list(cart.cartitem_set.all().values())
    total_price = str(cart.total_price)  # Преобразуем Decimal в строку
    data = {"cart": {"items": cart_items, "total_price": total_price}}
    return JsonResponse(data)




def create_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    order = Order.objects.create(user=request.user, total_price=cart.total_price, status='pending')
    for cart_item in cart.cartitem_set.all():
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
    cart.delete()
    return JsonResponse({"status": "success"})


def order_confirmation(request):
    return JsonResponse({"status": "success"})
