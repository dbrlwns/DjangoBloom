from django.shortcuts import render, redirect, get_object_or_404

from post3.forms import ContentForm
from post3.models import Content, Comment


# Create your views here.
def post3_page(request):
    if request.method == "POST":
        if "content_register" in request.POST:
            form = ContentForm(request.POST)
            content = form.save(commit=False)
            content.user = request.user
            content.save()
            return redirect('/post3/')
        elif "content_delete" in request.POST:
            content = get_object_or_404(Content, id=request.POST["contentId"])
            content.delete()
            return redirect('/post3/')
        elif "comment_register" in request.POST:
            if not request.POST["contentId"] and not request.POST["comment"]: return redirect("/post3/")
            comment = Comment.objects.create(
                user=request.user,
                content=Content.objects.get(id=request.POST["contentId"]),
                comment=request.POST["comment"]
            )
        elif "comment_delete" in request.POST:
            comment = get_object_or_404(Comment, id=request.POST["commentId"])
            comment.delete()
        return redirect(f'/post3/?open={request.POST["contentId"]}')
    else:
        contents = Content.objects.all()
        form = ContentForm()
        context = {'contents': contents,
                   'form' : form }
        return render(request, "post3.html", context)
