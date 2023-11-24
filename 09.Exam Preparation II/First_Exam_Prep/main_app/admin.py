from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'is_active']
    search_fields = ['full_name', 'email']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'in_stock', 'is_available']
    list_filter = ['is_available']
    search_fields = ['name']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['profile', 'total_price', 'creation_date', 'is_completed']
    list_filter = ['is_completed']
    search_fields = ['profile__full_name']

