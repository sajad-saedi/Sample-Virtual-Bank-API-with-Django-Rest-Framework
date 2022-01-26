import os
import sys

from django.http import JsonResponse
from .models import TransactionLog


class TransactionLogging:

    def __init__(self, log_params):
        self.log_params = log_params
        self.save_to_db()

    def prepare_variables(self, transaction_type, first_customer, second_customer, transaction_amount, log_status):
        return dict(transaction_type=transaction_type, first_customer=first_customer, second_customer=second_customer,
                    transaction_amount=transaction_amount, status=log_status)

    def save_to_db(self):
        try:
            TransactionLog.objects.create(transaction_type=self.log_params['transaction_type'],
                                          first_customer=self.log_params['first_customer'],
                                          second_customer=self.log_params['second_customer'],
                                          transaction_amount=self.log_params['transaction_amount'],
                                          status=self.log_params['status'])
        except Exception as ex:
            print(ex)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'result': 'Error is {0}'.format(ex), 'Line': str(exc_tb.tb_lineno)})
