from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from decimal import Decimal

from apps.debts.models import Tranzaction, Contact
from apps.debts.forms import (
    TranzactionForm,
    ContactForm,
    TranzactionContactForm,
)


@login_required
def main_dolgi(request):
    return render(request, 'debts/main_dolgi.html')


@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.user = request.user
            agent.save()
            return redirect('main')
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/create.html', context)


@login_required
def borrow(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        transaction_form = TranzactionForm(request.POST)
        if contact_form.is_valid() and transaction_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.user = request.user
            contact.save()
            transaction = transaction_form.save(commit=False)
            transaction.agent = contact
            transaction.type = 'Займ'
            transaction.save()
            return redirect('main')
    else:
        contact_form = ContactForm()
        transaction_form = TranzactionForm()
    return render(
                request, 'debts/borrow.html',
                {
                    'contact_form': contact_form,
                    'transaction_form': transaction_form
                }
            )


@login_required
def repay(request, transaction_id, slug):
    transaction = Tranzaction.objects.get(id=transaction_id)
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        if amount == float(transaction.amount) and slug == 'Погасить':
            transaction.publish = False  # закрытие сделки
            transaction.save()
            return redirect('main')
        elif amount <= float(transaction.amount) and slug == 'Погасить':
            Tranzaction.objects.create(
                agent=transaction.agent,
                amount=transaction.amount - Decimal(amount),
                description=f"""
                        Repayment of {amount} from transaction #{
                        transaction.id
                    }"""
            )
            transaction.publish = False
            transaction.save()
            return redirect('main')
        elif slug == 'Увеличить':
            Tranzaction.objects.create(
                agent=transaction.agent,
                amount=transaction.amount + Decimal(amount),
                description=f"""
                        Repayment of {amount} from transaction #{
                        transaction.id
                    }"""
            )
            transaction.publish = False
            transaction.save()
            return redirect('main')
    return render(request, 'debts/repay.html', {'transaction': transaction})


@login_required
def receive_payment(request, transaction_id):
    transaction = Tranzaction.objects.get(id=transaction_id)
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        if amount <= transaction.amount:
            transaction.amount -= amount
            transaction.save()
            return redirect('dashboard')
    return render(
                request, 'receive_payment.html',
                {'transaction': transaction}
            )


@login_required
def lend(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        transaction_form = TranzactionForm(request.POST)
        if contact_form.is_valid() and transaction_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.user = request.user
            contact.save()
            transaction = transaction_form.save(commit=False)
            transaction.agent = contact
            transaction.type = 'Долг'
            transaction.save()
            return redirect('main')
    else:
        contact_form = ContactForm()
        transaction_form = TranzactionForm()
    return render(
        request, 'debts/lend.html',
        {'contact_form': contact_form, 'transaction_form': transaction_form}
    )


@login_required
def my_debts(request):
    user_agents = Contact.objects.filter(user=request.user)
    my_debts = Tranzaction.objects.filter(
        type='Займ', agent__in=user_agents
    ).exclude(publish=False)

    context = {
        'my_debts': my_debts
    }
    return render(request, 'debts/my_debts.html', context)


@login_required
def debts_to_me(request):
    user_agents = Contact.objects.filter(user=request.user)
    debts_to_me = Tranzaction.objects.filter(
        type='Долг', agent__in=user_agents
    ).exclude(publish=False)

    context = {
        'debts_to_me': debts_to_me
    }
    return render(request, 'debts/debts_to_me.html', context)


@login_required
def my_contacts(request, slug):
    if slug == 'Займ':
        context = {
            'contacts': Contact.objects.filter(
                user=request.user,
            ),
            'my_debts': Tranzaction.objects.filter(
                type=slug,
            ).exclude(publish=False)
        }
        return render(request, 'accounts/list_contact.html', context)
    if slug == 'Долг':
        context = {
            'contacts': Contact.objects.filter(
                user=request.user,
            ),
            'my_debts': Tranzaction.objects.filter(
                type=slug,
            ).exclude(publish=False)
        }
        return render(request, 'accounts/list_contact2.html', context)


@login_required
def take_loan(request, slug):
    if request.method == 'POST':
        if slug == 'Займ':
            form = TranzactionContactForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.type = 'Займ'
                transaction.save()
                return redirect('main')
        elif slug == 'Долг':
            form = TranzactionContactForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.type = 'Займ'
                transaction.save()
                return redirect('main')
    else:
        form = TranzactionContactForm()

    context = {
        'form': form,
    }
    return render(request, 'debts/create_tranzaction.html', context)
