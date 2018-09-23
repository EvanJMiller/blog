from django.urls import path, re_path
from django.conf.urls.static import settings
from django.conf.urls.static import static
from . import views

#Specify the app name lets django know which url to use and when i.e. blog:HomeView
app_name = 'blog'

urlpatterns = [

    path('home', views.HomeView.as_view(), name='HomeView'),
    path('login', views.LoginView.as_view(), name='LoginView'),
    path('logout', views.logout, name='Logout'),
    path('register', views.RegisterView.as_view(), name='RegisterView'),
    path('authors', views.AuthorsView.as_view(), name='AuthorView'),
    re_path(r'^articles/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w-]+)', views.ArticleView.as_view(), name='ArticleView'),
    re_path(r'^articles/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})', views.ArchiveView.as_view(), name='DayMonthYearView'),
    re_path(r'^articles/(?P<year>\d{4})/(?P<month>\d{1,2})', views.ArchiveView.as_view(), name='MonthYearView'),
    re_path(r'^articles/(?P<year>\d{4})', views.ArchiveView.as_view(), name='YearView'),
    re_path('articles/(?P<tag>[\w0-9]+)$', views.TagView.as_view(), name='TagView'),
    re_path(r'^articles/(?P<username>[\w0-9]+)', views.articlesByAuthor, name='userArticles'),
    re_path(r'^authors/(?P<username>[\w0-9]+)/about$', views.AboutAuthorView.as_view(), name='aboutAuthorView'),
    re_path(r'^authors/(?P<username>[\w0-9]+)/edit$', views.editAuthorArticles, name='edit'),
    re_path(r'^authors/(?P<username>[\w0-9]+)/edit/(?P<id>[0-9]+)', views.EditView.as_view(), name='editArticle')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


