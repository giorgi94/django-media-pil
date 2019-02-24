from django.db import models
from djangomediapil.mediaPIL import MediaPIL
from djangomediapil.fields import ImagePILField


class MyModel(models.Model):
    title = models.CharField(max_length=50)
    image = ImagePILField()

    def thumb(self, size, method):
        img = MediaPIL(**self.image)
        return img.get(method, size=size, overwrite=True)

    def __str__(self):
        return self.title
