from email import message
from operator import mod
from pyexpat import model
from statistics import mode
from tabnanny import verbose
from django.db import models

# Create your models here.
class Brand(models.Model):
    title = models.CharField(max_length=100, verbose_name='Бренд')
    def __str__(self):
        return self.title



class SneakersCart(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описние')
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='main', verbose_name='Фото')
    category = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.CASCADE)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    number = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    message = models.TextField(verbose_name='Message')
    sent_at = models.DateField(auto_now_add=True, verbose_name='Date')


class Order(models.Model):
    product = models.CharField(max_length=500, verbose_name='Order')
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, verbose_name='Client')
    total_price = models.IntegerField(verbose_name='Total price')
    phone = models.IntegerField(verbose_name='Phone number')
    address = models.CharField(max_length=500, null=True, verbose_name='Addres')
    date = models.DateField(auto_now_add=True, verbose_name='Date')