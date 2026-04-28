from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Artwork, Comment, Like

class ProfileTest(TestCase):
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')

        self.assertTrue(Profile.objects.filter(user=user).exists())
        
class SignupTest(TestCase):
    def test_signup_creates_user(self):
        response = self.client.post('/accounts/signup/', {
            'username': 'newuser',
            'email': 'test@test.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
            
class LoginTest(TestCase):
    def test_login(self):
        User.objects.create_user(username='testuser', password='12345')

        response = self.client.login(username='testuser', password='12345')

        self.assertTrue(response)
        
class ArtworkTest(TestCase):
    def test_create_artwork(self):
        user = User.objects.create_user(username='artist', password='12345')

        artwork = Artwork.objects.create(
            owner=user,
            title="Test Art",
            description="Test",
            image="artworks/test.jpg"
        )

        self.assertEqual(artwork.title, "Test Art")
        self.assertEqual(artwork.owner.username, "artist")
        
class LikeTest(TestCase):
    def test_like_artwork(self):
        user = User.objects.create_user(username='user1', password='12345')
        artwork = Artwork.objects.create(
            owner=user,
            title="Art",
            description="Desc",
            image="artworks/test.jpg"
        )

        like = Like.objects.create(user=user, artwork=artwork)

        self.assertEqual(Like.objects.count(), 1)


class CommentTest(TestCase):
    def test_add_comment(self):
        user = User.objects.create_user(username='user1', password='12345')
        artwork = Artwork.objects.create(
            owner=user,
            title="Art",
            description="Desc",
            image="artworks/test.jpg"
        )

        comment = Comment.objects.create(
            user=user,
            artwork=artwork,
            text="Nice!"
        )

        self.assertEqual(comment.text, "Nice!")

class ViewTest(TestCase):
    def test_feed_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_like_api(self):
        user = User.objects.create_user(username='u', password='12345')
        self.client.login(username='u', password='12345')

        artwork = Artwork.objects.create(
            owner=user,
            title="Art",
            description="Desc",
            image="artworks/test.jpg"
        )

        response = self.client.post(f'/like/{artwork.id}/')
        self.assertEqual(response.status_code, 200)