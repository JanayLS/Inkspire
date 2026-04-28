from django.shortcuts import render, redirect, get_object_or_404
from .models import Artwork, Comment, Like
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from .models import Comment, Like
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from .models import Profile
from django.contrib.auth import login
from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Create or update profile
            profile = Profile.objects.get(user=user)
            profile.bio = form.cleaned_data.get('bio')
            if form.cleaned_data.get('profile_image'):
                profile.profile_image = form.cleaned_data.get('profile_image')
            profile.save()

            login(request, user)
            return redirect('gallery_feed')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')  # or 'gallery_feed'

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'gallery/edit_profile.html', {'form': form})


@staff_member_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()

    return JsonResponse({'success': True})


@staff_member_required
def delete_like(request, like_id):
    if request.method == 'POST':
        like = get_object_or_404(Like, id=like_id)
        artwork = like.artwork
        like.delete()

        return JsonResponse({
            'success': True,
            'likes_count': artwork.likes.count(),
            'artwork_id': artwork.id
        })

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.filter(user=user).first()
    artworks = Artwork.objects.filter(owner=user).order_by('-created_at')

    return render(request, 'gallery/profile.html', {
        'profile_user': user,
        'profile': profile,
        'artworks': artworks
    })

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    artworks = Artwork.objects.filter(owner=user).order_by('-created_at')

    return render(request, 'gallery/profile.html', {
        'profile_user': user,
        'artworks': artworks
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('gallery_feed')
    else:
        form = UserCreationForm()

    return render(request, 'gallery/register.html', {'form': form})

def gallery_feed(request):
    artworks = Artwork.objects.all().order_by('-created_at')
    return render(request, 'gallery/feed.html', {'artworks': artworks})


@login_required
def upload_artwork(request):
    if request.method == 'POST':
        Artwork.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
            owner=request.user  # ✅ FIXED
        )
        return redirect('gallery_feed')

    return render(request, 'gallery/upload.html')


@login_required
def add_comment(request, artwork_id):
    if request.method == 'POST':
        artwork = get_object_or_404(Artwork, id=artwork_id)

        comment = Comment.objects.create(
            artwork=artwork,
            user=request.user,
            text=request.POST.get('text')
        )

        return JsonResponse({
            'username': comment.user.username,
            'text': comment.text
        })


@login_required
def like_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)

    like, created = Like.objects.get_or_create(
        artwork=artwork,
        user=request.user
    )

    return JsonResponse({
        'likes_count': artwork.likes.count()
    })