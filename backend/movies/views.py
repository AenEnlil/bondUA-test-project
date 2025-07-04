from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from .filters import MovieFilter
from .models import Movie
from .serializers import MovieSerializer
from movie_persons.models import MoviePerson


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().order_by('title').prefetch_related(Prefetch('movieperson_set',
                                                                               queryset=MoviePerson.objects.select_related('person')))
    serializer_class = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = MovieFilter
