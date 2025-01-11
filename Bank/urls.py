from django.urls import path
from .views import *

urlpatterns = [
    
    path('deposit/', deposit_page, name="deposit_page"),
    path('transfer/', transfer_page, name="transfer_page"),
    path('withdrawal/', withdrawal_page, name="withdrawal_page"),
    path('accounts/', accounts_page, name="accounts_page"),
    path('accounts/create', create_account, name="create_account"),
]
