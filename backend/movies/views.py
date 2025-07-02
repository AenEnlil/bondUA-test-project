from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from .filters import MovieFilter
from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().order_by('title')
    serializer_class = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = MovieFilter
