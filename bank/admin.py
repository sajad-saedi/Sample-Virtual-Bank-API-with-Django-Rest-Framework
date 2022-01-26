from django.contrib import admin
from .models import Bank, Branch, BranchManager, Customer, RepaymentTime, Loan

# Register your models here.
admin.site.register(Bank)
admin.site.register(Branch)
admin.site.register(BranchManager)
admin.site.register(Customer)
admin.site.register(RepaymentTime)
admin.site.register(Loan)
