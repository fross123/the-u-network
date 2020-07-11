from django.test import TestCase
from django.contrib.auth import authenticate

from .models import User

# Create your tests here.
class NetworkTestCase(TestCase):
    def setUp(self):
        # Create Users
        u1 = User.objects.create_user("AAA", "AAA@test.com", "AAA")
        u2 = User.objects.create_user("BBB", "BBB@test.com", "BBB")

    def testAuthentication(self):
        """Test if User can be authenticated"""
        user1 = authenticate(self, username="AAA", password="AAA")
        user2 = authenticate(self, username="BBB", password="BBB")
        self.assertTrue(user1.is_authenticated and user2.is_authenticated)

    def testAuthenticationFalse(self):
        """Test if user is Denied"""
        user2 = authenticate(self, username="BBB", password="ABCD")
        self.assertEqual(user2, None)
