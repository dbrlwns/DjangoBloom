from dataclasses import field
from xml.dom import ValidationErr

from django.db import transaction
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from posts.forms import PostAddForm, PostImageForm, CommentForm, PostImageFormSet
from posts.models import Post, PostImage, Comment

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
    ImageFormSet = PostImageFormSet
    if request.method == "POST":
        if "update_post" in request.POST:
            form = PostAddForm(request.POST, instance=post)
            formset = ImageFormSet(request.POST, request.FILES, instance=post)
            print("formset_is_valid : ", formset.is_valid())
            if form.is_valid() and formset.is_valid():
                formset.save()  # image 수정을 위한 새로운 form 추가
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
        formset = ImageFormSet(instance=post)
        comment = CommentForm()
        context = {"post" : post, 'form': form, 'comment': comment
                   , 'formset' : formset}

    return render(request, "postDetail.html", context)




# 2. post_update에 image 추가하는 것도 만들기.
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
                form.add_error(None, f": {err}")
                # 오류 발생시 transaction으로 저장된 post를 롤백
    else:
        form = PostAddForm()
    return render(request, "postAdd.html",{'form' : form})

@require_POST
def comment_delete(request, postId, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
        return redirect(f'/posts/{postId}/')
    else: return redirect(f'/posts/{postId}/')
















