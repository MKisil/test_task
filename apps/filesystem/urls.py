from django.urls import path

from .views import (
    FileView,
    DirectoryView
)

urlpatterns = [
    path('file/', FileView.as_view()),
    path('file/<path:path>/', FileView.as_view()),
    path('directory/', DirectoryView.as_view()),
    path('directory/<path:path>/', DirectoryView.as_view()),
]
