from django.urls import include, path, re_path
from . import views

app_name = 'myapp'


urlpatterns = [
    path('', views.indexView)
]