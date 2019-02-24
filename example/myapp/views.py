from django.shortcuts import render

from .models import MyModel


def indexView(request):

    obj: MyModel = MyModel.objects.first()

    if obj is None:
        return render(request, "index.html", {})

    context = {
        'title': obj.title,
        'img': obj.image,
        'img_cover_300x200': obj.thumb((300, 200), 'cover'),
        'img_cover_h400': obj.thumb((None, 400), 'cover'),
        'img_cover_w200': obj.thumb((200, None), 'cover'),
        'img_contain_300x200': obj.thumb((300, 200), 'contain'),
    }

    return render(request, "index.html", context)
