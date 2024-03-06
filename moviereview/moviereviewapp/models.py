from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)


    def __str__(self):
        return self.name

class Movies(models.Model):
    title = models.CharField(max_length=250)
    poster = models.ImageField(upload_to='gallery')
    desc = models.TextField()
    release = models.DateField()
    actors = models.CharField(max_length=250)
    actress = models.CharField(max_length=250)
    categories = models.ManyToManyField(Category)
    trailer_link = models.URLField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
class Review(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username