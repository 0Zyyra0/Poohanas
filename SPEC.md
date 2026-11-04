# Poohanas - Premium Graphics Card E-Commerce Platform

## Project Overview

A production-minded graphics card e-commerce website built with Django, featuring premium Apple-inspired design, Three.js 3D product visualization, and complete e-commerce functionality.

## Technology Stack

- **Backend**: Python 3.12+, Django 5.x
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Three.js
- **Database**: SQLite (development), PostgreSQL-ready
- **Design**: Apple-inspired, neutral palette (black, white, charcoal, silver)

## Project Structure

```
Poohanas/
├── poohanas/              # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── store/                 # Main e-commerce app
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── components/
│   ├── store/
│   └── registration/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── 3d/
├── media/                 # User uploaded content
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Core Features

### 1. Product Management
- GPU catalog with brands (NVIDIA, AMD)
- Categories and subcategories
- Product images with multiple gallery support
- Specifications (VRAM, GPU series, memory type, etc.)
- Stock management
- Related products

### 2. User Experience
- Premium hero section with 3D elements
- Product catalog with search, filter, sort, pagination
- Product detail pages with specifications
- Shopping cart with real-time updates
- Wishlist functionality
- Product reviews and ratings

### 3. User Accounts
- Registration, login, logout
- Profile management
- Order history
- Address book

### 4. Checkout Flow
- Cart review
- Shipping information
- Order summary
- Demo checkout (no real payment processing)

### 5. Admin Panel
- Product management
- Order management
- User management
- Inventory tracking

## Database Models

### Product Models
- Category (name, slug, parent)
- Product (name, slug, brand, category, price, stock, description)
- ProductImage (product, image, alt_text, is_primary)
- ProductSpecification (product, key, value)

### User & Orders
- User (Django built-in)
- Profile (user, phone, addresses)
- Cart (user, created_at, updated_at)
- CartItem (cart, product, quantity)
- Order (user, status, total, shipping_address, created_at)
- OrderItem (order, product, quantity, price)
- Review (user, product, rating, comment, created_at)
- Wishlist (user, products)

## Design Tokens

```css
:root {
  /* Colors */
  --color-black: #000000;
  --color-white: #ffffff;
  --color-charcoal: #1d1d1f;
  --color-silver: #86868b;
  --color-gray-light: #f5f5f7;
  --color-gray-medium: #d2d2d7;
  
  /* Typography */
  --font-primary: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'SF Mono', Monaco, 'Courier New', monospace;
  
  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-medium: 300ms ease;
  --transition-slow: 500ms ease;
}
```

## Implementation Phases

### Phase 1: Project Setup
- Create Django project structure
- Configure settings, URLs
- Set up static files and media
- Create requirements.txt

### Phase 2: Models & Database
- Implement all models
- Create migrations
- Set up admin panel

### Phase 3: Frontend Foundation
- Base template with navigation
- CSS framework with design tokens
- Responsive layout
- Header and footer components

### Phase 4: Product Catalog
- Product listing views
- Product detail views
- Search and filtering
- Pagination

### Phase 5: Cart & Checkout
- Shopping cart functionality
- Checkout flow
- Order processing
- Order history

### Phase 6: User Features
- Authentication views
- Profile management
- Wishlist
- Reviews

### Phase 7: 3D Experience
- Three.js integration
- 3D product visualization
- Interactive controls

### Phase 8: Testing & Polish
- Unit tests
- Integration tests
- Performance optimization
- Accessibility review

### Phase 9: Deployment Preparation
- Environment configuration
- Security checklist
- Documentation
- GitHub push

## Security Considerations

- CSRF protection
- SQL injection prevention (Django ORM)
- XSS prevention (auto-escaping)
- Secure password hashing
- Environment variables for secrets
- No raw payment data storage
- Server-side validation

## Performance Optimization

- Lazy loading images
- Minified CSS/JS
- Database query optimization
- Caching strategies
- Reduced motion support
- Mobile-first responsive design

## Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast compliance
- Focus states
- Screen reader support
