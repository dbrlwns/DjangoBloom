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

from post2.models import Blog2, HashTag


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
        # post가 DB에 저장되어 아이디가 생성된 후에 해시태그 추가가능
        post.save()
        # Hash Append Section
        tag_string = request.POST.get('tags').lower()
        if tag_string:
            tag_names = [tag_name.strip() for tag_name in tag_string.split(',')]
            for tag_name in tag_names:
                tag, _ = HashTag.objects.get_or_create(hash=tag_name)  # 2인자는 생성여부
                post.hashTag.add(tag)
        return redirect(f'/post2/newDetail/{post.id}/')
    else:
        form.add_error('None', "Error occured")



def new_detail(request, postId):

    post = get_object_or_404(Blog2, id=postId)
    context = { 'post' : post }
    return render(request, 'new_detail.html', context)



def new_list(request):
    posts = Blog2.objects.all()
    tags = HashTag.objects.all()
    context = { 'posts': posts, 'tags': tags }
    return render(request, 'new_list.html', context)

@require_POST
def new_delete(request, postId):
    post = get_object_or_404(Blog2, id=postId)
    if post.user == request.user:
        post.delete()
    return redirect('/post2/newList/')




#api Test
def api_new(request):
    blogs = Blog2.objects.all().values("id", "title", "pub_date")
    data = list(blogs)
    # safe=True는 “보안을 위해 JSON 최상위 객체가 dict만 되게 하겠다”는 의미
    return JsonResponse({'data': data}, safe=True)

def new_tag(request, tag_name):
    try:
        tag = get_object_or_404(HashTag, hash=tag_name)
    except HashTag.DoesNotExist:
        posts = Blog2.objects.none()
    else:
        # Blog들을 필터
        posts = Blog2.objects.filter(hashTag=tag)

    all_tags = HashTag.objects.all()
    context = {
        "tag_name": tag_name,
        "posts": posts,
        "all_tags": all_tags,
    }
    return render(request, "new_tag.html", context)



def postEdit(request, postId):
    post = get_object_or_404(Blog2, id=postId)

    # 현재 사용자가 블로그 작성을 하지 않았으면 접근 제한
    if request.user != post.user:
        return redirect('/post2/newList/')
    if request.method == "POST":
        form = BlogPost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save()
            # Hash Append Section
            tag_string = request.POST.get('tags').lower()
            updated_post.hashTag.clear() # 연결된 HashTag 끊고 새로 추가
            if tag_string:
                tag_names = [tag_name.strip() for tag_name in tag_string.split(',')]
                for tag_name in tag_names:
                    tag, _ = HashTag.objects.get_or_create(hash=tag_name)  # 2인자는 생성여부
                    post.hashTag.add(tag)
            return redirect(f'/post2/newDetail/{post.id}/')
    else:
        form = BlogPost(instance=post)
        tags = ', '.join(post.hashTag.values_list('hash', flat=True))
    context = {'form' : form, 'post': post, 'tags': tags}
    return render(request, 'newEdit.html', context)

