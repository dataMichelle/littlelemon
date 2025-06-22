# Little Lemon Web Application - Back-end Developer Capstone Project

A full-stack web application for Little Lemon restaurant built with Django REST Framework, featuring menu management, table bookings, and user authentication.

## Features

- **Menu Management**: View and manage restaurant menu items
- **Table Booking System**: Book and manage restaurant reservations
- **User Authentication**: User registration, login, and token-based authentication
- **RESTful API**: Full CRUD operations for menu items and bookings
- **Admin Interface**: Django admin panel for management
- **Unit Tests**: Comprehensive test coverage for models, views, and API endpoints

## Technology Stack

- **Backend**: Django 4.x, Django REST Framework
- **Database**: MySQL
- **Authentication**: Token-based authentication with Djoser
- **Testing**: Django TestCase and APITestCase
- **Version Control**: Git

## Installation and Setup

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd littlelemon
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL Database**
   - Create a MySQL database named `reservations`
   - Update database settings in `littlelemon/settings.py`

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

- `POST /auth/users/` - User registration
- `POST /auth/token/login/` - User login (get token)
- `POST /auth/token/logout/` - User logout
- `POST /api-token-auth/` - Alternative token authentication

### Menu API Endpoints

- `GET /api/menu-items/` - List all menu items (requires authentication)
- `POST /api/menu-items/` - Create new menu item (requires authentication)
- `GET /api/menu-items/{id}/` - Get specific menu item (requires authentication)
- `PUT /api/menu-items/{id}/` - Update menu item (requires authentication)
- `DELETE /api/menu-items/{id}/` - Delete menu item (requires authentication)

### Booking API Endpoints

- `GET /api/bookings/` - List all bookings (requires authentication)
- `POST /api/bookings/` - Create new booking (requires authentication)
- `GET /api/bookings/{id}/` - Get specific booking (requires authentication)
- `PUT /api/bookings/{id}/` - Update booking (requires authentication)
- `DELETE /api/bookings/{id}/` - Delete booking (requires authentication)

### User Management

- `GET /api/users/` - List users (requires authentication)
- `POST /api/users/` - Create user (requires authentication)

### Test Endpoint

- `GET /api/message/` - Protected test endpoint (requires authentication)

## API Testing with Insomnia/Postman

### 1. User Registration
```http
POST http://127.0.0.1:8000/auth/users/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123"
}
```

### 2. Get Authentication Token
```http
POST http://127.0.0.1:8000/auth/token/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "testpass123"
}
```

### 3. List Menu Items (with authentication)
```http
GET http://127.0.0.1:8000/api/menu-items/
Authorization: Token <your-token-here>
```

### 4. Create Menu Item
```http
POST http://127.0.0.1:8000/api/menu-items/
Authorization: Token <your-token-here>
Content-Type: application/json

{
  "name": "Margherita Pizza",
  "price": 12.99,
  "menu_item_description": "Classic pizza with tomato sauce and mozzarella"
}
```

### 5. Create Booking
```http
POST http://127.0.0.1:8000/api/bookings/
Authorization: Token <your-token-here>
Content-Type: application/json

{
  "name": "John Doe",
  "no_of_guests": 4,
  "booking_date": "2024-12-25",
  "booking_slots": "19:00"
}
```

## Database Models

### Menu Model
- `name`: CharField (max_length=200)
- `price`: DecimalField (max_digits=10, decimal_places=2)
- `menu_item_description`: TextField

### Booking Model
- `name`: CharField (max_length=200)
- `no_of_guests`: IntegerField
- `booking_date`: DateField
- `booking_slots`: CharField (max_length=100)

## Testing

The application includes comprehensive unit tests covering:

- Model functionality and validation
- API endpoints and authentication
- View logic and form processing
- Error handling and edge cases

### Run Tests
```bash
# Run all tests
python manage.py test

# Run specific test modules
python manage.py test littlelemon.tests.test_models
python manage.py test littlelemon.tests.test_views

# Run with verbose output
python manage.py test -v 2
```

## Static Files and Templates

The application serves static HTML content using Django's template system:

- Homepage (`/`)
- About page (`/about/`)
- Menu page (`/menu/`)
- Booking page (`/book/`)
- Admin interface (`/admin/`)

## Project Structure

```
littlelemon/
├── littlelemon/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── tests/
│       ├── test_models.py
│       └── test_views.py
├── LittleLemonAPI/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── restaurant/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│   └── static/
├── manage.py
└── requirements.txt
```

## Key Features for Peer Review

✅ **Django Static HTML**: Application serves static HTML content through Django templates

✅ **Git Repository**: Project is committed to Git with proper version control

✅ **MySQL Database**: Backend connected to MySQL database with proper models

✅ **Menu API**: Full CRUD operations for menu items implemented

✅ **Booking API**: Complete table booking system with API endpoints

✅ **User Authentication**: User registration and token-based authentication system

✅ **Unit Tests**: Comprehensive test coverage for models, views, and API endpoints

✅ **Insomnia/Postman Ready**: API endpoints documented and ready for testing

## Author

Meta Back-end Developer Capstone Project

## License

This project is part of the Meta Back-end Developer Certificate program.
