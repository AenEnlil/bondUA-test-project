from rest_framework.viewsets import ModelViewSet
from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().order_by('title')
    serializer_class = MovieSerializer
