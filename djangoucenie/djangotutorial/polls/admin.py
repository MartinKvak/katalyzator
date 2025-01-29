from django.contrib import admin
from .models import Car, Rental

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'available', 'price_per_day', 'image_url') 
    search_fields = ('name', 'brand')
    list_filter = ('available', 'brand')  

    def image_tag(self, obj):
        if obj.image_url:
            return f'<img src="{obj.image_url}" width="100" height="100" />'
        return 'No image'
    image_tag.allow_tags = True  

admin.site.register(Car, CarAdmin)

class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'total_price')  
    search_fields = ('user__username', 'car__name')  
    list_filter = ('user', 'car', 'start_date')  
    readonly_fields = ('user', 'car', 'start_date', 'end_date', 'total_price')  

admin.site.register(Rental, RentalAdmin)
