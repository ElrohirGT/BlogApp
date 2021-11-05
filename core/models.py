from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ManyToOneRel
from django_quill.fields import QuillField
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class User(models.Model):

    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Password = models.BinaryField(max_length=64)
    Salt = models.BinaryField(max_length=32)
    JoinedSince = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.Name} : {self.Email}"

class Article(models.Model):

    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=50)
    Body = QuillField()
    ReadTime = models.TimeField(auto_now=False, auto_now_add=False)
    PublishedDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"
        ordering = ['PublishedDate']

    def __str__(self):
        return f"[{self.Author.Name}] {self.Title}"

class Comment(models.Model):

    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Article = models.ForeignKey(Article, on_delete=models.CASCADE)
    Body = QuillField()
    PublishedDate = models.DateTimeField(default=timezone.now)
    LastEditDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ['PublishedDate']

    def __str__(self):
        return f"[{self.PublishedDate}] {self.Author}"
