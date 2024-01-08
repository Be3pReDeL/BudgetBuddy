from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')  # Вернуться на домашнюю страницу или другую страницу
    else:
        form = ExpenseForm()
    return render(request, 'finance/add_expense.html', {'form': form})


def home(request):
    return render(request, 'finance/home.html')


def about(request):
    return render(request, 'finance/about.html')
