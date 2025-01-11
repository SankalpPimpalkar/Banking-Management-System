from django.shortcuts import render
from Bank.models import Transaction,Account
from django.db.models import Q
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='login_account')
def home_page(request):
    accounts = Account.objects.filter(user__id=request.user.id)

    transactions = Transaction.objects.none()
    selected_account = accounts[0]

    if request.method == 'POST':
        search = request.POST.get('search') or ''
        transactions = Transaction.objects.filter(
            Q(sender_account__account_number__icontains=search) |
            Q(recipient_account__account_number__icontains=search)
        )

    if request.method == 'GET':
        from_year = request.GET.get('from')
        to_year = request.GET.get('to')
        transaction_type = request.GET.get('type') or ''
        selected_account_id = request.GET.get('selected_account')

        if selected_account_id:
            selected_account = get_object_or_404(Account, id=selected_account_id, user=request.user)
            
            filters = Q(sender_account=selected_account)
            
            if from_year and to_year:
                try:
                    from_date = datetime(int(from_year), 1, 1)
                    to_date = datetime(int(to_year), 12, 31)
                    filters &= Q(transaction_date__range=(from_date, to_date))
                except ValueError:
                    pass
            
            if transaction_type != '':
                filters &= Q(transaction_type__iexact=transaction_type)

            transactions = Transaction.objects.filter(filters).order_by('-transaction_date')
        else:
            transactions = Transaction.objects.filter(sender_account=selected_account).order_by('-transaction_date')

    context = {
        'transactions': transactions,
        'accounts': accounts,
        'selected_account': selected_account,
    }

    return render(request, 'home.html', context)