from email.policy import default
from django.conf import settings
from django.db import models
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    rating=models.FloatField(default=0.0)
    def update_rating(self):
        result1=sum(post.rating*3 for post in self.posts.all())
        result2 = sum(comment.rating  for comment in self.user.comments.all())
        result3= sum(comment.rating for post in self.posts.all()
        for comment in post.comments.all())
        self.rating=result1+result2+result3
        self.save(update_fields=['rating'])

class Category(models.Model):
    topic=models.CharField(unique = True)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='subscribed_categories',
        blank=True,
        verbose_name='Подписчики',
    )
    def __str__(self):
        return self.name

class Post(models.Model):

    author = models.ForeignKey(
        'Author',on_delete=models.CASCADE,
        related_name='posts')

    class PostType(models.TextChoices):
        ARTICLE = 'AR', 'Статья'
        NEWS = 'NW', 'Новость'

    post_type = models.CharField(
        max_length=2,
        choices=PostType.choices
    )
    time_add=models.DateTimeField(auto_now_add=True)
    categories=models.ManyToManyField('Category', related_name='posts')
    title=models.CharField(max_length=200)
    text=models.TextField()
    rating=models.FloatField(default=0.0)
    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()
    def preview(self, leight=124):
        if len(self.text)<leight:
            return self.text
        else:
            return self.text[:leight]+ '...'

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.id])


class PostCategory(models.Model):
    post=models.ForeignKey('Post',on_delete=models.CASCADE)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
class Comment(models.Model):
    post = models.ForeignKey('Post',on_delete=models.CASCADE)
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments')
    text=models.TextField()
    time=models.DateTimeField(auto_now_add=True)
    rating=models.FloatField(default=0.0)
    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()





