from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as lang

from slib.utils.framework import *
from slib.utils.observer import Observer
from slib.models.item_status import ItemStatus, ItemAvailable, ItemCheckedOut, ItemPendingReturn, ItemUnavailable

class Holding(models.Model):
	"""Holding in the Slib network. E.g., a book title."""
	
	# Class information.
	
	class Meta:
		app_label = 'slib'
		
	def __str__(self): return self.name
	
	# Field information.
	
	code = models.SlugField(unique = True)
	name = models.CharField(max_length = MAX_LENGTH)
	item_max = models.SmallIntegerField(default = 0, editable = False)

class Item(models.Model, Observer):
	"""Physical instances of a single holding in the Slib network that can be borrowed. E.g., physical copies of a single book."""

	# Class information.
	
	class Meta:
		app_label = 'slib'
	
	def __str__(self): return self.code
	
	def clean(self):
		if self.owner == self.borrower:
			raise ValidationError(self.ERR_OWNER_IS_BORROWER)
	
	def save(self, *args, **kwargs):
		if self.number == 0:
			self.holding.item_max += 1
			self.holding.save()
			self.number = self.holding.item_max
			self.code = self.holding.code + "-" + str(self.number)
		super(Item, self).save(*args, **kwargs)

	# Field information.
	
	holding = models.ForeignKey(Holding, on_delete = models.CASCADE)
	number = models.SmallIntegerField(default = 0, editable = False)
	code = models.SlugField(editable = False)
	
	ERR_OWNER_IS_BORROWER = lang("The borrower cannot be the same person as the owner.")
	owner = models.ForeignKey(User, related_name = 'owned_items')
	borrower = models.ForeignKey(User, related_name = 'borrowed_items', null = True, blank = True)
	
	due_date = models.DateField(editable = False, null = True, blank = True)
	days_past_due = models.SmallIntegerField(editable = False, null = True, blank = True)
	
	# Item status and status-dependent methods.
	
	ITEM_AVAILABLE = ItemAvailable()
	ITEM_CHECKED_OUT = ItemCheckedOut()
	ITEM_PENDING_RETURN = ItemPendingReturn()
	ITEM_UNAVAILABLE = ItemUnavailable()
	
	STATUS_CHOICES = (
		(ITEM_AVAILABLE.name(), ITEM_AVAILABLE.number()),
		(ITEM_CHECKED_OUT.name(), ITEM_CHECKED_OUT.number()),
		(ITEM_PENDING_RETURN.name(), ITEM_PENDING_RETURN.number()),
		(ITEM_UNAVAILABLE.name(), ITEM_UNAVAILABLE.number()),
	)
	
	status = models.SmallIntegerField(choices = STATUS_CHOICES, default = ITEM_AVAILABLE.number(), editable = False)
	
	ERR_CANNOT_CHECK_IN = lang("This item is available and cannot be checked in.")
	ERR_CANNOT_CHECK_OUT = lang("This item is on loan and cannot be checked out.")
	
	def check_in(self): self.status.check_in(self)
	def check_out(self, date = None): self.status.check_out(self, date)
	def update(self): self.status.update(self)