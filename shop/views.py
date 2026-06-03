from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta
from django.utils import timezone

from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Category, Product, Favorite


def money(value):
    return Decimal(str(value))


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
    product = get_object_or_404(Product, slug=slug, is_active=True)

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        ).exists()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
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


@login_required(login_url='shop:login')
def profile_view(request):
    display_name = (
        request.user.first_name
        or request.user.username.split('@')[0]
        or request.user.email.split('@')[0]
    )

    return render(request, 'shop/profile.html', {
        'display_name': display_name,
    })


@login_required(login_url='shop:login')
def orders_page(request):
    display_name = (
        request.user.first_name
        or request.user.username.split('@')[0]
        or request.user.email.split('@')[0]
    )

    return render(request, 'shop/orders.html', {
        'display_name': display_name,
    })


@login_required(login_url='shop:login')
def favorites_page(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('product')

    display_name = (
        request.user.first_name
        or request.user.username.split('@')[0]
        or request.user.email.split('@')[0]
    )

    return render(request, 'shop/favorites.html', {
        'favorites': favorites,
        'display_name': display_name,
    })


@login_required(login_url='shop:login')
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

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


def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('shop:home')


def custom_404_preview(request):
    return render(request, '404.html', status=404)


def get_cart(request):
    cart = request.session.get('cart')

    if cart is None:
        cart = {}
        request.session['cart'] = cart

    return cart


def get_cart_data(request):
    cart = get_cart(request)

    cart_items = []
    total_price = Decimal('0.00')
    total_quantity = 0

    for product_id, item in cart.items():
        product = Product.objects.filter(id=product_id, is_active=True).first()

        if product is None:
            continue

        try:
            quantity = int(item.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        price = money(item.get('price', product.price))
        item_total = price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
            'item_total': item_total,
        })

        total_price += item_total
        total_quantity += quantity

    shipping = Decimal('9.99') if total_quantity > 0 else Decimal('0.00')
    tax = Decimal('8.00') if total_quantity > 0 else Decimal('0.00')
    final_total = total_price + shipping + tax

    return {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'shipping': shipping,
        'tax': tax,
        'final_total': final_total,
    }


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_cart(request)

    product_id_str = str(product.id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += quantity
    else:
        cart[product_id_str] = {
            'quantity': quantity,
            'price': str(product.price),
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
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
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
    cart_data = get_cart_data(request)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_data['cart_items'],
        'total_price': cart_data['total_price'],
        'total_quantity': cart_data['total_quantity'],
        'shipping': cart_data['shipping'],
        'tax': cart_data['tax'],
        'final_total': cart_data['final_total'],
    })


def checkout(request):
    cart_data = get_cart_data(request)

    if cart_data['total_quantity'] == 0:
        return redirect('shop:cart_detail')

    if request.method == 'POST':
        request.session['checkout_contact'] = {
            'full_name': request.POST.get('full_name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
        }

        request.session.modified = True
        return redirect('shop:shipping')

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_data['cart_items'],
        'total_price': cart_data['total_price'],
        'total_quantity': cart_data['total_quantity'],
        'shipping': cart_data['shipping'],
        'tax': cart_data['tax'],
        'final_total': cart_data['final_total'],
    })


def shipping(request):
    cart_data = get_cart_data(request)

    if cart_data['total_quantity'] == 0:
        return redirect('shop:cart_detail')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        country = request.POST.get('country', '').strip()
        region = request.POST.get('region', '').strip()
        street = request.POST.get('street', '').strip()
        building = request.POST.get('building', '').strip()
        apartment = request.POST.get('apartment', '').strip()
        city = request.POST.get('city', '').strip()
        zip_code = request.POST.get('zip_code', '').strip()
        shipping_method = request.POST.get('shipping_method', '').strip()

        address_parts = []

        if street:
            address_parts.append(street)

        if building:
            address_parts.append(building)

        if apartment:
            address_parts.append(f'apt. {apartment}')

        if city:
            address_parts.append(city)

        if region:
            address_parts.append(region)

        if zip_code:
            address_parts.append(zip_code)

        if country:
            address_parts.append(country)

        shipping_address = ', '.join(address_parts) if address_parts else 'Address not provided'

        request.session['shipping_address'] = shipping_address
        request.session['shipping_data'] = {
            'full_name': full_name,
            'country': country,
            'region': region,
            'street': street,
            'building': building,
            'apartment': apartment,
            'city': city,
            'zip_code': zip_code,
            'shipping_method': shipping_method,
        }

        request.session.modified = True

        return redirect('shop:payment')

    return render(request, 'shop/shipping.html', {
        'cart_items': cart_data['cart_items'],
        'total_price': cart_data['total_price'],
        'total_quantity': cart_data['total_quantity'],
        'shipping': cart_data['shipping'],
        'tax': cart_data['tax'],
        'final_total': cart_data['final_total'],
    })


def payment(request):
    cart_data = get_cart_data(request)

    if cart_data['total_quantity'] == 0:
        return redirect('shop:cart_detail')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'Pay')

        order_items = []

        for item in cart_data['cart_items']:
            product = item['product']

            order_items.append({
                'id': product.id,
                'brand': product.brand,
                'name': product.name,
                'description': product.description,
                'width': product.width,
                'price': str(item['price']),
                'quantity': item['quantity'],
                'total': str(item['item_total']),
                'image_url': product.image.url if product.image else '',
            })

        delivery_date = timezone.now().date() + timedelta(days=2)

        request.session['last_order'] = {
            'order_id': '10300849',
            'delivery_date': delivery_date.strftime('%B %d, %Y'),
            'payment_method': payment_method,
            'address': request.session.get('shipping_address', 'Address not provided'),
            'items': order_items,
            'cart_count': cart_data['total_quantity'],
            'subtotal': str(cart_data['total_price']),
            'shipping': str(cart_data['shipping']),
            'tax': str(cart_data['tax']),
            'total': str(cart_data['final_total']),
        }

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('shop:order_confirmation')

    return render(request, 'shop/payment.html', {
        'cart_items': cart_data['cart_items'],
        'total_price': cart_data['total_price'],
        'total_quantity': cart_data['total_quantity'],
        'shipping': cart_data['shipping'],
        'tax': cart_data['tax'],
        'final_total': cart_data['final_total'],
    })


def order_confirmation(request):
    order = request.session.get('last_order')

    if not order:
        return redirect('shop:home')

    cart_items = []

    for item in order.get('items', []):
        cart_items.append({
            'id': item.get('id'),
            'brand': item.get('brand'),
            'name': item.get('name'),
            'description': item.get('description'),
            'width': item.get('width', '7.0"'),
            'price': money(item.get('price', '0')),
            'quantity': int(item.get('quantity', 1)),
            'total': money(item.get('total', '0')),
            'image_url': item.get('image_url', ''),
        })

    return render(request, 'shop/order_confirmation.html', {
        'order': order,
        'cart_items': cart_items,
        'cart_count': order.get('cart_count', 0),
        'subtotal': money(order.get('subtotal', '0')),
        'shipping': money(order.get('shipping', '0')),
        'tax': money(order.get('tax', '0')),
        'total': money(order.get('total', '0')),
        'delivery_date': order.get('delivery_date', 'June 02, 2026'),
        'order_id': order.get('order_id', '10300849'),
        'payment_method': order.get('payment_method', 'Pay'),
        'address': order.get('address', 'Address not provided'),
    })