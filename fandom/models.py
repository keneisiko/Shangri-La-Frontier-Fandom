from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Profile(models.Model):
    """Расширенный профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    favorite_character = models.CharField(max_length=100, blank=True, verbose_name='Любимый персонаж')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Профиль {self.user.username}'


class Post(models.Model):
    """Посты пользователей"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, verbose_name='Лайки')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()


class Discussion(models.Model):
    """Обсуждения"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Обсуждение'
        verbose_name_plural = 'Обсуждения'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('discussion_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """Комментарии к обсуждениям"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments', verbose_name='Обсуждение')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.discussion.title}'


class Fanfic(models.Model):
    """Фанфики по вселенной Рубеж Шангрила"""
    RATING_CHOICES = [
        ('G', 'G - Для всех'),
        ('PG', 'PG - Детям рекомендуется просмотр с родителями'),
        ('PG-13', 'PG-13 - Детям до 13 лет просмотр нежелателен'),
        ('R', 'R - Лицам до 17 лет обязательно присутствие взрослого'),
        ('NC-17', 'NC-17 - Лицам до 17 лет просмотр запрещен'),
    ]

    GENRE_CHOICES = [
        ('romance', 'Романтика'),
        ('adventure', 'Приключения'),
        ('drama', 'Драма'),
        ('action', 'Экшн'),
        ('fantasy', 'Фэнтези'),
        ('mystery', 'Мистика'),
        ('comedy', 'Комедия'),
        ('angst', 'Ангст'),
        ('fluff', 'Флафф'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fanfics', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    content = models.TextField(verbose_name='Содержание')
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, default='PG-13', verbose_name='Рейтинг')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, verbose_name='Жанр')
    cover = models.ImageField(upload_to='fanfics/', blank=True, null=True, verbose_name='Обложка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    likes = models.ManyToManyField(User, related_name='liked_fanfics', blank=True, verbose_name='Лайки')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Фанфик'
        verbose_name_plural = 'Фанфики'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('fanfic_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    def get_rating_display_short(self):
        return dict(self.RATING_CHOICES).get(self.rating, self.rating)

    def get_genre_display_short(self):
        return dict(self.GENRE_CHOICES).get(self.genre, self.genre)

