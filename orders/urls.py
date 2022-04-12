from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/new', views.OrderCreateView.as_view(), name='orders-new'),
    path('orders/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order-delete'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product'),
    path('orders/<int:pk>/update', views.OrderUpdateView.as_view(), name='order-update'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
