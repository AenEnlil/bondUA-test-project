from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    people = models.ManyToManyField('movie_persons.Person', through='movie_persons.MoviePerson', related_name='movies')
