from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

from books.models import Book


def landing_page(request):
    all_books = Book.objects.all().annotate(
        avg_rating = Avg("reviews__rating"),
    ).order_by("title")
    total_books = all_books.count()
    context = {
        "books": all_books,
        "total_books": total_books,
        "page_title": 'Home'
    }
    return render(request, "books/landing_page.html", context)

def book_list(request):
    list_of_books = Book.objects.annotate(
        avg_rating = Avg("reviews__rating"),
    ).order_by("title")

    context = {
        'books': list_of_books,
        'page_title': 'Dashboard'
    }
    return render(request, "books/list_of_books.html", context)

def book_detail(request, slug:str):
    book = get_object_or_404(Book.objects.annotate(avg_rating=Avg("reviews__rating")), slug=slug)
    context = {
        'book': book,
        'page_title': f'{book.title} Details',
    }
    return render(request, "books/book_detail.html", context)