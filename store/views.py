"""Views for the Store app."""
import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Product, Category, Brand, Cart, CartItem, Order, OrderItem,
    ShippingAddress, Review, Wishlist, ProductImage
)
from .forms import (
    SearchForm, FilterForm, AddToCartForm, CartItemUpdateForm,
    ShippingAddressForm, ReviewForm, CheckoutForm
)


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create cart and wishlist for new user
            Cart.objects.create(user=user)
            Wishlist.objects.create(user=user)
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def home(request):
    """Homepage view."""
    featured_products = Product.objects.filter(
        is_available=True,
        stock__gt=0
    ).prefetch_related('images').order_by('-created_at')[:8]

    categories = Category.objects.filter(parent__isnull=True)[:6]
    brands = Brand.objects.all()[:6]

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'brands': brands,
        'search_form': SearchForm(),
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    """Product listing with search, filter, sort, and pagination."""
    products = Product.objects.filter(is_available=True).prefetch_related('images', 'brand')

    # Search
    search_form = SearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data.get('query'):
        query = search_form.cleaned_data['query']
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query)
        )

    # Filter
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    min_price = request.GET.get('min_price')
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except:
            pass

    max_price = request.GET.get('max_price')
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except:
            pass

    vram = request.GET.get('vram')
    if vram:
        products = products.filter(vram=int(vram))

    gpu_series = request.GET.get('gpu_series')
    if gpu_series:
        products = products.filter(gpu_series__icontains=gpu_series)

    memory_type = request.GET.get('memory_type')
    if memory_type:
        products = products.filter(memory_type__icontains=memory_type)

    in_stock = request.GET.get('in_stock')
    if in_stock:
        products = products.filter(stock__gt=0)

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Sort
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = ['price', '-price', 'name', '-name', '-created_at', 'created_at']
    if sort in valid_sorts:
        products = products.order_by(sort)

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Filter options
    brands = Brand.objects.all()
    categories = Category.objects.all()
    vram_options = Product.objects.values_list('vram', flat=True).distinct().order_by('vram')
    gpu_series_options = Product.objects.values_list('gpu_series', flat=True).distinct().order_by('gpu_series')
    memory_types = Product.objects.values_list('memory_type', flat=True).distinct().order_by('memory_type')

    context = {
        'products': products,
        'search_form': search_form,
        'brands': brands,
        'categories': categories,
        'vram_options': vram_options,
        'gpu_series_options': gpu_series_options,
        'memory_types': memory_types,
        'current_filters': {
            'brand': brand_slug,
            'category': category_slug,
            'min_price': min_price,
            'max_price': max_price,
            'vram': vram,
            'gpu_series': gpu_series,
            'memory_type': memory_type,
            'in_stock': in_stock,
            'sort': sort,
            'query': request.GET.get('query', ''),
        }
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """Product detail page."""
    product = get_object_or_404(
        Product.objects.prefetch_related('images', 'specifications', 'reviews'),
        slug=slug
    )

    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')[:5]

    # Check if product is in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        try:
            in_wishlist = request.user.wishlist.products.filter(id=product.id).exists()
        except Wishlist.DoesNotExist:
            pass

    # Check if user has already reviewed
    has_reviewed = False
    if request.user.is_authenticated:
        has_reviewed = Review.objects.filter(product=product, user=request.user).exists()

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'in_wishlist': in_wishlist,
        'has_reviewed': has_reviewed,
        'add_to_cart_form': AddToCartForm(),
        'review_form': ReviewForm(),
    }
    return render(request, 'store/product_detail.html', context)


@login_required
def cart_detail(request):
    """Shopping cart detail page."""
    try:
        cart = Cart.objects.prefetch_related('items__product__images').get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    subtotal = Decimal('0')
    if cart:
        subtotal = cart.total

    shipping = Decimal('9.99') if subtotal > 0 else Decimal('0')
    if subtotal >= Decimal('500'):
        shipping = Decimal('0')

    tax = subtotal * Decimal('0.08')  # 8% tax
    total = subtotal + shipping + tax

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    return render(request, 'store/cart_detail.html', context)


@login_required
@require_POST
def cart_add(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, id=product_id)

    form = AddToCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']

        # Check stock
        if quantity > product.stock:
            messages.error(request, f'Only {product.stock} items available in stock.')
            return redirect('store:product_detail', slug=product.slug)

        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                messages.error(request, f'Cannot add more. Only {product.stock} items in stock.')
                return redirect('store:product_detail', slug=product.slug)
            cart_item.quantity = new_quantity
            cart_item.save()

        messages.success(request, f'{product.name} added to cart.')
        return redirect('store:cart_detail')

    return redirect('store:product_detail', slug=product.slug)


