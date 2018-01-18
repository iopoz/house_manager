from django.contrib import admin

# Register your models here.
from .models import Flat, CategoryMoney, MoneyReport

admin.site.register(Flat)
admin.site.register(CategoryMoney)
admin.site.register(MoneyReport)