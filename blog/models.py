from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField( max_length=150)
    desc=models.TextField()
   
    file_name = models.CharField( max_length=150)
    my_file = models.FileField(upload_to='')
    # author=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name 