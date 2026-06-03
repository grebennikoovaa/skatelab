from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Category, Product
from .models import Product, ProductGalleryImage, ProductSpecification
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CustomerProfile, Favorite
from .forms import CustomerProfileForm
from django.contrib.auth import logout



def home(request):
    products = Product.objects.filter(is_active=True)[:8]

    return render(request, 'shop/home.html', {
        'products': products
    })


def categories(request):
    categories_list = Category.objects.filter(is_active=True)

    return render(request, 'shop/categories.html', {
        'categories': categories_list
    })


def complete_skateboards(request):
    category = get_object_or_404(Category, slug='complete-skateboards')

    products = Product.objects.filter(
        category=category,
        is_active=True
    )

    selected_brands = request.GET.getlist('brand')
    selected_levels = request.GET.getlist('level')
    selected_widths = request.GET.getlist('width')

    min_price = request.GET.get('min_price', '59')
    max_price = request.GET.get('max_price', '503')

    try:
        min_price_number = int(min_price)
    except ValueError:
        min_price_number = 59

    try:
        max_price_number = int(max_price)
    except ValueError:
        max_price_number = 503

    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    if selected_levels:
        products = products.filter(level__in=selected_levels)

    if selected_widths:
        products = products.filter(width__in=selected_widths)

    products = products.filter(
        price__gte=min_price_number,
        price__lte=max_price_number
    )

    active_filters_count = len(selected_brands) + len(selected_levels) + len(selected_widths)

    if min_price_number != 59 or max_price_number != 503:
        active_filters_count += 1

    return render(request, 'shop/complete_skateboards.html', {
        'category': category,
        'products': products,
        'selected_brands': selected_brands,
        'selected_levels': selected_levels,
        'selected_widths': selected_widths,
        'min_price': min_price_number,
        'max_price': max_price_number,
        'active_filters_count': active_filters_count,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        ).exists()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'is_favorite': is_favorite,
    })

def register_view(request):
    if request.user.is_authenticated:
        return redirect('shop:profile')

    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('shop:profile')
    else:
        form = CustomerRegisterForm()

    return render(request, 'shop/register.html', {
        'form': form
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:profile')

    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:
                login(request, user)

                if not remember_me:
                    request.session.set_expiry(0)

                messages.success(request, 'You are logged in.')
                return redirect('shop:profile')

            form.add_error(None, 'Invalid email or password.')
    else:
        form = CustomerLoginForm()

    return render(request, 'shop/login.html', {
        'form': form
    })


@login_required
def profile_view(request):
    customer_profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    favorites_count = Favorite.objects.filter(user=request.user).count()

    if request.method == 'POST':
        form = CustomerProfileForm(
            request.POST,
            user=request.user,
            customer_profile=customer_profile
        )

        if form.is_valid():
            form.save()
            return redirect('shop:profile')
    else:
        form = CustomerProfileForm(
            user=request.user,
            customer_profile=customer_profile
        )

    return render(request, 'shop/profile.html', {
        'form': form,
        'customer_profile': customer_profile,
        'favorites_count': favorites_count,
    })


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_cart(request)

    product_id_str = str(product.id)

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'quantity': 1,
            'price': product.price,
        }

    request.session['cart'] = cart
    request.session.modified = True

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'shop:cart_detail'
    return redirect(next_url)


def cart_remove(request, product_id):
    cart = get_cart(request)
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('shop:cart_detail')


def cart_update(request, product_id):
    cart = get_cart(request)
    product_id_str = str(product_id)

    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)

        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1

        if quantity <= 0:
            if product_id_str in cart:
                del cart[product_id_str]
        else:
            if product_id_str in cart:
                cart[product_id_str]['quantity'] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('shop:cart_detail')


def cart_clear(request):
    request.session['cart'] = {}
    request.session.modified = True

    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = get_cart(request)

    cart_items = []
    total_price = 0
    total_quantity = 0

    for product_id, item in cart.items():
        product = Product.objects.filter(id=product_id, is_active=True).first()

        if product is None:
            continue

        quantity = item.get('quantity', 1)
        item_total = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

        total_price += item_total
        total_quantity += quantity

    shipping = 9.99
    tax = 8
    final_total = total_price + shipping + tax

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'shipping': shipping,
        'tax': tax,
        'final_total': final_total,
    })

def checkout(request):
    cart = get_cart(request)

    cart_items = []
    total_price = 0
    total_quantity = 0

    for product_id, item in cart.items():
        product = Product.objects.filter(id=product_id, is_active=True).first()

        if product is None:
            continue

        quantity = item.get('quantity', 1)
        item_total = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

        total_price += item_total
        total_quantity += quantity

    if total_quantity == 0:
        return redirect('shop:cart_detail')

    shipping = 9.99
    tax = 8
    final_total = total_price + shipping + tax

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        request.session['checkout_contact'] = {
            'full_name': full_name,
            'email': email,
            'phone': phone,
        }

        request.session.modified = True

        return redirect('shop:shipping')

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'shipping': shipping,
        'tax': tax,
        'final_total': final_total,
    })

