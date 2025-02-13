from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchList = models.ManyToManyField('Listing', related_name="users")

class User2(models.Model):
    username = models.CharField(max_length=64, primary_key=True, unique=True)
    password = models.CharField(max_length=64)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User,  on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    category = models.ManyToManyField(Category, related_name="listings")
    description = models.TextField()
    price = models.FloatField()
    image = models.URLField()
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['creator', 'title'], name='unique_title_per_user'),
        ]

    def __str__(self):
        return f"creator: {self.creator}, title: {self.title}, category: {self.category}, description: {self.description}, price: {self.price}, image: {self.image}, date: {self.date}, is_active: {self.is_active}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

