from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce



class Author (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = Post.objects.filter(author = self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comment_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']

        print(post_rating)
        print('__________________')
        print(comment_rating)
        print('__________________')
        print(post_comment_rating)

        self.rating = post_rating * 3 + comment_rating + post_comment_rating
        self.save()
class Category (models.Model):

    category_name = models.CharField(max_length=50, unique = True)

class Post (models.Model):
    ARTICLE = 'artc'
    NEWS = 'news'

    TYPE = [
        (ARTICLE, 'Article'),
        (NEWS, 'News'),
    ]

    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    post_type = models.CharField(choices=TYPE, max_length=4, default='news')
    rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    category = models.ManyToManyField(Category, through = 'PostCategory')

    def preview(self):
        return f"{self.content[:124]}..."


    def like(self):
        self.rating += 1
        self.save()


    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory (models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)



class Comment (models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default=0)

    def like(self, ):
        self.rating += 1
        self.save()

    def dislike(self,):
        self.rating -= 1
        self.save()