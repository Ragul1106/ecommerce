from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Category, Product, Order, OrderItem

def healthcheck(request):
    return JsonResponse({"status": "ok"})

def home(request):
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {'categories': categories})

def products(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'shop/products.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/products.html', {'products': products, 'category': category})

def cart(request):
    # Basic cart implementation using session
    cart = request.session.get('cart', {})
    cart_items = []
    total_amount = 0
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total
        })
        total_amount += item_total
    
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, 'Product added to cart!')
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, 'Product removed from cart!')
    return redirect('cart')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            customer_name=request.POST['customer_name'],
            customer_email=request.POST['customer_email']
        )
        
        # Add products to order
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=product.price
            )
        
        # Clear cart
        request.session['cart'] = {}
        return redirect('order_success', order_id=order.id)
    
    # GET request - show checkout form
    cart_items = []
    total_amount = 0
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total
        })
        total_amount += item_total
    
    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})
