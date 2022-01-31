from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from posts import forms
from .models import Comment
from .forms import CommentForm
from posts.models import Post
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@login_required(login_url='user:sign-in')
def update_comment(request, pk):
    comment = None
    form = None
    try:
        comment = Comment.objects.get(id=pk)
        form = CommentForm(instance=comment)

        if request.user != comment.user:
            messages.error(request, 'Oops! Something went wrong...', extra_tags="danger")
            return redirect('posts:index')
            

        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            next = request.POST.get('next', '/')

            if form.is_valid():
                form.save()

                messages.success(request, 'Successfully updated your comment!')

                return HttpResponseRedirect(next)
            else:
                messages.error(request, 'Something went wrong...')
    except Comment.DoesNotExist:
        messages.error(request, 'Oops! Something went wrong...', extra_tags="danger")
        return redirect('posts:index')

    context = {
        'comment': comment,
        'form': form
    }

    return render(request, 'comments/comment_form.html', context)


@login_required(login_url='user:sign-in')
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(id=pk)

        if request.user != comment.user:
            messages.error(request, 'Oops! Something went wrong...', extra_tags="danger")
            return redirect('posts:index')

        if request.method == 'POST':
            next = request.POST.get('next', '/')
            comment.delete()

            messages.success(request, 'Successfully deleted your comment!')

            return HttpResponseRedirect(next)
    except Comment.DoesNotExist:
        comment = ""
        messages.error(request, 'Oops! Something went wrong...', extra_tags="danger")
        return redirect('posts:index')

    context = {
        'to_delete': comment
    }

    return render(request, 'delete.html', context)