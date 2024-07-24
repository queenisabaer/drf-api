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

class PostDetailTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        #create 1 post for each user
        Post.objects.create(
            owner=adam, title='a title', content='adams content'
        )
        Post.objects.create(
            owner=brian, title='another title', content='brians content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        # Let’s assert the fetched post’s title is appropriate, and set the status to 200.
        self.assertEqual(response.data['title'], 'a title')
        # make it fail
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # make it run
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        # fetch that post from the database by ID
        post = Post.objects.filter(pk=1).first()
        # test that the change to the post title has been persisted
        self.assertEqual(post.title, 'a new title')
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)