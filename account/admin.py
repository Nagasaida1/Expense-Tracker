from django.contrib import admin
from income.models import Income
from expense.models import Expense, Payment  # Combine imports for clarity

class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'income', 'income_type', 'income_date', 'description', 'user']

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense', 'expense_type', 'expense_date', 'description', 'user']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']

# Register models with their respective admin classes
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)  # Add missing registration for Expense
admin.site.register(Payment, PaymentAdmin)
