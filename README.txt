Little Lemon Restaurant API - Peer Review Testing Guide

API BASE URL: http://127.0.0.1:8000

AUTHENTICATION REQUIRED FOR ALL API ENDPOINTS
===============================================

1. USER REGISTRATION & AUTHENTICATION:
   POST /auth/users/                    - Register new user
   POST /auth/token/login/              - Login and get token
   POST /api-token-auth/                - Alternative token auth

2. MENU API PATHS:
   GET  /api/menu-items/                - List all menu items
   POST /api/menu-items/                - Create new menu item
   GET  /api/menu-items/{id}/           - Get specific menu item
   PUT  /api/menu-items/{id}/           - Update menu item
   DELETE /api/menu-items/{id}/         - Delete menu item

3. BOOKING API PATHS:
   GET  /api/bookings/                  - List all bookings
   POST /api/bookings/                  - Create new booking
   GET  /api/bookings/{id}/             - Get specific booking
   PUT  /api/bookings/{id}/             - Update booking
   DELETE /api/bookings/{id}/           - Delete booking

4. USER MANAGEMENT:
   GET  /api/users/                     - List users
   POST /api/users/                     - Create user

5. TEST ENDPOINT:
   GET  /api/message/                   - Protected test endpoint

SETUP INSTRUCTIONS:
==================
1. Clone repository
2. Install dependencies: pip install -r requirements.txt
3. Setup MySQL database named 'reservations'
4. Run: python manage.py migrate
5. Run: python manage.py runserver
6. Test with Insomnia/Postman using the endpoints above

AUTHENTICATION:
==============
All API endpoints require authentication. Use Token authentication:
Header: Authorization: Token <your-token-here>

Get token by first registering a user, then logging in.

SAMPLE REQUESTS:
===============
Register: POST /auth/users/ with {"username":"test", "email":"test@test.com", "password":"testpass123"}
Login: POST /auth/token/login/ with {"username":"test", "password":"testpass123"}
Create Menu: POST /api/menu-items/ with {"name":"Pizza", "price":12.99, "menu_item_description":"Delicious pizza"}
Create Booking: POST /api/bookings/ with {"name":"John", "no_of_guests":4, "booking_date":"2024-12-25", "booking_slots":"19:00"}
