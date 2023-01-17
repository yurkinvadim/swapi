from datetime import datetime

import petl as etl
import requests

from config.settings import SWAPI_URL


class StarWarsAPI:

    def __init__(self):
        urls = requests.get(SWAPI_URL).json()
        self._people_url = urls.get('people')
        self._planets_url = urls.get('planets')

    def _get_people_data(self):
        people_data = []
        url = self._people_url
        while True:
            data = requests.get(url).json()
            people_data.extend(
                [
                    {
                        'name': person.get('name'),
                        'height': person.get('height'),
                        'mass': person.get('mass'),
                        'hair_color': person.get('hair_color'),
                        'skin_color': person.get('skin_color'),
                        'eye_color': person.get('eye_color'),
                        'birth_year': person.get('birth_year'),
                        'gender': person.get('gender'),
                        'homeworld': person.get('homeworld'),
                        'edited': person.get('edited'),

                    } for person in data.get('results')
                ]
            )
            url = data.get('next')
            if not url:
                break
        return people_data

    def _get_planets_dict(self):
        planets_dict = {}
        url = self._planets_url
        while True:
            data = requests.get(url).json()
            planets_dict.update({planet.get('url'): planet.get('name') for planet in data.get('results')})
            url = data.get('next')
            if not url:
                break
        return planets_dict

    @staticmethod
    def _transform_to_table(people_data, planets_dict):
        people_table = etl.fromdicts(
            dicts=people_data,
            header=[
                'name',
                'height',
                'mass',
                'hair_color',
                'skin_color',
                'eye_color',
                'birth_year',
                'gender',
                'homeworld',
                'edited',
            ]
        )

        people_table = etl.convert(
            people_table,
            'homeworld',
            planets_dict
        )
        people_table = etl.addfield(
            people_table,
            'date',
            lambda rec: datetime.strptime(rec['edited'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d')
        )
        people_table = etl.cutout(people_table, 'edited')
        return people_table

    def get_people_table(self):
        planets_dict = self._get_planets_dict()
        people_data = self._get_people_data()
        people_table = self._transform_to_table(people_data, planets_dict)
        return people_table
