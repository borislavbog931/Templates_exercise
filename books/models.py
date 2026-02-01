from django.db import models
from django.utils.text import slugify

from common.models import TimeStampedModel


class Book(TimeStampedModel):
    class GenreChoices(models.TextChoices):
        FICTION = "Fiction", "Fiction" #първата стойност се пази в базата данни, втората е за показване на потребителя
        NON_FICTION = "Non-Fiction", "Non-Fiction"
        FANTASY = "Fantasy", "Fantasy"
        SCIENCE = "Science", "Science"
        HISTORY = "History", "History"
        MYSTERY = "Mystery", "Mystery"


    title = models.CharField(unique=True, max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    isbn = models.CharField(unique=True, max_length=20)
    genre = models.CharField(max_length=50, choices=GenreChoices.choices)
    publishing_date = models.DateField()
    description = models.TextField()
    image_url = models.URLField()
    slug = models.SlugField(max_length=100, blank=True,unique=True)
    pages = models.PositiveIntegerField(null =True, blank=True)
    publisher = models.CharField(max_length=100)

    def save (self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title} - {self.publisher}')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(Book, related_name='tags')

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name