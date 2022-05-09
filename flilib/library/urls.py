from django.urls import path, include

from . import views


app_name = 'library'

author = [
    path('', views.AuthorList.as_view(), name='list'),
    path('<str:slug>/', views.AuthorDetail.as_view(), name='detail'),
]

genre = [
    path('', views.GenreList.as_view(), name='list'),
    path('<slug:slug>/', views.GenreDetail.as_view(), name='detail'),
]

language = [
    path('', views.LanguageList.as_view(), name='list'),
    path('<slug:slug>/', views.LanguageDetail.as_view(), name='detail'),
]

series = [
    path('', views.SeriesList.as_view(), name='list'),
    path('<str:slug>/', views.SeriesDetail.as_view(), name='detail'),
]

book = [
    path('', views.BookList.as_view(), name='list'),
    path('<int:pk>/', views.BookDetail.as_view(), name='detail'),
    path('<int:pk>/download/', views.BookDownload.as_view(), name='download'),
]

urlpatterns = [
    path('author/', include((author, 'author'))),
    path('genre/', include((genre, 'genre'))),
    path('language/', include((language, 'language'))),
    path('series/', include((series, 'series'))),
    path('book/', include((book, 'book'))),
]
