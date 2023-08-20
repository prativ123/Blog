from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

    

    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.FileField(upload_to='uploads', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_like')
    tags = TaggableManager(blank=True) 
    

    def __str__(self):
        return self.title
    
    def number_of_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        

    def __str__(self):
        return self.comment 