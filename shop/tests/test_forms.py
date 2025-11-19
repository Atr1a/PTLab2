from django.test import TestCase
from shop.forms import RegistrationForm, PurchaseForm
from datetime import date


class FormsTest(TestCase):

    def test_registration_form_valid_email(self):

        data = {
            "username": "newuser",
            "email": "myname@mail.co",
            "password": "12345678",
            "birthday": "2000-05-05",
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid(), f"Форма должна быть валидной: {form.errors}")

        user = form.save()
        self.assertEqual(user.email, "myname@mail.co")
        self.assertEqual(user.profile.birthday.strftime("%Y-%m-%d"), "2000-05-05")

    def test_registration_invalid_email(self):

        data = {
            "username": "user",
            "email": "not-an-email",
            "password": "123",
            "birthday": "2000-01-01",
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_registration_birthday_today_discount(self):

        today = date.today().strftime("%Y-%m-%d")
        data = {
            "username": "birthdayboy",
            "email": "birthday@mail.com",
            "password": "pass1234",
            "birthday": today,
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid(), f"Форма должна быть валидной: {form.errors}")
        user = form.save()

        self.assertEqual(
            user.profile.birthday.strftime("%Y-%m-%d"),
            today
        )

    def test_purchase_form_requires_address(self):

        form = PurchaseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("address", form.errors)

    def test_purchase_form_valid_address(self):

        data = {"address": "123 Main Street"}
        form = PurchaseForm(data=data)
        self.assertTrue(form.is_valid())
        purchase = form.save(commit=False)
        self.assertEqual(purchase.address, "123 Main Street")