@login_required
@require_POST
def cart_update(request, item_id):
    """Update cart item quantity."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    form = CartItemUpdateForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']

        if quantity > cart_item.product.stock:
            messages.error(request, f'Only {cart_item.product.stock} items available.')
            return redirect('store:cart_detail')

        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')

    return redirect('store:cart_detail')


@login_required
def cart_remove(request, item_id):
    """Remove item from cart."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('store:cart_detail')


@login_required
def checkout(request):
    """Checkout page."""
    try:
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('store:cart_detail')

    if cart.item_count == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('store:cart_detail')

    # Get user's addresses
    addresses = ShippingAddress.objects.filter(user=request.user)

    subtotal = cart.total
    shipping = Decimal('9.99')
    if subtotal >= Decimal('500'):
        shipping = Decimal('0')
    tax = subtotal * Decimal('0.08')
    total = subtotal + shipping + tax

    if request.method == 'POST':
        address_form = ShippingAddressForm(request.POST)
        checkout_form = CheckoutForm(request.POST)

        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('store:checkout_process') + f'?address_id={address.id}'

    else:
        address_form = ShippingAddressForm()
        checkout_form = CheckoutForm()

    context = {
        'cart': cart,
        'addresses': addresses,
        'address_form': address_form,
        'checkout_form': checkout_form,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def checkout_process(request):
    """Process the checkout and create order."""
    try:
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('store:cart_detail')

    address_id = request.GET.get('address_id') or request.POST.get('shipping_address_id')
    if not address_id:
        messages.error(request, 'Please select a shipping address.')
        return redirect('store:checkout')

    try:
        address = ShippingAddress.objects.get(id=address_id, user=request.user)
    except ShippingAddress.DoesNotExist:
        messages.error(request, 'Invalid shipping address.')
        return redirect('store:checkout')

    if request.method == 'POST':
        # Calculate totals
        subtotal = cart.total
        shipping = Decimal('9.99')
        if subtotal >= Decimal('500'):
            shipping = Decimal('0')
        tax = subtotal * Decimal('0.08')
        total = subtotal + shipping + tax

        # Create order
        order = Order.objects.create(
            user=request.user,
            order_number=f'POO-{uuid.uuid4().hex[:10].upper()}',
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            total=total,
            shipping_address=address,
            is_demo=True,  # Mark as demo transaction
        )

        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity,
                subtotal=item.subtotal
            )

            # Update stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear cart
        cart.items.all().delete()

        messages.success(request, f'Order #{order.order_number} placed successfully! (Demo Mode)')
        return redirect('store:checkout_confirmation', order_number=order.order_number)

    return redirect('store:checkout')


@login_required
def checkout_confirmation(request, order_number):
    """Order confirmation page."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'store/checkout_confirmation.html', context)


@login_required
def order_list(request):
    """User's order history."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'store/order_list.html', context)


@login_required
def order_detail(request, order_number):
    """Order detail page."""
    order = get_object_or_404(
        Order.objects.prefetch_related('items'),
        order_number=order_number,
        user=request.user
    )

    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)


@login_required
def wishlist_detail(request):
    """User's wishlist."""
    try:
        wishlist = Wishlist.objects.prefetch_related('products__images').get(user=request.user)
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user)

    context = {
        'wishlist': wishlist,
    }
    return render(request, 'store/wishlist.html', context)


@login_required
def wishlist_add(request, product_id):
    """Add product to wishlist."""
    product = get_object_or_404(Product, id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)

    messages.success(request, f'{product.name} added to wishlist.')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))


@login_required
def wishlist_remove(request, product_id):
    """Remove product from wishlist."""
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)
        wishlist.products.remove(product)
        messages.success(request, f'{product.name} removed from wishlist.')
    except (Wishlist.DoesNotExist, Product.DoesNotExist):
        pass

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect(request.META.get('HTTP_REFERER', 'store:wishlist_detail'))


@login_required
def add_review(request, slug):
    """Add review to product."""
    product = get_object_or_404(Product, slug=slug)

    # Check if user already reviewed
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, 'You have already reviewed this product.')
        return redirect('store:product_detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted and is pending approval.')
            return redirect('store:product_detail', slug=slug)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'store/add_review.html', context)


@login_required
def account_dashboard(request):
    """User account dashboard."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]

    try:
        wishlist_count = request.user.wishlist.products.count()
    except Wishlist.DoesNotExist:
        wishlist_count = 0

    context = {
        'orders': orders,
        'wishlist_count': wishlist_count,
    }
    return render(request, 'store/account_dashboard.html', context)


def contact(request):
    """Contact page."""
    context = {}
    return render(request, 'store/contact.html', context)