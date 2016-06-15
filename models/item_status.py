import abc
from datetime import date

from django.core.exceptions import ValidationError

class ItemStatus(object, metaclass = abc.ABCMeta):
	
	@abc.abstractmethod
	def name(self): raise NotImplementedError
	
	@abc.abstractmethod
	def number(self): raise NotImplementedError
	
	@abc.abstractmethod
	def check_in(self): raise NotImplementedError
		
	@abc.abstractmethod
	def check_out(self): raise NotImplementedError
	
	@abc.abstractmethod
	def update(self): raise NotImplementedError
	
class ItemAvailable(ItemStatus):
	
	def name(self): return "Available"
	
	def number(self): return 0
	
	def check_in(self, item):
		raise ValidationError(item.ERR_CANNOT_CHECK_IN)
		
	def check_out(self, item, date):
		item.status = item.ITEM_CHECKED_OUT
		item.due_date = date
		print("Item was checked out.")
		
	def update(self, item): pass
		
class ItemCheckedOut(ItemStatus):
	
	def name(self): return "Checked Out"
	
	def number(self): return 1
	
	def check_in(self, item):
		item.status = item.ITEM_AVAILABLE
		item.due_date = None
		item.days_past_due = None
		print("Item was checked in.")
		
	def check_out(self, item, date):
		raise ValidationError(item.ERR_CANNOT_CHECK_OUT)
		
	def update(self, item):
		if item.due_date is not None:
			item.days_past_due = max((date.today() - item.due_date).days, 0)
			
class ItemPendingReturn(ItemStatus):

	def name(self): "Pending Return"
	
	def number(self): return 2
	
	def check_in(self, item): pass
	
	def check_out(self, item, date): pass
	
	def update(self, item): pass
	
class ItemUnavailable(ItemStatus):

	def name(self): "Unavailable"
	
	def number(self): return 3
	
	def check_in(self, item): pass
	
	def check_out(self, item, date): pass
	
	def update(self, item): pass