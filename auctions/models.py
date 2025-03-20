from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    watchList = models.ManyToManyField('Listing', related_name="users")


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
    create_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['creator', 'title'], name='unique_title_per_user'),
        ]

    def __str__(self):
        return f"creator: {self.creator}, title: {self.title}, category: {self.category}, description: {self.description}, price: {self.price}, image: {self.image}, creation_date: {self.create_date}, close_date: {self.close_date}, is_active: {self.is_active}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.amount <= self.listing.price:
            raise ValidationError("Bid amount must be greater than or equal to the current price")
        if self.listing.is_active == False:
            raise ValidationError("Listing is closed")
        listing = Listing.objects.filter(pk=self.listing.id)
        listing.update(price=self.amount)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"""Post {self.listing.title} by {self.listing.creator.username}, bid: {self.amount}, 
            by {self.author.username}, date: {self.date}"""

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""Post {self.listing.title} by {self.listing.creator.username}, comment: {self.comment}, 
            by {self.author.username}, date: {self.date}"""

