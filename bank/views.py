import random

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bank, Branch, Customer, CustomerLoan, BranchManager, TransactionLog
from .serializers import *
from .transaction_log import TransactionLogging


class BanksAPIView(APIView):

    def get(self, request):
        banks = Bank.objects.all().values()
        return JsonResponse({'result': list(banks)})


class BranchesAPIView(APIView):

    def get(self, request):
        data = request.data
        bank_name = data.get('bank_name')
        branches = Branch.objects.all()
        if bank_name:
            branches = branches.filter(bank__name=bank_name).values()
            return JsonResponse({'result': list(branches)})
        return JsonResponse({'result': list(branches.values())})


class CustomerViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def create(self, request, *args, **kwargs):
        account_number = random.randint(10000, 99999)
        request.data['account_number'] = account_number
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerLoanViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = CustomerLoanSerializer
    queryset = CustomerLoan.objects.all()


class TransferAPIView(APIView):

    def put(self, request, id):
        data = request.data
        other_account_number = data.get('account_number', None)
        transfer_amount = data.get('amount', None)
        first_obj = Customer.objects.get(id=id)
        other_obj = Customer.objects.get(account_number=other_account_number)
        if transfer_amount > first_obj.deposit:
            log_params = TransactionLogging.prepare_variables(self, 'transfer', first_obj.account_number,
                                                              other_obj.account_number,
                                                              transfer_amount, False)
            TransactionLogging(log_params)
            return Response({'result': "You don't have enough money"})

        first_obj.deposit = first_obj.deposit - transfer_amount
        other_obj.deposit = other_obj.deposit + transfer_amount
        first_obj.save()
        other_obj.save()
        log_params = TransactionLogging.prepare_variables(self, 'transfer', first_obj.account_number,
                                                          other_obj.account_number, transfer_amount,
                                                          True)
        TransactionLogging(log_params)
        return Response({'result': "Transfer Completed"})


class DepositAPIView(APIView):

    def put(self, request, id):
        data = request.data
        amount = data.get('amount', None)
        customer_obj = Customer.objects.get(id=id)
        if amount <= 0:
            log_params = TransactionLogging.prepare_variables(self, 'deposit', customer_obj.account_number, None,
                                                              amount, False)
            TransactionLogging(log_params)
            return Response({'result': "Deposit amount should be more than zero."})

        customer_obj.deposit = customer_obj.deposit + amount
        customer_obj.save()
        log_params = TransactionLogging.prepare_variables(self, 'deposit', customer_obj.account_number, None, amount,
                                                          True)
        TransactionLogging(log_params)
        return Response({'result': "Deposit Complete"})


class WithdrawAPIView(APIView):

    def put(self, request, id):
        data = request.data
        amount = data.get('amount', None)
        customer_obj = Customer.objects.get(id=id)
        if amount > customer_obj.deposit:
            log_params = TransactionLogging.prepare_variables(self, 'withdraw', customer_obj.account_number, None,
                                                              amount, False)
            TransactionLogging(log_params)
            return Response({'result': "You don't have enough money"})

        customer_obj.deposit = customer_obj.deposit - amount
        customer_obj.save()
        log_params = TransactionLogging.prepare_variables(self, 'withdraw', customer_obj.account_number, None, amount,
                                                          True)
        TransactionLogging(log_params)
        return Response({'result': "Transfer Completed"})


class CustomerReportAPIView(APIView):

    def get(self, request, username):
        data = request.data
        account_number = data.get('account_number')
        try:
            BranchManager.objects.get(username=username)
            customer_report = TransactionLog.objects.filter(first_customer=account_number).values()
            if customer_report:
                return JsonResponse({'result': list(customer_report)})
            else:
                return Response({'result': f"Account number '{account_number}' does not exist."})
        except ObjectDoesNotExist:
            return Response({'result': "You don't have access."})
