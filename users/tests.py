from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

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
        new_password = "newPassword1234"
        new_name = "newtest"

        with self.subTest("Update email"):
            self.user.email = new_email
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
            self.user.save()

    def test_change_email_integrity(self):
        User.objects.create_user("newuser@test.com", "testPassword1234")
        self.user.email = "newuser@test.com"
        with self.assertRaises(IntegrityError):
            self.user.save()

    def test_soft_delete_user(self):
        self.user.delete()
        self.assertTrue(self.user.is_deleted)
        try:
            User.objects.get(email="test@test.com")
        except Exception as e:
            self.fail("User should not have been deleted")
        # Ensure the user can still be found when explicitly querying for deleted users
        deleted_user = User.objects.filter(is_deleted=True).first()
        self.assertIsNotNone(deleted_user)
