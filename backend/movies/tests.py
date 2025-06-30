import datetime

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import Movie


class MovieTestCase(APITestCase):
    model = Movie
    number_of_movies_to_create = 40

    @classmethod
    def setUpTestData(cls):
        number_of_movies_to_create = 40
        movies = []
        for i in range(0, number_of_movies_to_create):
            movies.append(cls.model(title=f'Movie_{i}', release_date=datetime.datetime.now().date()))
        cls.model.objects.bulk_create(movies)

    def test_list(self):
        url = reverse('movie-list')
        first_existed_movie = self.model.objects.first()
        movies_count = self.model.objects.all().count()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertEqual(len(response_data), movies_count)
        self.assertEqual(first_existed_movie.id, response_data[0].get('id'))

    def test_create(self):
        movie_name = 'NewMovie'
        data = {'title': movie_name, 'release_date': datetime.datetime.now().date()}
        url = reverse('movie-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        response_data = response.data
        self.assertTrue(response_data)

        movie_in_db = self.model.objects.get(id=response_data.get('id'))
        self.assertTrue(movie_in_db)
        self.assertEqual(movie_in_db.title, movie_name)

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
