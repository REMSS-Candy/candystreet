from django.http import HttpResponse

from os import listdir
from os.path import dirname


def index(request):
    return HttpResponse("Hello world!")


path = dirname(__file__)
files = listdir(path)

__all__ = [
    file[:-3] for file in files
    if file.endswith(".py") and not file.startswith("_")
]

from . import *

del listdir, dirname, path, files
