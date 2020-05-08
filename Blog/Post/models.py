from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=130)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    slug=models.SlugField(unique=True)
    image=models.FileField(blank=True,null=True)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Post:retrieve',kwargs={"slug":self.slug})