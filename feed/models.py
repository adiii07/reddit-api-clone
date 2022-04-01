from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    body = models.CharField(max_length=20000)
    votes = models.IntegerField(default=0)


class Vote(models.Model):
    UPVOTE = 'U'
    DOWNVOTE = 'D'
    NEUTRAL = 'N'
    VOTE_OPTIONS = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]
    action_type = models.CharField(choices=VOTE_OPTIONS, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=5000)
    votes = models.IntegerField(default=0)
    