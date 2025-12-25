from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Profile, Post, Discussion, Comment, Fanfic
from .forms import (
    CustomUserCreationForm, ProfileForm, PostForm,
    DiscussionForm, CommentForm, FanficForm
)


def home(request):
    """Главная страница"""
    posts = Post.objects.all()[:6]
    discussions = Discussion.objects.all()[:6]
    fanfics = Fanfic.objects.all()[:6]
    
    context = {
        'posts': posts,
        'discussions': discussions,
        'fanfics': fanfics,
    }
    return render(request, 'fandom/home.html', context)


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаем профиль для нового пользователя
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'fandom/register.html', {'form': form})


@login_required
def profile_view(request, username):
    """Просмотр профиля пользователя"""
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=user)
    discussions = Discussion.objects.filter(author=user)
    fanfics = Fanfic.objects.filter(author=user)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'discussions': discussions,
        'fanfics': fanfics,
    }
    return render(request, 'fandom/profile.html', context)


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'fandom/profile_edit.html', {'form': form})


# Посты
def post_list(request):
    """Список всех постов"""
    posts = Post.objects.all()
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'fandom/post_list.html', {'page_obj': page_obj})


def post_detail(request, pk):
    """Детали поста"""
    post = get_object_or_404(Post, pk=pk)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(id=request.user.id).exists()
    
    return render(request, 'fandom/post_detail.html', {
        'post': post,
        'is_liked': is_liked,
    })


