from rest_framework import serializers

from .models import Bank, Branch, Customer, CustomerLoan


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLoan
        fields = '__all__'
