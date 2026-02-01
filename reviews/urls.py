from django.urls import path, include

from reviews.views import recent_reviews, review_detail, review_create, review_edit, review_delete

app_name = 'reviews'

urlpatterns = [
    path('', recent_reviews, name='list'),
    path('create/', review_create, name='create'),
    path('create/<slug:book_slug>/', review_create, name='create_for_book'),
    path('<int:pk>/', include([
        path('', review_detail, name='detail'),
        path('edit/', review_edit, name='edit'),
        path('delete/', review_delete, name='delete'),
    ])),
]