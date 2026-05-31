from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Category, Product

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

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
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
    return render(request, 'shop/profile.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('shop:home')




