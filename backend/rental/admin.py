from django.contrib import admin
from .models import Apartment, ApartmentImage


class ApartmentImageInline(admin.TabularInline):
	model = ApartmentImage
	extra = 1


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'rent', 'owner')

@admin.register(ApartmentImage)
class ApartmentImageAdmin(admin.ModelAdmin):
	list_display = ('apartment', 'uploaded_at')
