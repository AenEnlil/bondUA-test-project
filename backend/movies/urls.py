from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import MovieViewSet

movie_router = SimpleRouter()
movie_router.register('movies', MovieViewSet)

urlpatterns = [
    path('', include(movie_router.urls))
]