from django.contrib import admin
from .models import Profile, Order, ProductOrder, Product

# Register your models here.

class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'status')
    inlines = [ProductOrderInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'quantity', 'selection')

admin.site.register(Profile)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(Product, ProductAdmin)