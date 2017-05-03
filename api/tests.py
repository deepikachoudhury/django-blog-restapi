from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Blog
from api.serializers import BlogSerializer
import json
from django.core.management import call_command

class TestRestApiBlog(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/blogs/'
        call_command('loaddata', 'fixtures/blog_fixtures.json', verbosity=0)
        self.blog = Blog.objects.order_by('id')[0]

    def test_get_blog_list(self):
        """
        Testcase to test GET method to get all blog list
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_a_blog_detail(self):
        """
        Testcase to test GET method to get all blog list
        """
        geturl = '%s%d' % (self.url, self.blog.id)
        response = self.client.get(geturl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_bolg(self):
        """
        Testcase to test POST / CREATE a blog
        """
        #input dict to test the POST
        input_data = dict()
        input_data['title'] = "test post"
        input_data['body'] = "checking post"
        input_data['publish'] = True
        response=self.client.post(self.url,data=json.dumps(input_data),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('title',response.json())
        data=response.json()
        self.assertEqual(data['title'],input_data['title'])

    def test_put_or_update_existing_blog(self):
        """
            Testcase to test PUT / UPDATE a existing blog
        """
        # input dict to test the POST
        input_data = BlogSerializer(self.blog).data
        input_data.update({"title":"changed"})
        puturl='%s%d'%(self.url,self.blog.id)
        response = self.client.put(puturl, data=json.dumps(input_data), content_type='application/json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.json())

        self.assertEqual(data['title'], input_data['title'])

    def test_put_or_update_non_existing_blog(self):
        """
            Testcase to test PUT / UPDATE a non existing blog
        """
        # input dict to test the POST
        input_data = BlogSerializer(self.blog).data
        input_data.update({"title": "changed"})
        puturl = '%s%d' % (self.url, 200)
        response = self.client.put(puturl, data=json.dumps(input_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_or_update_blog_invalid_input_format(self):
        """
            Testcase to test PUT / UPDATE
            input is not in proper json format
        """
        # input dict to test the POST
        input_data = BlogSerializer(self.blog).data
        input_data.update({'title': 'changed'})
        puturl = '%s%d' % (self.url, self.blog.id)
        response = self.client.put(puturl, data=input_data, content_type='application/json')
        #data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_existing_blog(self):
        """
        Testcase to "DELETE" a blog detail through REST
        """
        deleteurl = '%s%d' % (self.url, self.blog.id)
        response = self.client.delete(deleteurl)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_blog_not_exist(self):
        """
        Testcase to delete a blog which is not exist in Database
        """
        deleteurl = '%s%d' % (self.url, 200)
        response = self.client.delete(deleteurl)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)