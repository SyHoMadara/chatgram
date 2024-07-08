from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from users.models import User


class UsersTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="testPassword1234",
            first_name="test",
            last_name="test",
        )

    def test_user_duplicate_creation(self):
        with self.assertRaises(IntegrityError):
            user = User.objects.create_user(
                email="test@test.com",
                password="testPassword1234",
                first_name="test",
                last_name="test",
            )

    def test_user_update(self):
        new_email = "newtest@test.com"
        new_password = "newPassword1234544"
        new_name = "newtest"

        with self.subTest("Update email"):
            self.user.set_email(new_email)
            self.user.save()
            self.assertEqual(self.user.email, new_email)

        with self.subTest("Update password"):
            self.user.set_password(new_password)
            self.user.save()
            self.assertTrue(self.user.check_password(new_password))

        with self.subTest("Update first name"):
            self.user.first_name = new_name
            self.user.save()
            self.assertEqual(self.user.first_name, new_name)

        with self.subTest("Update last name"):
            self.user.last_name = new_name
            self.user.save()
            self.assertEqual(self.user.last_name, new_name)

    def test_validate_password(self):
        with self.assertRaises(ValidationError):
            self.user.set_password("password")

    def test_change_email_integrity(self):
        User.objects.create_user("newuser@test.com", "testPassword1234")
        with self.assertRaises(IntegrityError):
            self.user.set_email("newuser@test.com")

    def test_soft_delete_user(self):
        self.user.delete()
        self.assertTrue(self.user.is_deleted)
        try:
            User.objects.get(email="test@test.com")
        except Exception:
            self.fail("User should not have been deleted")
        # Ensure the user can still be found when explicitly querying for deleted users
        deleted_user = User.objects.filter(is_deleted=True).first()
        self.assertIsNotNone(deleted_user)


def login(self):
    url = reverse("token_obtain_pair")
    data = {"email": "test@test.com", "password": "testPassword1234"}
    response = self.client.post(url, data, format="json")
    return response.data["access"], response.data["refresh"]


class UsersApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="testPassword1234",
            first_name="test",
            last_name="test"
        )
        cls.user2 = User.objects.create_user(
            email="test2@test.com",
            password="testPassword1234",
            first_name="test2",
            last_name="test2"
        )

    def test_user_registration(self):
        url = reverse("register")
        data = {
            "email": "newtest@test.com",
            "password": "newPassword1234",
            "first_name": "newtest",
            "last_name": "newtest"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 3)

    def test_get_profile(self):
        url = reverse("get-profile")
        access_token, _ = login(self)
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["last_name"], "test")

    def test_get_public_profile(self):
        url = reverse("get-public-profile")
        access_token, _ = login(self)
        data = {"email": "test2@test.com"}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["last_name"], "test2")

    def test_change_profile(self):
        url = reverse("change-profile")
        access_token, _ = login(self)
        data = {
            "email": "test3@test.com",
            "password": "testPassword12345",
            "first_name": "test3",
            "last_name": "test3",
            "is_deleted": True
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 2)
        updated_user = User.objects.get(email="test3@test.com")
        self.assertEqual(updated_user.first_name, "test3")
        self.assertEqual(updated_user.last_name, "test3")
        # These fields should not be updated
        self.assertFalse(updated_user.check_password("testPassword12345"))
        self.assertFalse(updated_user.is_deleted)

    def test_change_password(self):
        url = reverse("change-password")
        access_token, _ = login(self)
        data = {"password": "newPassword12345"}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(email="test@test.com").check_password("newPassword12345"))

    def test_log_out(self):
        url = reverse("logout")
        access_token, refresh_token = login(self)
        data = {"refresh-token": str(refresh_token)}
        response = self.client.post(url, data,HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)

        url = reverse("token_refresh")
        response = self.client.post(url, {"refresh": str(refresh_token)},HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 401)
