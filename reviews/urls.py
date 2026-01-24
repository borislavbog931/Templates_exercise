from django.urls import path, include

from reviews.views import recent_reviews, review_detail

app_name = 'reviews'
reviews_patterns = [
    path ('recent/', recent_reviews, name='recent'),
    path ('<int:pk>/', review_detail, name='detail'),
]

urlpatterns = [
    path('', include(reviews_patterns)),
]