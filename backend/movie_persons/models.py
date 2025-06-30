from django.db import models

# Create your models here.

# roles, person, movie_person


class Person(models.Model):
    name = models.CharField(max_length=255)


class MoviePerson(models.Model):
    ROLE_CHOICES = (
        ('director', 'Director'),
        ('actor', 'Actor'),
    )

    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES)