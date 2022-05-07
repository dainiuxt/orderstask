from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.views.generic import (
                                ListView,
                                DetailView,
                                DeleteView,
                                CreateView,
                                UpdateView,
                                )
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order, User, Product, ProductOrder
from .forms import OrderForm, RowFormUpdate, UserUpdateForm, RowForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt

# @csrf_exempt
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

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('date')


class OrderCreateView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Order
    form_class = OrderForm
    template_name = 'order_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

class OrderUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Order
    form_class = OrderForm
    template_name = 'order_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = 'my_order_delete.html'

    def get_success_url(self):
        return reverse('orders')

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user

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

class OrderDetailView(DetailView, FormMixin):
    model = Order
    template_name = 'order_detail.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})



@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid():
            u_form.save()
            # p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        # 'p_form': p_form,
    }    
    return render(request, 'profile.html', context)


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = ProductOrder
    form_class = RowForm
    # success_url = "orders/"
    template_name = 'position_new.html'

    def get_success_url(order):
        return reverse('orders')

    def form_valid(self, form):
        # form.instance.orderrow = self.request.orderrow
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        order = self.object
        context = super().get_context_data(**kwargs)
        context['form'].fields['order'].queryset = Order.objects.filter(user=self.request.user)
        return context


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductOrder
    form_class = RowFormUpdate
    template_name = 'position_update.html'

    def get_success_url(order):
        return reverse('orders')

    def form_valid(self, form):
        # form.instance.orderrow = self.request.orderrow
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        order = self.object
        context = super().get_context_data(**kwargs)
        return context
