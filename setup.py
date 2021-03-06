import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-media-pil',
    version='1.0.0',
    packages=['djangomediapil'],
    description='Simple widget for image manipulations by pillow in the Django Admin',
    include_package_data=True,
    long_description=README,
    author='Giorgi Kakulashvili',
    # author_email='yourname@example.com',
    url='https://github.com/giorgi94/django-media-pil',
    keywords=['django', 'pillow', 'mediamanager'],
    platforms=['OS Independent'],
    license='MIT',
    install_requires=[
        'Django>=2.1.0',
        'Pillow>=5.3.0',
        'pycrop>=1.0.1'
    ]
)
