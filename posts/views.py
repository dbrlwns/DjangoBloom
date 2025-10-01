from dataclasses import field
from xml.dom import ValidationErr

from django.db import transaction
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from posts.forms import PostAddForm, PostImageForm, CommentForm
from posts.models import Post, PostImage

from django.shortcuts import redirect

# Create your views here.
def show_posts(request):
    posts = Post.objects.all()
    context = {"posts" : posts}
    return render(request, "posts.html", context)


def post_delete(request, postId):
    post = get_object_or_404(Post, id=postId)
    post.delete()
    return redirect('/posts/')


def post_detail(request, postId):
    context = {}
    post = get_object_or_404(Post, id=postId)
    if request.method == "POST":
        if "update_post" in request.POST:
            form = PostAddForm(request.POST, instance=post)
            if form.is_valid():
                post.save() # Django가 instance의 field 값을 cleaned_data 값으로 업데이트
                return redirect(f'/posts/{post.id}/')
        elif "add_comment" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect(f'/posts/{post.id}/')
    else:
        form = PostAddForm(instance=post)
        comment = CommentForm()
        context = {"post" : post, 'form': form, 'comment': comment}
    return render(request, "postDetail.html", context)


def post_add(request):
    if request.method == "POST":
        form = PostAddForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if not images:
            form.add_error(None, "이미지는 최소 1개 이상 첨부해야합니다.")
        if form.is_valid():
            try:
                with transaction.atomic(): # 하나라도 실패시 롤백(DB저장X)
                    post = form.save(commit=False)  # 인스턴스만 생성
                    post.user = request.user    # post field 모두 채우기
                    post.save() # DB에 저장

                    for image in images:
                        post_image = PostImage(post=post, image=image)
                        post_image.full_clean() # model validator 실행(검증)
                        post_image.save()
                return redirect(f'/posts/{post.id}')
            except ValidationError as err:
                # 에러 메시지 템플릿에 노출
                form.add_error(None, f"{err}")
                # 오류 발생시 transaction으로 저장된 post를 롤백

    else:
        form = PostAddForm()
    return render(request, "postAdd.html",{'form' : form})
















