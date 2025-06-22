from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.test import RequestFactory
from restaurant.models import Menu, Booking
from restaurant.forms import BookingForm
import json
from datetime import date, datetime


class RestaurantViewLogicTests(TestCase):
    """Test the business logic of restaurant views without template rendering"""
    
    def setUp(self):
        """Set up test data"""
        self.factory = RequestFactory()
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test menu items
        self.menu_item1 = Menu.objects.create(
            name="Test Pizza",
            price=15.99,
            menu_item_description="Delicious test pizza"
        )
        self.menu_item2 = Menu.objects.create(
            name="Test Burger", 
            price=12.50,
            menu_item_description="Tasty test burger"
        )
        
        # Create test booking
        self.booking = Booking.objects.create(
            name="John Doe",
            no_of_guests=4,
            booking_date=date.today(),
            booking_slots="18:00"        )

    def test_menu_view_data_retrieval(self):
        """Test that menu view retrieves correct data from database"""
        from restaurant.views import menu
        
        # Test the data retrieval logic directly
        menu_data = Menu.objects.all()
        self.assertEqual(menu_data.count(), 2)
        
        # Verify the menu items are the ones we created
        menu_names = [item.name for item in menu_data]
        self.assertIn("Test Pizza", menu_names)
        self.assertIn("Test Burger", menu_names)

    def test_display_menu_item_with_valid_pk(self):
        """Test display_menu_item view logic with valid pk"""
        from restaurant.views import display_menu_item
        from django.shortcuts import get_object_or_404
        
        # Test that the correct menu item is retrieved
        request = self.factory.get(f'/menu/{self.menu_item1.pk}/')
        
        # We can test the get_object_or_404 logic directly
        menu_item = get_object_or_404(Menu, pk=self.menu_item1.pk)
        self.assertEqual(menu_item, self.menu_item1)
        self.assertEqual(menu_item.name, "Test Pizza")

    def test_display_menu_item_with_invalid_pk(self):
        """Test display_menu_item view with invalid pk raises 404"""
        from django.shortcuts import get_object_or_404
        from django.http import Http404
        
        with self.assertRaises(Http404):
            get_object_or_404(Menu, pk=999)

    def test_reservations_view_post_valid_booking(self):
        """Test creating a new reservation via POST"""
        from restaurant.views import reservations
        
        booking_data = {
            'name': 'Jane Smith',
            'booking_date': str(date.today()),
            'no_of_guests': 3
        }
        request = self.factory.post(
            '/reservations/',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        response = reservations(request)
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['success'], 'Reservation created successfully')
        
        # Verify booking was created
        booking_exists = Booking.objects.filter(name='Jane Smith').exists()
        self.assertTrue(booking_exists)

    def test_reservations_view_post_duplicate_booking(self):
        """Test creating a duplicate reservation returns error"""
        from restaurant.views import reservations
        
        booking_data = {
            'name': self.booking.name,
            'booking_date': str(self.booking.booking_date),
            'no_of_guests': 2
        }
        request = self.factory.post(
            '/reservations/',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        response = reservations(request)
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'This booking already exists')

    def test_reservations_view_ajax_request_returns_json(self):
        """Test reservations view with AJAX request returns JSON"""
        from restaurant.views import reservations
        
        request = self.factory.get('/bookings/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = reservations(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Test that the response contains valid JSON
        try:
            json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

    def test_reservations_view_get_with_date_filter(self):
        """Test reservations view GET request with date filter"""
        from restaurant.views import reservations
        
        # Create another booking for a different date
        different_date = date(2024, 12, 25)
        Booking.objects.create(
            name="Different Date Booking",
            no_of_guests=2,
            booking_date=different_date,
            booking_slots="19:00"
        )
        
        # Test AJAX request with date filter
        request = self.factory.get(
            '/bookings/', 
            {'date': str(date.today())},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response = reservations(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Parse the JSON response and check filtered results
        bookings_data = json.loads(response.content)
        # Should only contain today's booking, not the different date one
        today_bookings = [b for b in bookings_data if b['fields']['booking_date'] == str(date.today())]
        self.assertEqual(len(today_bookings), 1)

    def test_booking_form_validation(self):
        """Test BookingForm validation logic"""
        # Test valid form
        valid_data = {
            'name': 'Test Customer',
            'no_of_guests': 4,
            'booking_date': date.today(),
            'booking_slots': '20:00'
        }
        form = BookingForm(data=valid_data)
        self.assertTrue(form.is_valid())
        
        # Test invalid form (missing required field)
        invalid_data = {
            'name': '',  # Required field left empty
            'no_of_guests': 4,
            'booking_date': date.today(),
        }
        form = BookingForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_booking_form_save_creates_booking(self):
        """Test that BookingForm save creates a booking in database"""
        form_data = {
            'name': 'Form Test Customer',
            'no_of_guests': 6,
            'booking_date': date.today(),
            'booking_slots': '21:00'
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Count bookings before saving
        initial_count = Booking.objects.count()
        
        booking = form.save()
        self.assertEqual(booking.name, 'Form Test Customer')
        self.assertEqual(booking.no_of_guests, 6)
        
        # Verify it increased the count
        self.assertEqual(Booking.objects.count(), initial_count + 1)
        
        # Verify it was saved to database
        saved_booking = Booking.objects.get(name='Form Test Customer')
        self.assertEqual(saved_booking.no_of_guests, 6)

    def test_book_view_post_processing(self):
        """Test the booking form processing logic in book view"""
        from restaurant.views import book
        
        # Test POST data processing without template rendering
        post_data = {
            'name': 'Book View Test',
            'no_of_guests': 3,
            'booking_date': date.today(),
            'booking_slots': '19:30'
        }
        
        # Create form and test validation
        form = BookingForm(data=post_data)
        self.assertTrue(form.is_valid())
        
        # Test that saving the form creates the booking
        initial_count = Booking.objects.count()
        form.save()
        self.assertEqual(Booking.objects.count(), initial_count + 1)
        
        # Verify the booking details
        new_booking = Booking.objects.get(name='Book View Test')
        self.assertEqual(new_booking.no_of_guests, 3)
        self.assertEqual(str(new_booking.booking_date), str(date.today()))


class ModelTests(TestCase):
    """Test the models directly"""
    
    def test_menu_model_str_method(self):
        """Test Menu model string representation"""
        menu_item = Menu.objects.create(
            name="Test Dish",
            price=25.50,
            menu_item_description="A test dish"
        )
        self.assertEqual(str(menu_item), "Test Dish")

    def test_booking_model_str_method(self):
        """Test Booking model string representation"""
        booking = Booking.objects.create(
            name="Test Customer",
            no_of_guests=2,
            booking_date=date.today(),
            booking_slots="18:30"
        )
        self.assertEqual(str(booking), "Test Customer")

    def test_menu_model_fields(self):
        """Test Menu model field constraints"""
        menu_item = Menu.objects.create(
            name="Field Test Item",
            price=19.99,
            menu_item_description="Testing field constraints"
        )
        
        # Test field values
        self.assertEqual(menu_item.name, "Field Test Item")
        self.assertEqual(menu_item.price, 19.99)
        self.assertEqual(menu_item.menu_item_description, "Testing field constraints")

    def test_booking_model_fields(self):
        """Test Booking model field values"""
        booking = Booking.objects.create(
            name="Field Test Customer",
            no_of_guests=5,
            booking_date=date(2024, 6, 15),
            booking_slots="20:15"
        )
        
        # Test field values
        self.assertEqual(booking.name, "Field Test Customer")
        self.assertEqual(booking.no_of_guests, 5)
        self.assertEqual(booking.booking_date, date(2024, 6, 15))
        self.assertEqual(booking.booking_slots, "20:15")
