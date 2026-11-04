"""Context processors for the Store app."""
from .models import Cart, Wishlist, Category, Brand


def cart_item_count(request):
    """Add cart item count to context."""
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.items.count()
        except Cart.DoesNotExist:
            pass

    return {'cart_item_count': count}


def wishlist_count(request):
    """Add wishlist count to context."""
    count = 0
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            count = wishlist.products.count()
        except Wishlist.DoesNotExist:
            pass

    return {'wishlist_count': count}


def navigation_context(request):
    """Add navigation categories and brands to context."""
    categories = Category.objects.filter(parent__isnull=True)[:8]
    brands = Brand.objects.all()[:6]

    return {
        'nav_categories': categories,
        'nav_brands': brands,
    }