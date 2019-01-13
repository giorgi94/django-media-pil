import os
import json
from .imagePIL import (
    ImagePIL, normilize_size)
from django.conf import settings

BASE_DIR = settings.BASE_DIR
MEDIA_DIR = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL


def reverse(path, method, size, point=None):
    basename = os.path.basename(path)
    filename, ext = os.path.splitext(basename)
    path = path.replace(MEDIA_DIR, '')

    if not path.startswith('/'):
        path = '/' + path

    if point is None:
        point = (50, 50)

    path = os.path.dirname(path)
    point = "%dx%d" % point

    if None not in size:
        size = "w%dh%d" % size
    elif size[0] is None:
        size = "h%d" % size[1]
    else:
        size = "w%d" % size[0]

    return f'__thumbs__/{method}/{size}{path}/{filename}{ext}'


class MediaPIL(ImagePIL):

    BASE_DIR = BASE_DIR
    MEDIA_DIR = MEDIA_DIR
    MEDIA_URL = MEDIA_URL

    def __init__(self, pathway=None, point=(50, 50), quality=90, upload_to=".",
                 * args, **kwargs):
        self.pathway = pathway
        self.set_path(pathway)
        self.point = tuple(point)
        self.quality = quality
        self.upload_to = upload_to

    def set_path(self, pathway):
        if pathway:
            self.path = os.path.join(MEDIA_DIR, pathway)
        else:
            self.path = None

    @property
    def url(self):
        if self.pathway is None:
            return None
        return os.path.join(MEDIA_URL, self.pathway)

    def path_to_url(self, path):
        return os.path.join(MEDIA_URL, path.replace(MEDIA_DIR + '/', ''))

    @staticmethod
    def placeholder(size):
        return 'http://via.placeholder.com/%s' % size

    @staticmethod
    def reverse(path, method="cover", size="10x10", point=None):
        return reverse(path, method, size, point)

    def default_save_path(self, size, method, point=None):
        path = reverse(self.path, method, size, point)
        return os.path.join(MEDIA_DIR, path)

    def __setitem__(self, key, value):
        setattr(self, key, value)

        if key == 'pathway':
            self.set_path(value)

    def __getitem__(self, key):
        return getattr(self, key)

    def to_json(self):
        return {
            'pathway': self.pathway,
            'point': self.point,
            'quality': self.quality,
            'upload_to': self.upload_to,
        }

    def to_str(self):
        return json.dumps(self.to_json(), ensure_ascii=False)

    def get(self, method, *args, **kwargs):
        if self.pathway:
            overwrite = kwargs.get('overwrite', False)
            kwargs['overwrite'] = overwrite

            r = getattr(self, method)(*args, **kwargs)
            if r[0]:
                return self.path_to_url(r[1])
        return ""


if __name__ == '__main__':
    # from apps.pymedia.mediaPIL import MediaPIL
    img = MediaPIL('img.jpg')
    # img.contain((300, 230))
    # img.cover((300, 230), point=(50, 70))
    # print(getattr(img, 'path'))
