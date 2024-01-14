from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import DateField
from django.db.models.functions import TruncDate
from django.db.models import Sum


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')  # Redirect to home after successful submission
    else:
        form = ExpenseForm()

    # If the form is not valid or it's a GET request, render home.html with the form
    expenses_by_date = Expense.objects.filter(user=request.user).order_by('date').values('date').distinct()
    context = {
        'expenses_by_date': expenses_by_date,
        'form': form,
    }
    return render(request, 'finance/home.html', context)


def home(request):
    # Получить уникальные даты из временных меток трат пользователя
    unique_dates = Expense.objects.filter(user=request.user).values('date').distinct()

    # Получить траты пользователя, сгруппированные по датам
    expenses_by_date = {}
    for date_info in unique_dates:
        date = date_info['date']
        expenses_by_date[date] = Expense.objects.filter(user=request.user, date=date)

    category_data = []
    category_labels = []

    # Получите уникальные категории
    unique_categories = Expense.objects.filter(user=request.user).values('category').distinct()

    # Посчитайте сумму расходов в каждой категории
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total']

    for category_info in unique_categories:
        category = category_info['category']
        category_expenses = Expense.objects.filter(user=request.user, category=category).aggregate(total=Sum('amount'))[
            'total']

        # Рассчитайте проценты от общей суммы
        percentage = (category_expenses / total_expenses) * 100 if total_expenses else 0

        category_labels.append(category)
        category_data.append(percentage)

    context = {'expenses_by_date': expenses_by_date, 'form': ExpenseForm(), 'category_labels': category_labels,
               'category_data': category_data}

    return render(request, 'finance/home.html', context)



def about(request):
    return render(request, 'finance/about.html')
