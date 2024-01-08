from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm


def login_view(request):
    # Проверка, аутентифицирован ли пользователь
    if request.user.is_authenticated:
        return redirect('home')  # Перенаправляем на главную страницу

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Сообщение об ошибке, если вход не удался
                messages.error(request, 'Неправильный логин или пароль.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует.')
            else:
                form.save()
                messages.success(request, 'Учетная запись успешно создана.')
                return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
