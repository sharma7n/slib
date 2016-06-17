from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from slib.models.holding import Holding, Item

class HoldingList(ListView):
    model = Holding
	
class HoldingDetail(DetailView):
    model = Holding
	
class ItemList(ListView):
    model = Item
	
class ItemDetail(DetailView):
    model = Item
    
def index(request):
    return render(request, 'slib/index.html')
