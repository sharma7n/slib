from datetime import date, timedelta
from unittest import mock

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from slib.models import Holding, Item
from slib.utils.framework import MockDate

class HoldingTestCase(TestCase):
	
	def setUp(cls):
		cls.holding = Holding.objects.create(code = "Holding", name = "New Holding")
		cls.user = User.objects.create_user(username = "test", email = "", password = "123")
	
	def test_holding(self):
		"""Holding DDTT."""
		item1 = Item.objects.create(holding = self.holding, owner = self.user)
		item2 = Item.objects.create(holding = self.holding, owner = self.user)
		self.assertEqual(self.holding.item_max, 2)
		self.holding.full_clean()
		
class ItemTestCase(TestCase):

	def setUp(cls):
		cls.holding1 = Holding.objects.create(code = "Holding1", name = "New Holding 1")
		cls.holding2 = Holding.objects.create(code = "Holding2", name = "New Holding 2")
		
		cls.user1 = User.objects.create_user(username = "test1", email = "", password = "123")
		cls.user2 = User.objects.create_user(username = "test2", email = "", password = "123")
		
		cls.item1_1 = Item.objects.create(holding = cls.holding1, owner = cls.user1)
		cls.item1_2 = Item.objects.create(holding = cls.holding1, owner = cls.user1, borrower = cls.user2)
		cls.item2_1 = Item.objects.create(holding = cls.holding2, owner = cls.user2)
		
	@mock.patch("slib.models.item_status.date", MockDate)
	def test_item(self):
		"""Item DDTT, including number and days past due calculations."""
		item1_2_a = Item.objects.get(number = 2)
		item1_2_b = Item.objects.get(borrower = self.user2)
		self.assertEqual(item1_2_a, item1_2_b)
		
		i = self.item2_1
		i.owner = self.user1
		i.check_out(date(2000, 1, 1))
		i.save()
		
		self.assertEqual(i.number, 1)
		
		MockDate.today = classmethod(lambda cls: date(2000, 1, 11))
		i.update()
		self.assertEqual(i.days_past_due, 10)
		
		i.check_in()
		i.check_out(None)
		self.assertEqual(i.days_past_due, None)
		
		items = Item.objects.all()
		for item in items:
			item.full_clean()
		
	def test_owner_is_not_borrower(self):
		"""Owner and Borrower cannot be the same user."""
		with self.assertRaises(ValidationError):
			item1_3 = Item.objects.create(holding = self.holding1, owner = self.user1, borrower = self.user1)
			item1_3.clean()
		
	def test_check_in(self):
		"""Item can be checked in only once."""
		self.item1_1.check_out(None)
		self.item1_1.check_in()
		with self.assertRaises(ValidationError):
			self.item1_1.check_in()
			
	def test_check_out(self):
		"""Item can be checked out only once."""
		self.item1_1.check_out(None)
		with self.assertRaises(ValidationError):
			self.item1_1.check_out(None)