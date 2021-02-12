from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth


# Create your views here.
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('duka')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')


    else:
        return render(request, 'duka/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken!')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken!')
                return redirect('register')

            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                password=password1, email=email)
                user.save()
                print('User created successfully:')
                return redirect('login')

        else:
            messages.info(request, 'Password must match!')
            return redirect('register')

    else:
        return render(request, 'duka/register.html')
