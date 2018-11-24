import os
import json
import datetime as dt
from django.conf import settings
from django.forms import widgets


MEDIA_URL = settings.MEDIA_URL


class ImagePILWidget(widgets.TextInput):
    template_name = 'djangomediapil/image_widget.html'

    def url(self, pathway):
        if pathway is None:
            return None
        return os.path.join(MEDIA_URL, pathway)

    def format_value(self, value):
        if type(value) == str:
            value = json.loads(value)
        value['url'] = self.url(value['pathway'])
        return value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        value = context['widget']['value']
        context['upload_to'] = os.path.join(value.get('upload_to', '.'),
                                            dt.datetime.now().strftime('%Y/%m-%d'))

        context['json'] = json.dumps(value, ensure_ascii=False)
        context['MEDIA_URL'] = MEDIA_URL
        return context

    class Media:
        css = {
            'all': ('djangomediapil/widget.css',)
        }
        js = ('djangomediapil/widget.js',)
