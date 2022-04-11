from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import (
                                ListView,
                                DetailView,
                                DeleteView,
                                CreateView,
                                UpdateView,
                                )

from orders.models import Order, User, Product


def index(request):
    all_orders = Order.objects.all()
    context = {
      'all_orders': all_orders,
    }
    return render(request, 'index.html', context=context)

class OrderListView(ListView):
    model = Order
    paginate_by = 5
    template_name = 'order_list.html'

class UserListView(ListView):
    model = User
    paginate_by = 5
    template_name = 'user_list.html'

class UserDetailView(DetailView):
    model = User
    paginate_by = 5
    template_name = 'user_detail.html'

class ProductListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'product_list.html'

class ProductDetailView(DetailView):
    model = Product
    paginate_by = 10
    template_name = 'product_detail.html'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
