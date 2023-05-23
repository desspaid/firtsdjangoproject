from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.SmallIntegerField(default = 0)
    
    def __str__(self):
        return f"{self.user}"
    
    def update_rating(self):
        posts_rating = self.posts.aggregate(result = Sum('rating')).get('result')
        comments_rating = self.user.comments.aggregate(result = Sum('rating')).get('rating')
        print(f"... {self.user}: обновляем рейтинг автора ...")
        print(f"Рейтинг постов = {posts_rating}")
        print(f"Рейтинг комментариев = {comments_rating}")
        self.rating = 3 * posts_rating + comments_rating
        self.save()
        print(f"Рейтинг = 3 * {posts_rating} + {comments_rating} = {self.rating}")

class Category(models.Model):
    name = models.CharField(unique = True, max_length = 128)

    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name = 'posts')
    date_time = models.DateTimeField(auto_now_add = True)
    post_type = models.CharField(max_length = 2, choices = CATEGORY_CHOICES, default = ARTICLE)
    category = models.ManyToManyField(Category, through = "PostCategory")
    title = models.CharField(max_length = 128)
    text = models.TextField()
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
    
    def preview(self, length = 124) -> str:
        return f"{self.text[:length]}..." if len(self.text) > length else self.text

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add = True)

