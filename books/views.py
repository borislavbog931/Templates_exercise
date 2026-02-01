from django.db.models import Avg, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from books.forms import BookFormBasic, BookEditForm, BookDeleteForm, BookSearchForm
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
    search_form = BookSearchForm(request.GET or None)
    list_of_books = Book.objects.annotate(
        avg_rating = Avg("reviews__rating"),
    ).order_by("title")

    if search_form.is_valid():
        search_value = search_form.cleaned_data.get("query")
        if search_value:
            list_of_books = list_of_books.filter(
                Q(title__icontains=search_value)|
                Q(description__icontains=search_value)
            )

    context = {
        'books': list_of_books,
        'page_title': 'Dashboard',
        'search_form': search_form,
    }
    return render(request, "books/list_of_books.html", context)

def book_detail(request, slug:str):
    book = get_object_or_404(Book.objects.annotate(avg_rating=Avg("reviews__rating")), slug=slug)
    context = {
        'book': book,
        'page_title': f'{book.title} Details',
    }
    return render(request, "books/book_detail.html", context)


def book_create(request: HttpRequest):
    form = BookFormBasic(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save() # when we use Model forms
        # Book.objects.create(  #creating an object) # or (**form.cleaned_data)
        #     title=form.cleaned_data["title"],
        #     genre=form.cleaned_data["genre"],
        #     publishing_date=form.cleaned_data["publishing_date"],
        #     isbn=form.cleaned_data["isbn"],
        #     price=form.cleaned_data["price"],
        #     description=form.cleaned_data["description"],
        #     image_url=form.cleaned_data["image_url"],
        #     publisher=form.cleaned_data["publisher"],
        #
        # )
        return redirect ("books:home")

    context = {
        "form": form,
    }
    return render(request, 'books/create.html', context)

def book_edit(request:HttpRequest, pk:int) -> HttpResponse:
    book = Book.objects.get(pk=pk)
    form = BookEditForm(request.POST or None, instance=book) #
    if request.method == "POST" and form.is_valid():
        form.save() # when we use Model forms
        return redirect ("books:home")
    context = {
        "form": form,
    }
    return render(request, 'books/edit.html', context)

def book_delete(request:HttpRequest, pk:int) -> HttpResponse:
    book = Book.objects.get(pk=pk)
    form = BookDeleteForm(request.POST or None, instance=book) #
    if request.method == "POST" and form.is_valid():
        book.delete()
        return redirect ("books:home")
    context = {
        "form": form,
    }
    return render(request, 'books/delete.html', context)