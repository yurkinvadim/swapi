from datetime import datetime

import petl as etl
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
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
        collection = get_object_or_404(Collection, pk=pk)
        table = collection.table
        number_of_people = int(request.GET.get('n', 10))
        people = table.head(n=number_of_people).dicts()

        context = {
            'collection': collection,
            'people': people,
            'n': number_of_people,
        }
        return render(request, 'swapi/collection_detail.html', context=context)


def download_csv(request, pk):
    collection = Collection.objects.get(pk=pk)
    filename = collection.filename
    return FileResponse(open(f'{MEDIA_ROOT}/{filename}', 'rb'))


def value_count(request, pk):
    if request.method == 'GET':
        return redirect('collection-detail', pk=pk)

    if request.method == 'POST':
        fields = tuple(field for field in request.POST.keys() if field != 'csrfmiddlewaretoken')

        if not fields:
            return redirect('collection-detail', pk=pk)

        collection = get_object_or_404(Collection, pk=pk)

        table = collection.table
        table = etl.aggregate(table, fields, aggregation=len)
        headers = etl.header(table)
        data = etl.data(table)
        context = {
            'data': data,
            'headers': headers,
        }
        return render(request, 'swapi/value_count.html', context=context)
