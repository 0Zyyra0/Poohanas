# Poohanas - Premium Graphics Card E-Commerce

A production-minded graphics card e-commerce website built with Django, HTML5, CSS3, and vanilla JavaScript. Features premium Apple-inspired design, Three.js 3D visualization, and complete e-commerce functionality.

## Features

- **Product Catalog**: Browse NVIDIA and AMD graphics cards with advanced filtering (brand, VRAM, price, memory type)
- **Shopping Cart**: Add/remove items, quantity updates, real-time subtotal calculations
- **Checkout Flow**: Complete checkout with shipping address, order confirmation (demo mode)
- **User Accounts**: Registration, login, order history, wishlist, profile management
- **Product Reviews**: Rating and review system with moderation
- **3D Visualization**: Three.js powered product viewing on hero section
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Admin Panel**: Full Django admin for product and order management

## Tech Stack

- **Backend**: Django 5.x (Python 3.12+)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **3D Graphics**: Three.js
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Design**: Apple-inspired, neutral palette

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Step 1: Clone and Navigate

```bash
cd Poohanas
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment

Copy `.env.example` to `.env` and update settings:

```bash
copy .env.example .env
```

Edit `.env` with your settings:
- `SECRET_KEY`: Generate a secure secret key
- `DEBUG`: Set to False for production
- `ALLOWED_HOSTS`: Your domain/hostnames

### Step 6: Run Migrations

```bash
python manage.py migrate
```

### Step 7: Load Sample Data

```bash
python manage.py loaddata sample_data.json
```

Or create a superuser and add products manually:

```bash
python manage.py createsuperuser
```

### Step 8: Run Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the site.

## Project Structure

```
Poohanas/
├── poohanas/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                 # Main e-commerce app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── forms.py           # Forms
│   ├── admin.py           # Admin configuration
│   └── context_processors.py
├── templates/
│   ├── base.html          # Base template
│   ├── store/             # Store templates
│   └── registration/      # Auth templates
├── static/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript
│   └── images/            # Static images
├── media/                 # User uploads
├── requirements.txt
└── manage.py
```

## Usage

### Adding Products (via Admin)

1. Start the server: `python manage.py runserver`
2. Go to `http://127.0.0.1:8000/admin/`
3. Login with your superuser credentials
4. Add categories, brands, and products

### Demo Checkout

The checkout is in demo mode - no real payment is processed. To test:
1. Add products to cart
2. Proceed to checkout
3. Enter shipping address
4. Complete order (marked as demo)

## Customization

### Adding More Product Images

Product images are stored in `media/products/`. Add images via Django admin.

### Changing Colors/Styles

Edit CSS variables in `static/css/main.css`:

```css
:root {
    --color-charcoal: #1d1d1f;
    --color-silver: #86868b;
    /* Add your custom colors */
}
```

### Adding Payment Gateway

In `store/views.py`, modify the `checkout_process` view to integrate with Stripe, PayPal, or another payment provider.

## Testing

Run the test suite:

```bash
python manage.py test store
```

## Deployment

### For Production

1. Set `DEBUG=False` in `.env`
2. Use PostgreSQL instead of SQLite
3. Configure static file serving (Whitenoise or CDN)
4. Set up HTTPS/SSL
5. Use environment variables for secrets

Example deployment with Gunicorn:

```bash
pip install gunicorn
gunicorn poohanas.wsgi:application --bind 0.0.0.0:8000
```

## License

MIT License - See LICENSE file for details.

## Credits

- Design inspired by Apple
- 3D visualization with Three.js
- Built with Django

## Support

For issues or questions, contact support@poohanas.com