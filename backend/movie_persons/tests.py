from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import Person


class PersonTestCase(APITestCase):
    model = Person

    @classmethod
    def setUpTestData(cls):
        number_of_persons_to_create = 40
        persons = []
        for i in range(0, number_of_persons_to_create):
            persons.append(cls.model(name=f'Name_{i}'))
        cls.model.objects.bulk_create(persons)

    def test_list(self):
        url = reverse('person-list')
        first_existed_person = self.model.objects.first()
        persons_count = self.model.objects.all().count()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertEqual(len(response_data), persons_count)
        self.assertEqual(first_existed_person.id, response_data[0].get('id'))

    def test_create(self):
        person_name = 'Test Person'
        data = {'name': person_name}
        url = reverse('person-list')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)

        response_data = response.data
        self.assertTrue(response_data)

        person_in_db = self.model.objects.get(id=response_data.get('id'))
        self.assertTrue(person_in_db)
        self.assertEqual(person_in_db.name, person_name)

    def test_retrieve(self):
        first_existed_person = self.model.objects.first()
        url = reverse('person-detail', kwargs={'pk': first_existed_person.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertEqual(response_data.get('name'), first_existed_person.name)

    def test_retrieve_non_existent_person(self):
        url = reverse('person-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        last_person, new_name = self.model.objects.last(), 'new_name'
        self.assertTrue(last_person)
        self.assertNotEqual(last_person.name, new_name)
        new_data = {'name': new_name}
        url = reverse('person-detail', kwargs={'pk': last_person.id})
        response = self.client.patch(url, data=new_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertTrue(response_data)
        self.assertEqual(response_data.get('id'), last_person.id)
        self.assertEqual(response_data.get('name'), new_name)

    def test_update_non_existent_person(self):
        url = reverse('person-detail', kwargs={'pk': 999})
        response = self.client.patch(url, data={'name': 'new_name'})
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        last_person = self.model.objects.last()
        self.assertTrue(last_person)
        url = reverse('person-detail', kwargs={'pk': last_person.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        person_exist = self.model.objects.filter(id=last_person.id).exists()
        self.assertFalse(person_exist)

    def test_delete_non_existent_person(self):
        url = reverse('person-detail', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
