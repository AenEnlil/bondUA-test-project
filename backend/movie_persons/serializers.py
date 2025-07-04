from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import IntegerField, CharField
from .models import Person, MoviePerson


class PersonSerializer(ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class MoviePersonSerializer(ModelSerializer):
    person_id = IntegerField()
    person_name = CharField(source='person.name', read_only=True)

    class Meta:
        model = MoviePerson
        fields = ['person_id', 'person_name', 'role']
