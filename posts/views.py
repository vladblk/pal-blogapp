from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from posts.forms import PostForm
from posts.models import Post, Topic
from comments.models import Comment

# Create your views here.

def index(request):

    if request.GET.get('q') == None:
        query = ''
    else:
        query = request.GET.get('q')

    topics = Topic.objects.all()
    posts = Post.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(comment__body__icontains=query) |
        Q(user__username__icontains=query)
    ).order_by('-created')

    posts_count = posts.count()

    context = {
        'posts': posts,
        'topics': topics,
        'posts_count': posts_count,
    }

    return render(request, 'posts/home.html', context)


def post(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comment_set.all().order_by('-created') # get the comments from each post
    comments_count = post.comment_set.all().count()

    if request.method == 'POST':
        Comment.objects.create(
            user = request.user,
            post = post,
            body = request.POST.get('comment')
        )

        messages.success(request, 'Successfully added your new comment!')

        return redirect('posts:post', pk=post.id)

    context = {
        'post': post,
        'comments': comments,
        'comments_count': comments_count,
    }

    return render(request, 'posts/post.html', context)


@login_required(login_url='user:sign-in')
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            post.save()

            messages.success(request, 'Successfully created your new post!')

            return redirect('posts:index')
        else:
            messages.error(request, 'Something went wrong...')


    context = {
        'form': form
    }

    return render(request, 'posts/post_form.html', context)


@login_required(login_url='user:sign-in')
def update_post(request, pk):
    post = None
    form = None
    try:
        post = Post.objects.get(id=pk)
        form = PostForm(instance=post) # get the instance of the specific post - prefill the inputs in the form

        if request.user != post.user:
            messages.error(request, 'Oops! Something went wrong...', extra_tags='danger')
            return redirect('posts:index')

        if request.method == 'POST':
            form = PostForm(request.POST, instance=post) # if instance is not specified here again, it will create a new post instead of updating
            next = request.POST.get('next', '/')

            if form.is_valid():
                form.save()

                messages.success(request, 'Successfully updated your post!')

                return HttpResponseRedirect(next)
            else:
                messages.error(request, 'Something went wrong...')
    except Post.DoesNotExist:
        messages.error(request, 'Oops! Something went wrong...', extra_tags='danger')
        return redirect('posts:index')


    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'posts/post_form.html', context)


@login_required(login_url='user:sign-in')
def delete_post(request, pk):
    post = None
    try:
        post = Post.objects.get(id=pk)

        if request.user != post.user:
            messages.error(request, 'Oops! Something went wrong...', extra_tags='danger')
            return redirect('posts:index')

        if request.method == 'POST':
            post.delete()

            messages.success(request, 'Successfully deleted your post!')

            return redirect('posts:index')

    except Post.DoesNotExist:
        messages.error(request, 'Oops! Something went wrong...', extra_tags='danger')
        return redirect('posts:index')

    context = {
        'to_delete': post
    }

    return render(request, 'delete.html', context)