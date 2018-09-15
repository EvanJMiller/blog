from django.db import models
from django import forms

from django.contrib.auth.models import User

class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField()
    email = forms.EmailField()

class ArticleForm(forms.Form):

    title = forms.CharField(max_length=300)
    slug = forms.CharField(max_length=300)
    subtitle = forms.CharField(max_length=300)
    preview = forms.CharField(widget=forms.Textarea)
    body = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    tags = forms.CharField(max_length=200)

class Article(models.Model):

    author = models.ManyToManyField(User)
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300)
    preview = models.TextField()
    body = models.TextField()
    status = models.CharField(max_length=100)
    date = models.DateTimeField()
    tags = models.CharField(max_length=200)

    views = models.IntegerField()
    image = models.ImageField(default='default.png')

    def get_url(self):

        url = 'http://127.0.0.1:8000/blog/articles/'
        url += str(self.date.year) + '/' + str(self.date.month) + '/' + str(self.date.day)
        url += '/' + self.slug.replace(' ', '-')
        return url

    def edit_url(self):
        url = 'http://127.0.0.1:8000/blog/authors/'
        url += str(self.author.all()[0]) + "/edit/" + str(self.pk)
        return url

    def get_tags(self):
        return self.tags.strip().replace(",", " ").split()

    def authorName(self):
        try:
            author = self.author.all()[0]
            return author.first_name + " " + author.last_name
        except:
            return ""

class Comment(models.Model):
    text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField()

