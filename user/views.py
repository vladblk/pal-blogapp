from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def sign_up(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False) # save the form but don't commit to DB

            new_user.username = new_user.username.lower()
            new_user.save()

            login(request, new_user)

            messages.success(request, 'Successfully created your account!')

            return redirect('posts:index')
        else:
            messages.error(request, 'Oops! Something went wrong...', extra_tags='danger')

    context = {
        'form': form
    }

    return render(request, 'user/signup.html', context)


def sign_in(request):

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            print('User does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, f'Welcome back, {username}!')

            return redirect('posts:index')
        else:
            messages.error(request, 'Oops! Something went wrong...', extra_tags='danger')

    return render(request, 'user/signin.html')


def log_out(request):
    if request.user.is_authenticated:
        logout(request)

        messages.success(request, 'Successfully logged  you out! See you soon.')

        return redirect('posts:index')
    else:
        return redirect('user:sign-in')