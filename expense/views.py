
from django.shortcuts import render, redirect
from .models import ExpenseForm, Expense
from django.contrib.auth.models import User

def addexpense1(request):
    uid = request.session.get('uid')

    if request.method == 'POST':
        expense = request.POST.get('expense')
        if get_balance(request) > int(expense):
            expense_type = request.POST.get('expense_type')
            expense = request.POST.get('expense')
            expense_type = request.POST.get('expense_type')
            expense_date = request.POST.get('expense_date')
            description = request.POST.get('description')
            inc = Expense()
            inc.expense = expense
            inc.expense_type = expense_type
            inc.expense_date = expense_date
            inc.description = description
            inc.user = User.objects.get(id=uid)
            inc.save()
            return redirect('/')

        else:
            f = ExpenseForm
            y = {'k': f, 'exp_msg': 'Warning : In-sufficient balance !!!'}
            return render(request, "addexpense1.html", y)

    else:
        f = ExpenseForm
        y = {'k': f}
        return render(request, "addexpense1.html", y)

def data2(request):
    uid = request.session.get('uid')
    elist = Expense.objects.filter(user=uid)
    expt = set()
    for i in elist:
        expt.add(i.expense_type)

    d = {'s': elist, 'expt': expt}
    return render(request, 'db3.html', d)

def delete_E(request, id):
    x = Expense.objects.get(id=id)
    x.delete()
    return redirect('/expenselist')

def edit_E(request, id):
    me = Expense.objects.get(id=id)
    if request.method == 'POST':
        f = ExpenseForm(request.POST, instance=me)
        f.save()
        return redirect('/')

    else:
        fe = ExpenseForm(instance=me)
        contexts = {'s': fe}
        return render(request, "addexpense1.html", contexts)

def expense_search2(request):
    uid = request.session.get('uid')
    srch = request.POST.get('srch')
    expl = Expense.objects.filter(user=uid, description__icontains=srch)
    context = {'s': expl}
    return render(request, "db3.html", context)

def sort_data(request, ext):
    uid = request.session.get('uid')
    elist = Expense.objects.filter(user=uid)
    expt = set()
    for i in elist:
        expt.add(i.expense_type)

    elist = Expense.objects.filter(user=uid, expense_type=ext)
    d = {'s': elist, 'expt': expt}
    return render(request, 'db3.html', d)

from income.models import Income
from expense.models import Expense

def get_balance(request):
    uid = request.session.get('uid')
    incl = Income.objects.filter(user=uid)
    expl = Expense.objects.filter(user=uid)

    total_income = 0
    total_expense = 0

    for i in incl:
        total_income = total_income + i.income

    for i in expl:
        total_expense = total_expense + i.expense

    return total_income - total_expense

from .models import Payment

import razorpay
from django.conf import settings

def payment1(request):
    user = request.user
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    DATA = {'amount': 50000, 'currency': 'INR', 'receipt': 'receipt#1'}
    payment_response = client.order.create(data=DATA)
    print(payment_response)
    id = payment_response['id']
    status = payment_response['status']
    if status == 'created':
        payment = Payment(
            user=user,
            razorpay_id=id,
            razorpay_payment_status=status

        )
        payment.save()
    return render(request, 'payment.html')
