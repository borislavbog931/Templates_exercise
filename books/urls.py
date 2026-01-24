from django.urls import path, include

from books.views import landing_page, book_list, book_detail

app_name = 'books'
books_patterns = [
    path('', book_list, name='list'),
    path('<slug:slug>/', book_detail, name='detail')
]
urlpatterns = [
    path('', landing_page, name='home'),
    path('books/', include(books_patterns)),
]