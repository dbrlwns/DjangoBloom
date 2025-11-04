from django.shortcuts import render

from post2.models import Blog2
from posts.models import Post


def index(request):
    # 메인 포스트는 blog의 글 하나를 선택해서 가져오기
    main_post = Blog2.objects.get(id=11)
    side_posts = Post.objects.all()
    context = {"main_post": main_post, "side_posts": side_posts}
    return render(request, 'base.html', context)