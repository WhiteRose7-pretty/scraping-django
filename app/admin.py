from django.contrib import admin
from .models import Product, Limit

def duplicate(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate.short_description = "Copy select element"

class AdminCopy(admin.ModelAdmin):
    actions = [duplicate]

admin.site.register(Product, AdminCopy)
admin.site.register(Limit)