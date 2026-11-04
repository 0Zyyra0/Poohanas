"""Forms for the Store app."""
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Review, ShippingAddress


class SearchForm(forms.Form):
    """Product search form."""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search graphics cards...',
            'class': 'search-input',
            'aria-label': 'Search products'
        })
    )


class FilterForm(forms.Form):
    """Product filtering form."""
    brand = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    max_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    vram = forms.CharField(required=False)
    gpu_series = forms.CharField(required=False)
    memory_type = forms.CharField(required=False)
    in_stock = forms.BooleanField(required=False)


class AddToCartForm(forms.Form):
    """Add product to cart form."""
    quantity = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'quantity-input',
            'min': '1',
            'max': '10',
            'aria-label': 'Quantity'
        })
    )


class CartItemUpdateForm(forms.Form):
    """Update cart item quantity form."""
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'quantity-input',
            'min': '1',
            'max': '10'
        })
    )


class ShippingAddressForm(forms.ModelForm):
    """Shipping address form for checkout."""
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'phone', 'address_line1',
                  'address_line2', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'address_line1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Street address', 'required': True}),
            'address_line2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Apartment, suite, etc. (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
        }


class ReviewForm(forms.ModelForm):
    """Product review form."""
    rating = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'rating-input'}),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Review title',
                'required': True
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Share your experience with this product...',
                'rows': 4,
                'required': True
            }),
        }


class CheckoutForm(forms.Form):
    """Checkout confirmation form."""
    shipping_address_id = forms.IntegerField(widget=forms.HiddenInput())
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Order notes (optional)',
            'rows': 3
        })
    )