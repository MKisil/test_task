from rest_framework.test import APITestCase
from rest_framework import status

class FileSystemAPITest(APITestCase):

    def test_create_and_read_file(self):
        response = self.client.post('/files/', {
            'name': 'test.txt',
            'content': 'Hello world'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/files/test.txt/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Hello world')

    def test_update_file(self):
        self.client.post('/files/', {
            'name': 'update.txt',
            'content': 'Original'
        }, format='json')

        response = self.client.put('/files/update.txt/', {
            'content': 'Updated'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/files/update.txt/')
        self.assertEqual(response.data['content'], 'Updated')

    def test_delete_file(self):
        self.client.post('/files/', {
            'name': 'delete.txt',
        }, format='json')

        response = self.client.delete('/files/delete.txt/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/files/delete.txt/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

