from django.db import models

from djangomediapil.fields import ImagePILField



class MyModel(models.Model):
    title = models.CharField(max_length=50)
    image = ImagePILField()

    def __str__(self):
        return self.title
