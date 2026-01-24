from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

import reviews
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