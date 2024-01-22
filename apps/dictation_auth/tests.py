from django.contrib.auth import get_user_model
from django.test import TestCase  # noqa


User = get_user_model()


class UsersManagersTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="basicuser@domain.com", password="secret")
        self.assertEqual(user.email, "basicuser@domain.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="secret")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("superuser@domain.com", "secret")
        self.assertEqual(admin_user.email, "superuser@domain.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="superuser@domain.com",
                password="secret",
                is_superuser=False,
            )
