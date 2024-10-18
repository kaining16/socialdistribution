from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

class Author(AbstractUser):
    "username, fqid, host are necessary and can not be change"
    username = models.CharField(
        primary_key=True,
        max_length=150,
        unique=True,
        help_text='need.',
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': "already exists.",
        },
    )
    #fqid will be generated automatically using host and primary key, and once generated it can not be modify.
    fqid = models.URLField(unique=True, blank=True, null=True)
    #type
    type = models.CharField(max_length=10, default="author")
    #default set to username 
    displayName = models.CharField(max_length=10, blank=True)
    #used to generate fqid, can not be null
    host = models.URLField()
    #github link
    github = models.URLField(blank=True, null=True)
    #image link
    profileImage = models.URLField(blank=True, null=True)
    #page link
    page = models.URLField(blank=True, null=True)

    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    def save(self, *args, **kwargs):
        #generate fqid
        if not self.fqid:
            self.fqid = f"{self.host}authors/{self.username}"
        #set default display name to username
        if not self.displayName:
            self.displayName = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fqid

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