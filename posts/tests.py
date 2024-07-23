from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase

class PostListViewsTest(APITestCase):
    # setUp method that will automatically  run before every test method in the class.
    def setUp(self):
        # create a user that we can reference  later on in all the tests 
        # We’ll also need this user when we manually  create a post and need to set its owner.
        User.objects.create_user(username='adamtest', password='pass')

    
    def test_can_list_posts(self):
        adam = User.objects.get(username='adamtest')
        Post.objects.create(owner=adam, title='a title')
        # want to test that can make a get request to ‘/posts’ to list all the posts
        # make test network requests by calling an appropriate method on self-dot-client,
        # namely self.client.get or .post, .put
        # followed by the url we’re making the request to (e.g. /posts/)
        response = self.client.get('/posts/')
        # make it fail by  asserting the status_code isn’t 200
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #adjust it so it will run ok 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        # to test protected routes, log in first using the  APITest client
        # pass in the  username and password from the setUp method
        self.client.login(username='adamtest', password='pass')
        response =self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        # make it fail
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # make it run
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_logged_out_user_can_create_post(self):
        #no user authentification needed
        response = self.client.post('/posts/', {'title': 'a title'})
        # make it fail
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # make it run
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)