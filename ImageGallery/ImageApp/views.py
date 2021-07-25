from io import StringIO
import io
from django.core.files.base import ContentFile
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import request
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.shortcuts import render
from.models import ImageUpload
from.forms import ImageForm


# Create your views here.


def imageView(request):
    # Show most common tags
    imgView = ImageUpload.objects.all()
    common_tags = ImageUpload.tags.most_common()[:4]
    form = ImageForm(request.POST, request.FILES,)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
    context = {
        'imgView': imgView,
        'common_tags': common_tags,
        'form': form,
    }
    return render(request, 'home.html', context)


def detail_view(request, slug):
    post = get_object_or_404(ImageUpload, slug=slug)

    context = {
        'post': post,
    }
    return render(request, 'detail.html', context)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    common_tags = ImageUpload.tags.most_common()[:4]
    pagelist = ImageUpload.objects.all()
    # paginator = Paginator(pagelist, 8)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    imgView = ImageUpload.objects.filter(tags=tag)
    context = {
        'pagelist': pagelist,
        # 'page_obj': page_obj,
        'tag': tag,
        'common_tags': common_tags,
        'imgView': imgView,
    }

    return render(request, 'home.html', context)


def listPage(request):
    pageList = ImageUpload.objects.all()
    # print(pageList)

    paginator = Paginator(pageList, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'allView.html', {'pageList': pageList, 'page_obj': page_obj, })


def rotateLeft(request, id=None):
    try:
        myModel = ImageUpload.objects.get(pk=id).first()
    except ImageUpload.DoesNotExist:
        myModel = None

    original_photo = StringIO(myModel.images.read())
    rotated_photo = StringIO()

    image = Image.open(original_photo)
    image = image.rotate(-90)
    image.save(rotated_photo, 'JPEG')

    rotimg = myModel.file.save(
        image.file.path, ContentFile(rotated_photo.getvalue()))
    rotimg.save()

    return render(request, 'rotete.html', {'rotimg': rotimg})


def rotateRight(request, id=None):
    try:
        myModel = ImageUpload.objects.get(pk=id).first()
    except ImageUpload.DoesNotExist:
        myModel = None

    original_photo = StringIO(myModel.file.read())
    rotated_photo = StringIO()

    image = Image.open(original_photo)
    image = image.rotate(+90)
    image.save(rotated_photo, 'JPEG')

    rotimg = myModel.file.save(
        image.file.path, ContentFile(rotated_photo.getvalue()))
    rotimg.save()

    return render(request, 'rotete.html', {'rotimg': rotimg})


# def imageView(request):
#     # Show most common tags
#     imgView = ImageUpload.objects.all()
#     common_tags = ImageUpload.tags.most_common()[:4]
#     paginator = Paginator(imgView, 8)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     form = ImageForm(request.POST, request.FILES,)
#     if form.is_valid():
#         newpost = form.save(commit=False)
#         newpost.slug = slugify(newpost.title)
#         newpost.save()
#         # Without this next line the tags won't be saved.
#         form.save_m2m()
#     context = {
#         'imgView': imgView,
#         'common_tags': common_tags,
#         'form': form,
#         'page_obj': page_obj
#     }
#     return render(request, 'home.html', context)
