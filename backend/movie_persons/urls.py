from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PersonViewSet


person_router = SimpleRouter()
person_router.register('movie-persons', PersonViewSet)


urlpatterns = [
    path('', include(person_router.urls))
]
