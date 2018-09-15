from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout

from .models import LoginForm, RegisterForm,Article, ArticleForm

from pprint import pprint as pp

import datetime

def year(request, year):

    return HttpResponse("<h1>Year</h1>")

def articlesByAuthor(request, username):

    user = User.objects.filter(username=username)[0]

    context = {'articles': user.article_set.all()}

    for article in user.article_set.all():
        print("Artile id: " + str(article.id))

    return render(request, 'blog/ArticleResultsPage.html', context)

def editAuthorArticles(request, username):

    print("edit author articles")

    #Check the method, get session data
    if request.method == 'GET':

        if request.user.is_authenticated and request.user.username == username:
            print("User logged in and can edit")
            #get the authors articles
            context = {
                'articles' : request.user.article_set.all().order_by('-date'),
                'author_logged_in' : True
            }

            return render(request, 'blog/ArticleResultsPage.html', context)
        else:
            return HttpResponse("<h1> Error! User not found </h1>")

def editArticle(request, username, id):

    if request.method == "GET":
        if request.user.is_authenticated and request.user.username == username:

            if request.user.article_set.get(pk=id) is not None:
                print("Article found")
                article = request.user.article_set.get(pk=id)

                default = {
                    'title': article.title,
                    'preview': article.preview,
                    'slug': article.slug,
                    'subtitle': article.subtitle,
                    'body' : article.body,
                    'tags' : article.tags,
                    'image': article.image
                }

                article_form = ArticleForm(initial=default)


                context = {'form':article_form, 'title': 'Edit Article', 'button_title': 'Save'}
                return render(request, 'blog/base_form.html', context)
            else:
                return HttpResponse("<h1> Error! Article not found. </h1>")
        else:
            return HttpResponse("<h1> Error! Not logged in or permission denied </h1>")

    if request.method == 'POST':
        print("Submit form...")

        if request.user.is_authenticated:
            form = ArticleForm(request.POST, request.FILES)

            article = request.user.article_set.get(pk=id)

            print(form.errors)

            if form.is_valid():

                article.title = form.cleaned_data['title']
                article.slug = form.cleaned_data['slug']
                article.subtitle = form.cleaned_data['subtitle']
                article.preview = form.cleaned_data['preview']
                article.body = form.cleaned_data['body']
                article.image = form.cleaned_data['image']

                article.tags = form.cleaned_data['tags']
                article.save()

                print("Article saved successfully...")
                return HttpResponseRedirect(reverse('blog:edit', args=[username]))

            else:
                #Invlid form, notify the front end...
                return JsonResponse({'status': 'false', 'message': 'invalid form', 'errors': form.errors}, status=500)


class ArchiveView(TemplateView):

    template_name = 'blog/ArticleResultsPage.html'

    def get_context_data(self, **kwargs):

        #use kwargs to determine how to filter articles by dates
        year = kwargs.get("year")
        month = kwargs.get("month")
        day = kwargs.get("day")
        pp(kwargs)
        if year and month and day:

            articles = Article.objects.filter(date__year=year, date__month=month, date__day=day)
        elif year and month:
            articles = Article.objects.filter(date__year=year, date__month=month).order_by('-date')
        elif year:

            articles = Article.objects.filter(date__year=year)

        #cut off results
        if len(articles) > 9:
            articles = articles[0:9]

        context = super().get_context_data()
        context['articles'] = articles

        return context

class ArticleView(TemplateView):

    template_name = 'blog/ArticlePage.html'

    def get_context_data(self, **kwargs):
        date = datetime.date(int(kwargs['year']), int(kwargs['month']), int(kwargs['day']))

        #Need form validation to make sure slug entires do not contain spaces, only - dashes
        article = Article.objects.filter(date__date=date).filter(slug__contains=kwargs['slug'])[0]
        recent_articles = Article.objects.order_by('-date')[0:5]
        context = super().get_context_data()
        context['article'] = article
        context['recent_articles'] = recent_articles
        return context

class TagView(TemplateView):

    template_name = 'blog/ArticleResultsPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs['tag']
        articles = Article.objects.filter(tags__contains=tag).order_by('-date')[:]
        context['articles'] = articles
        return context

def logout(request):

    if request.method == 'GET':
        auth_logout(request)

        return HttpResponseRedirect(reverse('blog:HomeView'))

class LoginView(FormView):

    template_name = 'blog/login.html'
    form_class = LoginForm
    success_url = 'blog:HomeView'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('blog:HomeView'))

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)

        if user is None:
            return HttpResponseRedirect(reverse('blog:RegisterView'))
        else:
            auth_login(self.request, user)
            return HttpResponseRedirect(reverse('blog:HomeView'))

    def form_invalid(self, form):
        print("Invalid Form")
        return HttpResponseRedirect(reverse('blog:LoginView'))

class RegisterView(FormView):
    template_name = 'blog/register.html'
    success_url = '/home/'
    form_class = RegisterForm

    def form_valid(self, form):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)
        if user is None:
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.save()
            auth_login(self.request, new_user)
        elif not user.is_authenticated:
            auth_login(self.request, user)

        return HttpResponseRedirect(reverse('blog:home'))

class HomeView(View):

    def get(self, request, *args, **kwargs):

        latest_articles = Article.objects.order_by('-date')[:]
        rows = int(len(latest_articles) / 3)

        deck = []
        for i in range(rows):
            print(i)
            row = latest_articles[3 * i:3 * (i + 1)]
            deck.append(row)

        if request.user.is_authenticated:

            return render(request, 'blog/home.html', {'deck': deck, 'user': request.user})
        else:

            return render(request, 'blog/home.html', {'deck': deck})

    def post(self, request, *args, **kwargs):
        pass




