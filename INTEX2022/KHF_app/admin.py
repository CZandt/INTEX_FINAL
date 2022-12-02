from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import recommendation, user, meal, food_item, food_item_in_meal, registeredUser
# Register your models here.
admin.site.register(recommendation)
admin.site.register(user)
admin.site.register(meal)
admin.site.register(food_item)
admin.site.register(food_item_in_meal)
admin.site.register(registeredUser, UserAdmin)