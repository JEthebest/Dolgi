from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.debts.models import Transaction, Contact
from apps.debts.forms import (
    TransactionForm,
    ContactForm,
)


@login_required
def main_dolgi(request):
    return render(request, 'debts/main_dolgi.html')


@login_required
def my_debts(request):
    debts = Transaction.objects.filter(
        contact__user=request.user,
        transaction_type='BORROW'
    )
    context = {
        'debts': debts
    }
    return render(request, 'debts/my_debts.html', context)


@login_required
def debts_to_me(request):
    debts = Transaction.objects.filter(
        contact__user=request.user,
        transaction_type='LEND'
    )
    print(debts)
    context = {
        'debts': debts
    }
    return render(request, 'debts/debts_to_me.html', context)


@login_required
def transaction_contact(request, transaction_type):
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            contact = Contact.objects.get(id=contact_id)
            transaction.contact = contact
            transaction.transaction_type = transaction_type
            transaction.save()
            return redirect('main')
    else:
        contact_form = ContactForm()
        transaction_form = TransactionForm()
        contacts = Contact.objects.filter(user=request.user)
    context = {
        'contact_form': contact_form,
        'transaction_form': transaction_form,
        'contacts': contacts,
    }
    return render(request, 'debts/contact_transaction.html', context)


@login_required
def transaction(request, transaction_type):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        transaction_form = TransactionForm(request.POST)
        if contact_form.is_valid() and transaction_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.user = request.user
            contact.save()
            transaction = transaction_form.save(commit=False)
            transaction.contact = contact
            transaction.transaction_type = transaction_type
            transaction.save()
            return redirect('main')
    else:
        contact_form = ContactForm()
        transaction_form = TransactionForm()
    context = {
        'contact_form': contact_form,
        'transaction_form': transaction_form
    }
    return render(request, 'debts/transaction.html', context)


@login_required
def new_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('main')
    else:
        form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'debts/new_contact.html', context)
