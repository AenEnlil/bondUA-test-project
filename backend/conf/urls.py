from django.urls import path, include

urlpatterns = [
    path('api/v1/movies', include('movies.urls')),
    path('api/v1/', include('movie_persons.urls'))
]
