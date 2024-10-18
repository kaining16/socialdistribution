from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

class Author(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='need.',
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': "already exists.",
        },
    )
    
    fqid = models.URLField(unique=True, blank=True, null=True)

    
    type = models.CharField(max_length=10, default="author")

    
    displayName = models.CharField(max_length=100)

    
    host = models.URLField()

    
    github = models.URLField(blank=True, null=True)

    
    profileImage = models.URLField(blank=True, null=True)

    
    page = models.URLField(blank=True, null=True)

    
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    def save(self, *args, **kwargs):
        
        if not self.pk:
            super().save(*args, **kwargs)

        
        if not self.fqid:
            self.fqid = f"{self.host}authors/{self.pk}"

            
            super().save(update_fields=['fqid'])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username  

    def add_follower(self, author):
       
        if author != self:
            self.followers.add(author)

    def remove_follower(self, author):
        
        self.followers.remove(author)

    def is_friend(self, author):
        
        return author in self.friends

    def add_friend(self, author):
        
        if author != self and author in self.followers and self in author.followers:
            self.friends.add(author)
            author.friends.add(self)

    def remove_friend(self, author):
       
        self.friends.remove(author)
        author.friends.remove(self)

from django.db import models
from django.contrib.auth import get_user_model



from django.db import models
from author.models import Author

class FollowRequest(models.Model):
    
    request_type = models.CharField(max_length=10, default="follow")

    
    summary = models.CharField(max_length=255)

    
    actor = models.ForeignKey(Author, related_name='follow_requests_sent', on_delete=models.CASCADE)

    
    object = models.ForeignKey(Author, related_name='follow_requests_received', on_delete=models.CASCADE)

   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor.displayName} wants to follow {self.object.displayName}"