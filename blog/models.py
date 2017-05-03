from django.db import models

# Create your models here.
from django.utils import timezone

class Blog(models.Model):
    """
    Blog Model
    """
    title = models.CharField(max_length=200)            #title of the blog
    body = models.TextField()                           #description/text for the blog
    publish =models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)   #creation date
    modified = models.DateTimeField(auto_now_add=True)  #modified date

    def __str__(self):
        return self.title

    class Meta:
        verbose_name= "Blog Entry"
        verbose_name_plural = "Blog Entries"
        ordering = ["-created"]