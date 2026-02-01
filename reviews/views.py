from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from books.models import Book
from reviews.forms import ReviewForm, ReviewEditForm, ReviewDeleteForm
from reviews.models import Review


def recent_reviews(request: HttpRequest) -> HttpResponse:
    DEFAULT_REVIEW_COUNT = 5
    reviews_count = int(request.GET.get('count', DEFAULT_REVIEW_COUNT))
    reviews = Review.objects.select_related('book')[:reviews_count] #Join every review with the book it corresponds to

    context = {
        'reviews': reviews,
        'page_title': 'Recent Book Reviews',
    }

    return render(request, 'reviews/recent_reviews.html', context)

def review_detail(request: HttpRequest, pk: int) -> HttpResponse:
    review = get_object_or_404(Review.objects.select_related('book'), pk=pk)
    context = {
        'review': review,
        'page_title': f'{review.author}\'s Review of {review.book.title}',
    }
    return render(request, 'reviews/review_detail.html', context)


def review_create(request: HttpRequest, book_slug: str | None = None) -> HttpResponse:
    book = None
    if book_slug:
        book = get_object_or_404(Book, slug=book_slug)

    initial_data = {}
    if book:
        initial_data['book'] = book

    form = ReviewForm(request.POST or None, initial=initial_data)

    if request.method == "POST" and form.is_valid():
        review = form.save()
        return redirect("reviews:detail", pk=review.pk)

    context = {
        "form": form,
        "book": book, # Pass the book to the template for context if needed
    }
    return render(request, 'reviews/create.html', context)


def review_edit(request: HttpRequest, pk: int) -> HttpResponse:
    review = get_object_or_404(Review, pk=pk)
    form = ReviewEditForm(request.POST or None, instance=review)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("reviews:detail", pk=review.pk)

    context = {
        "form": form,
        "review": review,
    }
    return render(request, 'reviews/edit.html', context)


def review_delete(request: HttpRequest, pk: int) -> HttpResponse:
    review = get_object_or_404(Review, pk=pk)
    form = ReviewDeleteForm(request.POST or None, instance=review)
    if request.method == "POST":
        review.delete()
        return redirect("reviews:list")

    context = {
        "form": form,
        "review": review,
    }
    return render(request, 'reviews/delete.html', context)