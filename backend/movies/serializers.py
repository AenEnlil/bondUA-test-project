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

    def validate_cast(self, data):
        # validate person ids in bulk to optimize db queries
        person_ids = [person.get('person_id') for person in data]
        persons_in_db = Person.objects.in_bulk(person_ids)
        missing_ids = set(person_ids) - set(persons_in_db)
        if missing_ids:
            raise ValidationError(f'Invalid person_id(s): {missing_ids}')
        return data

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