def shipping(request):
    cart = get_cart(request)

    cart_items = []
    total_price = 0
    total_quantity = 0

    for product_id, item in cart.items():
        product = Product.objects.filter(id=product_id, is_active=True).first()

        if product is None:
            continue

        quantity = item.get('quantity', 1)
        item_total = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

        total_price += item_total
        total_quantity += quantity

    if total_quantity == 0:
        return redirect('shop:cart_detail')

    if request.method == 'POST':
        request.session['shipping_address'] = {
            'full_name': request.POST.get('full_name'),
            'country': request.POST.get('country'),
            'region': request.POST.get('region'),
            'street': request.POST.get('street'),
            'building': request.POST.get('building'),
            'apartment': request.POST.get('apartment'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip_code'),
            'shipping_method': request.POST.get('shipping_method'),
        }

        request.session.modified = True

        return redirect('shop:payment')

    return render(request, 'shop/shipping.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    })



def payment(request):
    cart = request.session.get('cart', {})

    cart_items = []
    subtotal = Decimal('0.00')
    cart_count = 0

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)

        quantity = int(item.get('quantity', 1))
        price = Decimal(str(item.get('price', product.price)))
        total = price * quantity

        cart_items.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'width': getattr(product, 'width', '7.0'),
            'price': str(price),
            'quantity': quantity,
            'total': str(total),
            'image_url': product.image.url if getattr(product, 'image', None) else '',
        })

        subtotal += total
        cart_count += quantity

    shipping = Decimal('9.99') if subtotal > 0 else Decimal('0.00')
    tax = Decimal('8.00') if subtotal > 0 else Decimal('0.00')
    total_amount = subtotal + shipping + tax

    if request.method == 'POST':
        request.session['last_order'] = {
            'items': cart_items,
            'cart_count': cart_count,
            'subtotal': str(subtotal),
            'shipping': str(shipping),
            'tax': str(tax),
            'total': str(total_amount),
            'delivery_date': 'June 02, 2026',
            'order_id': '10300849',
            'payment_method': 'Pay',
            'address': request.session.get('shipping_address', '6391 Elgin St....'),
        }

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('shop:order_confirmation')

    return render(request, 'shop/payment.html', {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total_amount,
    })

from decimal import Decimal
from django.shortcuts import render


def order_confirmation(request):
    order = request.session.get('last_order')

    if not order:
        return render(request, 'shop/order_confirmation.html', {
            'cart_items': [],
            'cart_count': 0,
            'subtotal': Decimal('0.00'),
            'total': Decimal('0.00'),
            'delivery_date': 'June 02, 2026',
            'order_id': '10300849',
            'payment_method': 'Pay',
            'address': '6391 Elgin St....',
        })

    cart_items = []

    for item in order.get('items', []):
        price = Decimal(str(item.get('price', '0')))
        total = Decimal(str(item.get('total', '0')))

        cart_items.append({
            'id': item.get('id'),
            'name': item.get('name'),
            'brand': item.get('brand'),
            'width': item.get('width', '7.0'),
            'price': price,
            'quantity': item.get('quantity', 1),
            'total': total,
            'image_url': item.get('image_url', ''),
        })

    return render(request, 'shop/order_confirmation.html', {
        'cart_items': cart_items,
        'cart_count': order.get('cart_count', 0),
        'subtotal': Decimal(str(order.get('subtotal', '0'))),
        'shipping': Decimal(str(order.get('shipping', '0'))),
        'tax': Decimal(str(order.get('tax', '0'))),
        'total': Decimal(str(order.get('total', '0'))),
        'delivery_date': order.get('delivery_date', 'June 02, 2026'),
        'order_id': order.get('order_id', '10300849'),
        'payment_method': order.get('payment_method', 'Pay'),
        'address': order.get('address', '6391 Elgin St....'),
    })

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        favorite.delete()

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'

    return redirect(next_url)

@login_required
def orders_page(request):
    return render(request, 'shop/orders.html')


def logout_view(request):
    logout(request)
    return redirect('shop:home')

def custom_404_preview(request):
    return render(request, '404.html', status=404)

def get_cart(request):
    cart = request.session.get('cart')

    if cart is None:
        cart = {}
        request.session['cart'] = cart

    return cart


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = get_cart(request)

    product_id_str = str(product.id)

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'quantity': 1,
            'price': str(product.price),
        }

    request.session['cart'] = cart
    request.session.modified = True

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'shop:cart_detail'
    return redirect(next_url)

@login_required
def favorites_page(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    display_name = request.user.first_name or request.user.username.split('@')[0]

    return render(request, 'shop/favorites.html', {
        'favorites': favorites,
        'display_name': display_name,
    })

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    favorite = Favorite.objects.filter(
        user=request.user,
        product=product
    ).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            product=product
        )

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'shop:favorites'
    return redirect(next_url)


@login_required
def favorites_page(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('product')

    display_name = request.user.first_name or request.user.username.split('@')[0]

    return render(request, 'shop/favorites.html', {
        'favorites': favorites,
        'display_name': display_name,
    })