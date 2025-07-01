from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    people = models.ManyToManyField('movie_persons.Person', through='movie_persons.MoviePerson', related_name='movies')
