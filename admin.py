from django.contrib import admin
from .models import Holding, Item

# Register your models here.

admin.site.register(Holding)
admin.site.register(Item)