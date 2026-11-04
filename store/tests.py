"""
Tests for the Store app.
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import (
    Category, Brand, Product, Cart, CartItem, Order, OrderItem,
    ShippingAddress, Review, Wishlist
)


class ProductModelTest(TestCase):
    """Tests for the Product model."""

    def setUp(self):
        self.brand = Brand.objects.create(name='NVIDIA', slug='nvidia')
        self.category = Category.objects.create(name='Gaming', slug='gaming')

    def test_product_creation(self):
        """Test product is created with correct fields."""
        product = Product.objects.create(
            brand=self.brand,
            name='GeForce RTX 4090',
            slug='geforce-rtx-4090',
            category=self.category,
            description='Ultimate gaming GPU',
            price=Decimal('1599.00'),
            stock=10,
            vram=24,
            gpu_series='RTX 40 Series',
            memory_type='GDDR6X',
            interfaces='HDMI, DisplayPort',
            release_year=2024
        )
        self.assertEqual(str(product), 'NVIDIA GeForce RTX 4090')
        self.assertTrue(product.is_in_stock)
        self.assertTrue(product.is_available)

    def test_product_out_of_stock(self):
        """Test product out of stock behavior."""
        product = Product.objects.create(
            brand=self.brand,
            name='Test GPU',
            slug='test-gpu',
            category=self.category,
            description='Test',
            price=Decimal('500.00'),
            stock=0,
            vram=8,
            gpu_series='Test',
            memory_type='GDDR6',
            release_year=2024
        )
        self.assertFalse(product.is_in_stock)


class CartTest(TestCase):
    """Tests for shopping cart functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.brand = Brand.objects.create(name='NVIDIA', slug='nvidia')
        self.category = Category.objects.create(name='Gaming', slug='gaming')
        self.product = Product.objects.create(
            brand=self.brand,
            name='RTX 4090',
            slug='rtx-4090',
            category=self.category,
            description='Test',
            price=Decimal('1599.00'),
            stock=5,
            vram=24,
            gpu_series='RTX 40',
            memory_type='GDDR6X',
            release_year=2024
        )

    def test_cart_creation(self):
        """Test cart is created for user."""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(str(cart), 'Cart for testuser')

    def test_cart_item_subtotal(self):
        """Test cart item subtotal calculation."""
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(item.subtotal, Decimal('3198.00'))

    def test_cart_total(self):
        """Test cart total calculation."""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart.total, Decimal('3198.00'))


class OrderTest(TestCase):
    """Tests for order processing."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.brand = Brand.objects.create(name='NVIDIA', slug='nvidia')
        self.category = Category.objects.create(name='Gaming', slug='gaming')
        self.product = Product.objects.create(
            brand=self.brand,
            name='RTX 4090',
            slug='rtx-4090',
            category=self.category,
            description='Test',
            price=Decimal('1599.00'),
            stock=5,
            vram=24,
            gpu_series='RTX 40',
            memory_type='GDDR6X',
            release_year=2024
        )
        self.address = ShippingAddress.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone='1234567890',
            address_line1='123 Test St',
            city='Test City',
            state='TS',
            postal_code='12345'
        )

    def test_order_creation(self):
        """Test order is created correctly."""
        order = Order.objects.create(
            user=self.user,
            order_number='TEST-001',
            subtotal=Decimal('1599.00'),
            tax=Decimal('127.92'),
            shipping=Decimal('0.00'),
            total=Decimal('1726.92'),
            shipping_address=self.address
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name=self.product.name,
            product_price=self.product.price,
            quantity=1,
            subtotal=Decimal('1599.00')
        )
        self.assertEqual(order.item_count, 1)
        self.assertEqual(str(order), 'Order #TEST-001 by testuser')

    def test_stock_reduction(self):
        """Test stock is reduced after order."""
        initial_stock = self.product.stock
        order = Order.objects.create(
            user=self.user,
            order_number='TEST-002',
            subtotal=Decimal('1599.00'),
            tax=Decimal('127.92'),
            shipping=Decimal('0.00'),
            total=Decimal('1726.92'),
            shipping_address=self.address
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name=self.product.name,
            product_price=self.product.price,
            quantity=2,
            subtotal=Decimal('3198.00')
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock - 2)


class ReviewTest(TestCase):
    """Tests for product reviews."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.brand = Brand.objects.create(name='NVIDIA', slug='nvidia')
        self.category = Category.objects.create(name='Gaming', slug='gaming')
        self.product = Product.objects.create(
            brand=self.brand,
            name='RTX 4090',
            slug='rtx-4090',
            category=self.category,
            description='Test',
            price=Decimal('1599.00'),
            stock=5,
            vram=24,
            gpu_series='RTX 40',
            memory_type='GDDR6X',
            release_year=2024
        )

    def test_review_creation(self):
        """Test review is created."""
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title='Great GPU',
            comment='Excellent performance',
            is_approved=True
        )
        self.assertEqual(str(review), 'Review for RTX 4090 by testuser')

    def test_product_average_rating(self):
        """Test product average rating calculation."""
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            title='Great',
            comment='Test'
        )
        user2 = User.objects.create_user(username='user2', password='pass')
        Review.objects.create(
            product=self.product,
            user=user2,
            rating=4,
            title='Good',
            comment='Test'
        )
        self.assertEqual(self.product.average_rating, 4.5)


class WishlistTest(TestCase):
    """Tests for wishlist functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.brand = Brand.objects.create(name='NVIDIA', slug='nvidia')
        self.category = Category.objects.create(name='Gaming', slug='gaming')
        self.product = Product.objects.create(
            brand=self.brand,
            name='RTX 4090',
            slug='rtx-4090',
            category=self.category,
            description='Test',
            price=Decimal('1599.00'),
            stock=5,
            vram=24,
            gpu_series='RTX 40',
            memory_type='GDDR6X',
            release_year=2024
        )
        self.wishlist = Wishlist.objects.create(user=self.user)

    def test_add_to_wishlist(self):
        """Test adding product to wishlist."""
        self.wishlist.products.add(self.product)
        self.assertEqual(self.wishlist.products.count(), 1)

    def test_remove_from_wishlist(self):
        """Test removing product from wishlist."""
        self.wishlist.products.add(self.product)
        self.wishlist.products.remove(self.product)
        self.assertEqual(self.wishlist.products.count(), 0)


class ViewsTest(TestCase):
    """Tests for views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.brand = Brand.objects.create(name='NVIDIA', slug='nvidia')
        self.category = Category.objects.create(name='Gaming', slug='gaming')
        self.product = Product.objects.create(
            brand=self.brand,
            name='RTX 4090',
            slug='rtx-4090',
            category=self.category,
            description='Test GPU',
            price=Decimal('1599.00'),
            stock=5,
            vram=24,
            gpu_series='RTX 40',
            memory_type='GDDR6X',
            release_year=2024
        )

    def test_home_view(self):
        """Test home page loads."""
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_view(self):
        """Test product list page loads."""
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        """Test product detail page loads."""
        url = reverse('store:product_detail', args=['rtx-4090'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_required_for_cart(self):
        """Test cart requires login."""
        response = self.client.get(reverse('store:cart_detail'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)