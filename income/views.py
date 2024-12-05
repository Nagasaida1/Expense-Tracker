from django.shortcuts import render, redirect
from .models import IncomeForm, Income
from django.contrib.auth.models import User

def addincome2(request):
    uid = request.session.get('uid')
    if request.method == 'POST':
        income = request.POST.get('income')
        income_type = request.POST.get('income_type')
        income_date = request.POST.get('income_date')
        description = request.POST.get('description')
        incs = Income(
            income=income,
            income_type=income_type,
            income_date=income_date,
            description=description,
            user=User.objects.get(id=uid)
        )
        incs.save()
        return redirect('/')
    else:
        f = IncomeForm()
        return render(request, "addincome1.html", {'h': f})

def data1(request):
    uid = request.session.get('uid')
    elist = Income.objects.filter(user=uid)
    ixpt = {i.income_type for i in elist}
    return render(request, 'dbb.html', {'s': elist, 'ixpt': ixpt})

def delete_emp(request, id):
    Income.objects.get(id=id).delete()
    return redirect('/incomelist')

def edit1(request, id):
    m = Income.objects.get(id=id)
    if request.method == 'POST':
        f = IncomeForm(request.POST, instance=m)
        f.save()
        return redirect('/incomelist')
    else:
        f = IncomeForm(instance=m)
        return render(request, "addincome1.html", {'s': f})

def income_search2(request):
    uid = request.session.get('uid')
    srch = request.POST.get('srchs')
    expl = Income.objects.filter(user=uid, description__icontains=srch)
    return render(request, "dbb.html", {'s': expl})

def sort_data1(request, ixt):
    uid = request.session.get('uid')
    elist = Income.objects.filter(user=uid)
    ixpt = {i.income_type for i in elist}
    elist = Income.objects.filter(user=uid, income_type=ixt)
    return render(request, 'dbb.html', {'s': elist, 'ixpt': ixpt})
