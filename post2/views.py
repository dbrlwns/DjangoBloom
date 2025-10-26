import os

from django.contrib.auth.models import AnonymousUser
from django.core.files.storage import default_storage
from django.core.files.storage.filesystem import FileSystemStorage
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from DjangoBloom import settings
from post2.forms import BlogPost

from post2.models import Blog2


# Create your views here.

def default_view(request):

    if not request.user.is_authenticated:
        return redirect('/users/login/')


    form = BlogPost()
    context = {'form' : form}
    return render(request, 'new.html', context)

# tinyMCE view
@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        upload = request.FILES.get("file")
        fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'uploads')
        if not os.path.exists(fs.location): os.makedirs(fs.location, exist_ok=True)
        filename = fs.save(upload.name, upload)
        file_url = settings.MEDIA_URL + 'uploads/' + filename
        return JsonResponse({"location": file_url}) # mce key
    return JsonResponse({"error": "Invalid request"}, status=400)


@require_POST
def create_post(request):
    form = BlogPost(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect(f'/post2/newDetail/{post.id}/')
    else:
        form.add_error('None', "Error occured")



def new_detail(request, postId):

    post = get_object_or_404(Blog2, id=postId)
    context = { 'post' : post }
    return render(request, 'new_detail.html', context)



def new_list(request):
    posts = Blog2.objects.all()
    context = { 'posts': posts }
    return render(request, 'new_list.html', context)

@require_POST
def new_delete(request, postId):
    post = get_object_or_404(Blog2, id=postId)
    if post.user == request.user:
        post.delete()
    return redirect('/post2/newList/')










