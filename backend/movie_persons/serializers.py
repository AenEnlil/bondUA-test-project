from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import IntegerField
from .models import Person, MoviePerson


class PersonSerializer(ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class MoviePersonSerializer(ModelSerializer):
    person_id = IntegerField()

    class Meta:
        model = MoviePerson
        fields = ['person_id', 'role']