@login_required
def post_create(request):
    """Создание поста"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост успешно создан!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'fandom/post_form.html', {'form': form, 'title': 'Создать пост'})


@login_required
def post_edit(request, pk):
    """Редактирование поста"""
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        messages.error(request, 'Вы не можете редактировать этот пост!')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно обновлен!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'fandom/post_form.html', {'form': form, 'title': 'Редактировать пост', 'post': post})


@login_required
def post_delete(request, pk):
    """Удаление поста"""
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        messages.error(request, 'Вы не можете удалить этот пост!')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост успешно удален!')
        return redirect('post_list')
    
    return render(request, 'fandom/post_confirm_delete.html', {'post': post})


@login_required
def post_like(request, pk):
    """Лайк/дизлайк поста"""
    post = get_object_or_404(Post, pk=pk)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        messages.info(request, 'Лайк убран')
    else:
        post.likes.add(request.user)
        messages.success(request, 'Пост понравился!')
    
    return redirect('post_detail', pk=pk)


# Обсуждения
def discussion_list(request):
    """Список всех обсуждений"""
    discussions = Discussion.objects.all()
    paginator = Paginator(discussions, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'fandom/discussion_list.html', {'page_obj': page_obj})


def discussion_detail(request, pk):
    """Детали обсуждения"""
    discussion = get_object_or_404(Discussion, pk=pk)
    discussion.views += 1
    discussion.save(update_fields=['views'])
    
    comments = discussion.comments.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('discussion_detail', pk=pk)
    else:
        form = CommentForm()
    
    return render(request, 'fandom/discussion_detail.html', {
        'discussion': discussion,
        'comments': comments,
        'form': form,
    })


@login_required
def discussion_create(request):
    """Создание обсуждения"""
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            messages.success(request, 'Обсуждение успешно создано!')
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm()
    
    return render(request, 'fandom/discussion_form.html', {'form': form, 'title': 'Создать обсуждение'})


@login_required
def discussion_edit(request, pk):
    """Редактирование обсуждения"""
    discussion = get_object_or_404(Discussion, pk=pk)
    
    if discussion.author != request.user:
        messages.error(request, 'Вы не можете редактировать это обсуждение!')
        return redirect('discussion_detail', pk=pk)
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Обсуждение успешно обновлено!')
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm(instance=discussion)
    
    return render(request, 'fandom/discussion_form.html', {
        'form': form,
        'title': 'Редактировать обсуждение',
        'discussion': discussion,
    })


@login_required
def discussion_delete(request, pk):
    """Удаление обсуждения"""
    discussion = get_object_or_404(Discussion, pk=pk)
    
    if discussion.author != request.user:
        messages.error(request, 'Вы не можете удалить это обсуждение!')
        return redirect('discussion_detail', pk=pk)
    
    if request.method == 'POST':
        discussion.delete()
        messages.success(request, 'Обсуждение успешно удалено!')
        return redirect('discussion_list')
    
    return render(request, 'fandom/discussion_confirm_delete.html', {'discussion': discussion})


# Фанфики
def fanfic_list(request):
    """Список всех фанфиков"""
    fanfics = Fanfic.objects.all()
    genre = request.GET.get('genre')
    rating = request.GET.get('rating')
    search = request.GET.get('search')
    
    if genre:
        fanfics = fanfics.filter(genre=genre)
    if rating:
        fanfics = fanfics.filter(rating=rating)
    if search:
        fanfics = fanfics.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    paginator = Paginator(fanfics, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'fandom/fanfic_list.html', {
        'page_obj': page_obj,
        'genres': Fanfic.GENRE_CHOICES,
        'ratings': Fanfic.RATING_CHOICES,
    })


def fanfic_detail(request, pk):
    """Детали фанфика"""
    fanfic = get_object_or_404(Fanfic, pk=pk)
    fanfic.views += 1
    fanfic.save(update_fields=['views'])
    
    is_liked = False
    if request.user.is_authenticated:
        is_liked = fanfic.likes.filter(id=request.user.id).exists()
    
    return render(request, 'fandom/fanfic_detail.html', {
        'fanfic': fanfic,
        'is_liked': is_liked,
    })


@login_required
def fanfic_create(request):
    """Создание фанфика"""
    if request.method == 'POST':
        form = FanficForm(request.POST, request.FILES)
        if form.is_valid():
            fanfic = form.save(commit=False)
            fanfic.author = request.user
            fanfic.save()
            messages.success(request, 'Фанфик успешно создан!')
            return redirect('fanfic_detail', pk=fanfic.pk)
    else:
        form = FanficForm()
    
    return render(request, 'fandom/fanfic_form.html', {'form': form, 'title': 'Создать фанфик'})


@login_required
def fanfic_edit(request, pk):
    """Редактирование фанфика"""
    fanfic = get_object_or_404(Fanfic, pk=pk)
    
    if fanfic.author != request.user:
        messages.error(request, 'Вы не можете редактировать этот фанфик!')
        return redirect('fanfic_detail', pk=pk)
    
    if request.method == 'POST':
        form = FanficForm(request.POST, request.FILES, instance=fanfic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фанфик успешно обновлен!')
            return redirect('fanfic_detail', pk=fanfic.pk)
    else:
        form = FanficForm(instance=fanfic)
    
    return render(request, 'fandom/fanfic_form.html', {
        'form': form,
        'title': 'Редактировать фанфик',
        'fanfic': fanfic,
    })


@login_required
def fanfic_delete(request, pk):
    """Удаление фанфика"""
    fanfic = get_object_or_404(Fanfic, pk=pk)
    
    if fanfic.author != request.user:
        messages.error(request, 'Вы не можете удалить этот фанфик!')
        return redirect('fanfic_detail', pk=pk)
    
    if request.method == 'POST':
        fanfic.delete()
        messages.success(request, 'Фанфик успешно удален!')
        return redirect('fanfic_list')
    
    return render(request, 'fandom/fanfic_confirm_delete.html', {'fanfic': fanfic})


@login_required
def fanfic_like(request, pk):
    """Лайк/дизлайк фанфика"""
    fanfic = get_object_or_404(Fanfic, pk=pk)
    
    if fanfic.likes.filter(id=request.user.id).exists():
        fanfic.likes.remove(request.user)
        messages.info(request, 'Лайк убран')
    else:
        fanfic.likes.add(request.user)
        messages.success(request, 'Фанфик понравился!')
    
    return redirect('fanfic_detail', pk=pk)

