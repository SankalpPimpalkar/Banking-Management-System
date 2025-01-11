from django.shortcuts import render,redirect
from .models import Account,Transaction
from django.contrib import messages
from users.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(redirect_field_name='login_account')
def deposit_page(request):
    if request.method == 'POST':
        account_id = request.POST.get('account')
        amount = request.POST.get('amount')

        account = Account.objects.get(id= account_id)
        account.balance += float(amount)
        account.save()

        Transaction.objects.create(
            sender_account=account,
            transaction_type='Deposit',
            amount=amount
        )

        return redirect('home_page')

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'forms/deposit.html', {'accounts': accounts})

@login_required(redirect_field_name='login_account')
def transfer_page(request):
    if request.method == 'POST':
            account_id = request.POST.get('sender_account')
            recipient_account_number = request.POST.get('recipient_account')
            amount = request.POST.get('amount')

            sender_account = Account.objects.get(id=account_id)
            
            try:
                recipient_account = Account.objects.get(account_number=recipient_account_number)
            except Account.DoesNotExist:
                messages.info(request, 'Account does not exist')
                recipient_account = None

            if recipient_account is not None:
                print('Recipient', recipient_account)
                print('Sender', sender_account)
                
                sender_account.balance -= float(amount)
                recipient_account.balance += float(amount)
                sender_account.save()
                recipient_account.save()

                Transaction.objects.create(
                    sender_account=sender_account,
                    recipient_account=recipient_account,
                    transaction_type='Transfer',
                    amount=amount
                )

                return redirect('home_page')

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'forms/transfer.html', {'accounts': accounts})

@login_required(redirect_field_name='login_account')
def withdrawal_page(request):
    if request.method == 'POST':
        account_id = request.POST.get('account')
        amount = request.POST.get('amount')
        
        account = Account.objects.get(id=account_id)
        account.balance -= float(amount)
        account.save()
        
        Transaction.objects.create(
            sender_account=account,
            transaction_type= 'Withdrawal',
            amount=amount
        )
        
        return redirect('home_page')
    
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'forms/withdrawal.html', {'accounts': accounts})

@login_required(redirect_field_name='login_account')
def accounts_page(request):
    
    user = User.objects.get(id=request.user.id)
    accounts = Account.objects.filter(user=user)
    
    context = {
        'accounts': accounts
    }
    return render(request, 'accounts.html', context)

@login_required(redirect_field_name='login_account')
def create_account(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        user = User.objects.get(id=request.user.id)
        
        if not account_type:
            messages.info(request, 'Account Type is needed for creating account')
        else:
            Account.objects.create(
                user=user,
                account_type=account_type
            )
            
            return redirect('accounts_page')
    return render(request, 'forms/create_account.html')