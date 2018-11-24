import os
import glob
from django.conf import settings
from .imagePIL import assure_path_exists
from .mediaPIL import MediaPIL


class ImageUploadMixin:

    def upload_to(self, request):
        for key, file in request.FILES.items():
            upload_to = request.POST.get(key + '-upload_to')
            path = os.path.join(settings.MEDIA_ROOT, upload_to, file.name)

            assure_path_exists(path)

            with open(path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

    def save_model(self, request, obj, form, change):
        self.upload_to(request)
        super().save_model(request, obj, form, change)


class ImagePILMixin:

    @staticmethod
    def generatethumbs(image, sizes):
        if type(image) == str and '{' in image:
            image = eval(image)

        if image['pathway']:
            img = MediaPIL(**image)
            for m, s in sizes.items():
                for size in s:
                    img.get(m, size)

    @staticmethod
    def rmoldthumbs(image, sizes):
        if type(image) == str and '{' in image:
            image = eval(image)

        pathway = image['pathway']
        if pathway:
            for m, s in sizes.items():
                for size in s:
                    thumb = os.path.join(
                        MediaPIL.MEDIA_DIR, MediaPIL.reverse(
                            pathway, method="cover", size=size, point=(0, 0)))
                    for path in glob.glob(thumb.replace('__0x0', '__*x*')):
                        point = '__%dx%d' % tuple(image['point'])
                        if point not in path:
                            os.remove(path)
