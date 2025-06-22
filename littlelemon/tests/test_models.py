from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from restaurant.models import Menu, Booking


# Model Tests
class MenuModelTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(name="Ice Cream", price=80, menu_item_description="Delicious ice cream")
        self.assertEqual(str(item), "Ice Cream")


# API Tests
class MenuAPITest(APITestCase):
    def setUp(self):
        # Create a user and token for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        
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

    def test_get_menu_items_unauthenticated(self):
        """Test that unauthenticated users cannot access menu items"""
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_menu_items_authenticated(self):
        """Test that authenticated users can get menu items"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_menu_item(self):
        """Test creating a new menu item"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'name': 'New Test Item',
            'price': 9.99,
            'menu_item_description': 'A new test menu item'
        }
        response = self.client.post('/api/menu-items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)

    def test_get_single_menu_item(self):
        """Test retrieving a single menu item"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(f'/api/menu-items/{self.menu_item1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Pizza')

    def test_update_menu_item(self):
        """Test updating a menu item"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'name': 'Updated Pizza',
            'price': 18.99,
            'menu_item_description': 'Updated delicious pizza'
        }
        response = self.client.put(f'/api/menu-items/{self.menu_item1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item1.refresh_from_db()
        self.assertEqual(self.menu_item1.name, 'Updated Pizza')

    def test_delete_menu_item(self):
        """Test deleting a menu item"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(f'/api/menu-items/{self.menu_item1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 1)

