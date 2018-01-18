from django.db import models


# Create your models here.

class Flat(models.Model):
    flat_owner = models.CharField(max_length=50)
    flat_number = models.CharField(max_length=2)
    def __str__(self):
        return self.flat_number


class CategoryMoney(models.Model):
    category_name = models.CharField(max_length=10)
    def __str__(self):
        return self.category_name


class MoneyReport(models.Model):
    user = models.ForeignKey(Flat, on_delete=models.CASCADE)
    type_service = models.ForeignKey(CategoryMoney, on_delete=models.CASCADE)
    name_service = models.CharField(max_length=200)
    money = models.IntegerField()
    plan_date = models.DateField(blank=True, null=True)
    current_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.name_service
