from django.shortcuts import render, get_object_or_404

from post2.models import Blog2, HashTag
from post3.models import Content
from posts.models import Post


def index(request):
    # 메인 포스트는 blog의 글 하나(tag=main)를 선택해서 가져오기
    main_post = Blog2.objects.filter(hashTag__hash="main").first()
    # main_post = Blog2.objects.get(hashTag=tag)
    side_posts = Post.objects.all()[:6] # 6개까지만
    queries = Content.objects.all()[:10]
    context = {"main_post": main_post, "side_posts": side_posts,
               "queries": queries}
    return render(request, 'base.html', context)