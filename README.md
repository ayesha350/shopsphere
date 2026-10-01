# ShopSphere - E-Commerce REST API

ShopSphere is a backend E-Commerce REST API built using Django and Django REST Framework.

The project provides user authentication, role-based access, product management, shopping cart functionality, and order management.

## 🚀 Features

### Authentication
- Custom User model
- Email-based authentication
- Phone number support
- User registration
- JWT authentication
- Access and Refresh tokens

### User Roles
- Customer
- Seller

### Product Management
- Create products
- View products
- Update products
- Delete products
- Seller ownership validation
- Product search
- Category filtering
- Pagination

### Category Management
- Create categories
- View categories
- Category-based product filtering

### Shopping Cart
- Add products to cart
- View cart
- Update cart quantity
- Remove products from cart
- User-specific cart

### Order Management
- Place orders
- View user's orders
- View order details
- Cancel orders
- Order status management
- Order items
- Automatic total calculation
- Stock validation
- Automatic stock reduction after successful order

## 🛠️ Technologies Used

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite
- Thunder Client / Postman for API testing

## 📁 Project Structure

```text
ShopSphere/
│
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
