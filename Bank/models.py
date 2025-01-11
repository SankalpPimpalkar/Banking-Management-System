from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
import uuid

User = settings.AUTH_USER_MODEL

def generate_account_number():
    return int(str(uuid.uuid4().int)[:14])

def generate_cvv():
    return int(str(uuid.uuid4().int)[:3])

class Account(models.Model):
    
    ACCOUNT_TYPE = [
        ('Savings', 'Savings'),
        ('Current', 'Current'),
        ('Fix Deposit', 'Fix Deposit')
    ]
    today = datetime.today()
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    account_number = models.BigIntegerField(default=generate_account_number)
    account_type = models.CharField(choices=ACCOUNT_TYPE, default='Savings', max_length=20)
    account_expiry = models.DateTimeField(default=today + timedelta(days=1000))
    balance = models.FloatField(default=0)
    cvv = models.IntegerField(default=generate_cvv)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    
    TRANSACTION_TYPE = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer')
    ]
    
    sender_account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    recipient_account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.FloatField()
    transaction_date = models.DateTimeField(auto_now_add=True)
