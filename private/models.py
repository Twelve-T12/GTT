from django.db import models

# Create your models here.

class Black_List(models.Model):
    username = models.CharField(max_length=1000,blank=True,null=True)
    reason = models.TextField(blank=True,null=True)

    def __str__(self):
        return str(self.username)