from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    people = models.ManyToManyField('movie_persons.Person', through='movie_persons.MoviePerson', related_name='movies')
