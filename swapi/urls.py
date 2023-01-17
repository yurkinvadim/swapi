from django.urls import path

from swapi.views import CollectionDetailView, CollectionListView, download_csv

urlpatterns = [
    path('', CollectionListView.as_view(), name='collection-list'),
    path('<pk>', CollectionDetailView.as_view(), name='collection-detail'),
    path('<pk>/download/', download_csv, name='download-csv')
]
