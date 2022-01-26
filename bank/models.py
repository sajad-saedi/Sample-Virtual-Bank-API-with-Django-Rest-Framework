from django.db import models


# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    bank_code = models.CharField(max_length=250)

    def json_object(self):
        return {
            "name": self.name,
            "address": self.address,
            "branch_code": self.bank_code
        }

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=250)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def json_object(self):
        return {
            "name": self.name,
            "branch": self.bank
        }

    def __str__(self):
        return self.name


class BranchManager(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    family = models.CharField(max_length=250)
    username = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f"{self.name} {self.family}: {self.branch}"


class Customer(models.Model):
    name = models.CharField(max_length=250)
    family = models.CharField(max_length=250)
    national_code = models.IntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    account_number = models.IntegerField(unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    deposit = models.FloatField()

    def __str__(self):
        return f"{self.name} {self.family}: {self.account_number}"


class RepaymentTime(models.Model):
    repayment_time = models.IntegerField()

    def __str__(self):
        return str(self.repayment_time)


class Loan(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    repayment_type = models.ForeignKey(RepaymentTime, on_delete=models.CASCADE)
    amount = models.IntegerField()
    interest = models.IntegerField()

    def __str__(self):
        return f"{self.branch}: {self.amount}-{self.repayment_type}"


class CustomerLoan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)


class TransactionLog(models.Model):
    transaction_type = models.CharField(max_length=250)
    first_customer = models.IntegerField()
    second_customer = models.IntegerField(blank=True, null=True)
    transaction_amount = models.IntegerField()
    log_datetime = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
