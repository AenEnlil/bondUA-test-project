import json
from datetime import date
from collections import Counter

from django.http import QueryDict
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from .models import Movie
from movie_persons.serializers import MoviePersonSerializer
from movie_persons.models import MoviePerson, Person


class MovieSerializer(ModelSerializer):
    cast = MoviePersonSerializer(source='movieperson_set', many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_year', 'cast']

    def _clean_cast_field_from_duplicates(self, data):
        seen = set()
        cleaned = []
        for item in data:
            key = (item['person_id'], item['role'])
            if key not in seen:
                seen.add(key)
                cleaned.append(item)
        return cleaned

    def _update_movie_person_relations(self, instance, data):
        new_links = {(person.get('person_id'), person.get('role')): person for person in data}
        existing_links = {(person.person_id, person.role): person for person in instance.movieperson_set.all()}
        links_to_create = []

        for key, data in new_links.items():
            if key in existing_links:
                existing_links.pop(key)
            else:
                links_to_create.append(MoviePerson(movie=instance, **data))
        MoviePerson.objects.bulk_create(links_to_create)

        # if any links remains in existing_links that means they not valid anymore, therefore remove them
        links_to_remove = [link.id for link in existing_links.values()]
        if links_to_remove:
            MoviePerson.objects.filter(id__in=links_to_remove).delete()

    def _querydict_to_dict(self, data: QueryDict) -> dict:
        """
        Transform QueryDict to python dictionary
        """
        result = {}
        for key in data:
            values = data.getlist(key)
            result[key] = values if len(values) > 1 else values[0]
        return result

    def to_internal_value(self, data):
        """
        Extends behaviour to support form-data with nested structures. If request.data is QueryDict,
        then it will be transformed to python dict and 'cast' field will be transformed from str to list
        """
        if isinstance(data, QueryDict):
            data = self._querydict_to_dict(data)
            cast = data.get('cast')
            if isinstance(cast, str):
                try:
                    data['cast'] = json.loads(cast)
                except json.JSONDecodeError:
                    raise ValidationError({'cast': 'Invalid JSON'})

        return super().to_internal_value(data)

    def validate_release_year(self, value):
        year_shift = 15
        min_year, max_year = 1896, date.today().year + year_shift
        if value > max_year:
            raise ValidationError(f"release year can`t be higher than {max_year}")
        elif value < min_year:
            raise ValidationError(f"release year can`t be lower than {min_year}")
        return value

    def validate_cast(self, data):
        cleaned_data = self._clean_cast_field_from_duplicates(data)

        # validate that movie have one director
        roles_count = Counter([item.get('role') for item in cleaned_data])
        if roles_count.get('director', 0) > 1:
            raise ValidationError('Movie can have only one director')

        # validate person ids in bulk to optimize db queries
        person_ids = [person.get('person_id') for person in cleaned_data]
        persons_in_db = Person.objects.in_bulk(person_ids)
        missing_ids = set(person_ids) - set(persons_in_db)
        if missing_ids:
            raise ValidationError(f'Invalid person_id(s): {missing_ids}')
        return cleaned_data

    def create(self, validated_data):
        cast_data = validated_data.pop('movieperson_set')
        instance = Movie.objects.create(**validated_data)

        # create records in MtM table
        movie_person_entries = []
        for person in cast_data:
            movie_person_entries.append(MoviePerson(movie_id=instance.pk, person_id=person.get('person_id'),
                                                    role=person.get('role')))
        MoviePerson.objects.bulk_create(movie_person_entries)
        return instance

    def update(self, instance, validated_data):
        cast_data = validated_data.pop('movieperson_set', None)
        instance = super().update(instance, validated_data)
        if cast_data is not None:
            self._update_movie_person_relations(instance, cast_data)
        return instance
