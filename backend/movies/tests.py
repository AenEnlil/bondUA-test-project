import datetime
import json

from django.test import override_settings
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import Movie
from movie_persons.models import MoviePerson, Person

caches = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache", }}


@override_settings(CACHES=caches)
class MovieTestCase(APITestCase):
    model = Movie

    @classmethod
    def setUpTestData(cls):
        number_of_movies_to_create = 40
        movies = []
        for i in range(0, number_of_movies_to_create):
            movies.append(cls.model(title=f'Movie_{i}', release_year=datetime.datetime.now().date().year))
        cls.model.objects.bulk_create(movies)
        cls.test_person = Person.objects.create(name='test')

    def test_list_paginated(self):
        url = reverse('movie-list')
        movies_count = self.model.objects.all().count()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.data
        self.assertTrue(response_data)
        self.assertIn('count', response_data)
        self.assertIn('next', response_data)
        self.assertIn('previous', response_data)
        self.assertIn('results', response_data)
        self.assertEqual(response_data.get('count'), movies_count)
        self.assertTrue(response_data.get('next'))
        self.assertFalse(response_data.get('previous'))

    def test_list(self):
        url = reverse('movie-list')
        first_existed_movie = self.model.objects.first()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertEqual(first_existed_movie.id, response_data.get('results')[0].get('id'))

    def test_list_filter_by_release_year(self):
        release_year = 2012
        movie = self.model.objects.create(title='NewFilm1', release_year=release_year)
        movies_count = self.model.objects.count()
        self.assertTrue(movie)
        url = reverse('movie-list', query={'release_year': release_year})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertNotEqual(movies_count, response_data.get('count'))
        self.assertEqual(movie.pk, response_data['results'][0].get('id'))
        self.assertEqual(movie.release_year, response_data['results'][0].get('release_year'))

    def test_list_filter_by_director(self):
        movie = self.model.objects.create(title='NewFilm1', release_year=2025)
        MoviePerson.objects.create(person=self.test_person, movie=movie, role='director')
        movies_count = self.model.objects.count()
        self.assertTrue(movie)
        url = reverse('movie-list', query={'director': self.test_person.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertNotEqual(movies_count, response_data.get('count'))
        self.assertEqual(movie.pk, response_data['results'][0].get('id'))
        cast = response_data['results'][0].get('cast')
        self.assertTrue(cast)
        self.assertEqual(cast[0].get('person_id'), self.test_person.id)
        self.assertEqual(cast[0].get('role'), 'director')

    def test_list_filter_by_actor(self):
        movie = self.model.objects.create(title='NewFilm1', release_year=2025)
        MoviePerson.objects.create(person=self.test_person, movie=movie, role='actor')
        movies_count = self.model.objects.count()
        self.assertTrue(movie)
        url = reverse('movie-list', query={'actor': self.test_person.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertNotEqual(movies_count, response_data.get('count'))
        self.assertEqual(movie.pk, response_data['results'][0].get('id'))
        cast = response_data['results'][0].get('cast')
        self.assertTrue(cast)
        self.assertEqual(cast[0].get('person_id'), self.test_person.id)
        self.assertEqual(cast[0].get('role'), 'actor')

    def test_create(self):
        movie_name = 'NewMovie'
        data = {'title': movie_name, 'release_year': datetime.datetime.now().date().year,
                'cast': []}
        url = reverse('movie-list')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response_data = response.data
        self.assertTrue(response_data)

        movie_in_db = self.model.objects.get(id=response_data.get('id'))
        self.assertTrue(movie_in_db)
        self.assertEqual(movie_in_db.title, movie_name)

    def test_links_created(self):
        self.assertFalse(MoviePerson.objects.all().exists())
        movie_name = 'NewMovie'
        data = {'title': movie_name, 'release_year': datetime.datetime.now().date().year,
                'cast': [{'person_id': self.test_person.id, 'role': 'director'},
                         {'person_id': self.test_person.id, 'role': 'actor'}]}
        url = reverse('movie-list')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertTrue(MoviePerson.objects.all().exists())
        links = MoviePerson.objects.filter(movie_id=response_data.get('id'))
        self.assertTrue(links)
        self.assertEqual(len(data.get('cast')), len(links))

        person_data = data.get('cast')[0]
        self.assertEqual(person_data.get('person_id'), links[0].person_id)
        self.assertEqual(person_data.get('role'), links[0].role)

    def test_duplicate_cast_entries_are_removed(self):
        movie_name = 'NewMovie'
        data = {'title': movie_name, 'release_year': datetime.datetime.now().date().year,
                'cast': [{'person_id': self.test_person.id, 'role': 'actor'},
                         {'person_id': self.test_person.id, 'role': 'actor'}]}
        url = reverse('movie-list')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertEqual(len(response_data['cast']), 1)

    def test_error_when_invalid_release_year(self):
        movie_name = 'NewMovie'
        data = {'title': movie_name, 'release_year': 1111,
                'cast': []}
        url = reverse('movie-list')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response_data = response.data
        self.assertTrue(response_data.get('release_year'))

    def test_error_when_person_not_exists(self):
        movie_name = 'NewMovie'
        data = {'title': movie_name, 'release_year': datetime.datetime.now().date().year,
                'cast': [{'person_id': 999, 'role': 'actor'}]}
        url = reverse('movie-list')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response_data = response.data
        self.assertTrue(response_data.get('cast'))

    def test_error_when_several_directors_passed(self):
        person2 = Person.objects.create(name='testperson2')
        movie_name = 'NewMovie'
        data = {'title': movie_name, 'release_year': datetime.datetime.now().date().year,
                'cast': [{'person_id': self.test_person.id, 'role': 'director'},
                         {'person_id': person2.id, 'role': 'director'}]}
        url = reverse('movie-list')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response_data = response.data
        self.assertTrue(response_data.get('cast'))

    def test_retrieve(self):
        first_existed_movie = self.model.objects.first()
        url = reverse('movie-detail', kwargs={'pk': first_existed_movie.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertEqual(response_data.get('title'), first_existed_movie.title)

    def test_retrieve_non_existent_movie(self):
        url = reverse('movie-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        last_movie, new_title = self.model.objects.last(), 'new_title'
        self.assertTrue(last_movie)
        self.assertNotEqual(last_movie.title, new_title)
        new_data = {'title': new_title}
        url = reverse('movie-detail', kwargs={'pk': last_movie.id})
        response = self.client.patch(url, data=new_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertEqual(response_data.get('id'), last_movie.id)
        self.assertEqual(response_data.get('title'), new_title)

    def test_update_non_existent_movie(self):
        url = reverse('movie-detail', kwargs={'pk': 999})
        response = self.client.patch(url, data={'title': 'new_title'})
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        last_movie = self.model.objects.last()
        self.assertTrue(last_movie)
        url = reverse('movie-detail', kwargs={'pk': last_movie.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        movie_exist = self.model.objects.filter(id=last_movie.id).exists()
        self.assertFalse(movie_exist)

    def test_delete_non_existent_movie(self):
        url = reverse('movie-detail', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
