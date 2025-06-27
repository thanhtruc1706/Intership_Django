from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm

class PostFormTest(TestCase):
    def test_post_form_valid(self):
        form = PostForm(data={'title': 'Test title', 'content': 'Test content'})
        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        form = PostForm(data={'title': '', 'content': ''})
        self.assertFalse(form.is_valid())

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_create_view_login_required(self):
        response = self.client.get(reverse('post_create'))
        self.assertNotEqual(response.status_code, 200)  # Redirect to login
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post_create'), {'title': 'New Post', 'content': 'New Content'})
        self.assertEqual(Post.objects.count(), 2)
        self.assertRedirects(response, reverse('post_detail', args=[2]))

    def test_post_edit_only_author(self):
        other_user = User.objects.create_user(username='other', password='otherpass')
        self.client.login(username='other', password='otherpass')
        response = self.client.get(reverse('post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 404)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('post_edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_delete_only_author(self):
        other_user = User.objects.create_user(username='other2', password='otherpass2')
        self.client.login(username='other2', password='otherpass2')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(Post.objects.count(), 1)
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(Post.objects.count(), 0) 