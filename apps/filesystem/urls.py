from django.urls import path

from .views import (
    FileListView,
    FileDetailView,
    FilenameSearchView,
    ContentSearchView,
    MetadataView,
    DirectoryView
)

urlpatterns = [
    path('files/', FileListView.as_view()),
    path('files/<str:name>/', FileDetailView.as_view()),
    path('search/filename/', FilenameSearchView.as_view()),
    path('search/content/', ContentSearchView.as_view()),
    path('metadata/<str:name>/', MetadataView.as_view()),
    path('directories/', DirectoryView.as_view()),
]
