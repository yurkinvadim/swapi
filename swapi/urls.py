from django.urls import path

from swapi.views import CollectionDetailView, CollectionListView, download_csv

urlpatterns = [
    path('', CollectionListView.as_view(), name='collection-list'),
    path('<int:pk>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('<int:pk>/download/', download_csv, name='download-csv')
]
