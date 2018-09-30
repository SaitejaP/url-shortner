from django.urls import path

from .views import ShortenUrlView, URLsListView

urlpatterns = [
    path('urls/', URLsListView.as_view(), name='list'),
    path('shorten/', ShortenUrlView.as_view(), name='shorten'),
]
