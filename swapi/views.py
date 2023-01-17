from datetime import datetime

import petl as etl
from django.http import FileResponse
from django.shortcuts import render
from django.views import View

from config.settings import MEDIA_ROOT
from swapi.models import Collection
from swapi.utils import StarWarsAPI


class CollectionListView(View):
    def get(self, request):

        collections = Collection.objects.all()
        latest_collection = collections.first()
        other_collections = collections[1:]

        context = {
            'latest_collection': latest_collection,
            'other_collections': other_collections,
        }

        return render(request, 'swapi/collection_list.html', context=context)

    def post(self, request):
        sw = StarWarsAPI()
        people_table = sw.get_people_table()
        filename = 'sw_' + datetime.now().strftime("%y%m%d_%H%M%S%f") + '.csv'
        etl.tocsv(people_table, f'{MEDIA_ROOT}/{filename}')
        Collection.objects.create(filename=filename)

        collections = Collection.objects.all()
        latest_collection = collections.first()
        other_collections = collections[1:]

        context = {
            'latest_collection': latest_collection,
            'other_collections': other_collections,
        }

        return render(request, 'swapi/collection_list.html', context=context)


class CollectionDetailView(View):
    def get(self, request, pk):
        collection = Collection.objects.get(pk=pk)
        context = {
            'collection': collection
        }
        return render(request, 'swapi/collection_detail.html', context=context)


def download_csv(request, pk):
    collection = Collection.objects.get(pk=pk)
    filename = collection.filename
    return FileResponse(open(f'{MEDIA_ROOT}/{filename}', 'rb'))
