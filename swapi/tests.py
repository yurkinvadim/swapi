import os

import petl as etl
import pytest
import requests
from bs4 import BeautifulSoup
from django.shortcuts import reverse
from django.test import Client

from config.settings import MEDIA_ROOT
from swapi.models import Collection

COLLECTION_URL = reverse('collection-list')


@pytest.mark.django_db
def test_collection_model():
    Collection.objects.create(filename='firstfile.csv')
    assert Collection.objects.count() == 1

    # test auto_now_add
    assert Collection.objects.first().created_at

    # test ordering
    Collection.objects.create(filename='secondfile.csv')
    assert Collection.objects.first().filename == 'secondfile.csv'


@pytest.mark.django_db
def test_collection_list_page():
    client = Client()
    response = client.get(COLLECTION_URL)
    assert response.status_code == 200

    # check "Fetch" button
    soup = BeautifulSoup(response.content, "html.parser")
    fetch_input = soup.find_all(attrs={'value': 'Fetch'})[0]
    assert fetch_input

    # test creating csv and collection object after post request
    assert Collection.objects.count() == 0
    client.post(COLLECTION_URL)

    assert Collection.objects.count() == 1
    collection = Collection.objects.first()
    assert os.path.isfile(f'{MEDIA_ROOT}/{collection.filename}')
    os.remove(f'{MEDIA_ROOT}/{collection.filename}')


@pytest.mark.django_db
def test_collection_detail_status_codes():
    client = Client()
    response = client.get(COLLECTION_URL+'1/')
    assert response.status_code == 404

    # making fetch
    client.post(COLLECTION_URL)

    response = client.get(COLLECTION_URL+'1/')
    assert response.status_code == 200

    os.remove(f'{MEDIA_ROOT}/{Collection.objects.first().filename}')


@pytest.mark.django_db
def test_swapi_class():
    client = Client()
    client.post(COLLECTION_URL)

    collection = Collection.objects.first()
    table = collection.table

    response = requests.get("https://swapi.dev/api/people/")

    assert response.json().get('count') == len(etl.data(table))
    os.remove(f'{MEDIA_ROOT}/{Collection.objects.first().filename}')