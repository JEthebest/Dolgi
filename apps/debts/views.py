from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.db.models.functions import TruncMonth

from apps.debts.models import Debt, Agent
from apps.debts.forms import DebtForm, AgentForm


@login_required
def agent_debts(request):
    user_agents = Agent.objects.filter(user=request.user)
    debts = Debt.objects.filter(agent__in=user_agents)

    context = {
        'debts': debts
    }
    return render(request, 'debts/agent_debts.html', context)


@login_required
def my_debts(request):
    user_agents = Agent.objects.filter(user=request.user)
    my_debts = Debt.objects.filter(
        tranzaction_type='ВЗЯТЬ', agent__in=user_agents
    )

    context = {
        'my_debts': my_debts
    }
    return render(request, 'debts/my_debts.html', context)


@login_required
def debts_to_me(request):
    user_agents = Agent.objects.filter(user=request.user)
    debts_to_me = Debt.objects.filter(
        tranzaction_type='ДАТЬ', agent__in=user_agents
    )

    context = {
        'debts_to_me': debts_to_me
    }
    return render(request, 'debts/debts_to_me.html', context)


@login_required
def create_agent(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.user = request.user
            agent.save()
            messages.success(request, 'Агент создан успешно!')
            return redirect('agent_debts')
    else:
        form = AgentForm()

    context = {
        'form': form
    }
    return render(request, 'agents/create.html', context)


@login_required
def create_debt(request):
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.save()
            messages.success(request, 'Задолженность создана успешно!')
            return redirect('agent_debts')
    else:
        form = DebtForm()

    context = {
        'form': form
    }
    return render(request, 'debts/create_debt.html', context)


@login_required
def update_debt(request, pk):
    debt = get_object_or_404(Debt, pk=pk)

    if request.method == 'POST':
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.save()
            messages.success(request, 'Задолженность изменена успешно!')
            return redirect('agent_debts')
    else:
        form = DebtForm(instance=debt)

    context = {
        'form': form
    }
    return render(request, 'debts/update_debt.html', context)


@login_required
def delete_debt(request, pk):
    debt = get_object_or_404(Debt, pk=pk)
    debt.delete()
    messages.success(request, 'Задолженность удалена успешно!')
    return redirect('agent_debts')


@login_required
def account_statistics(request):
    user_agents = Agent.objects.filter(user=request.user)

    total_given = Debt.objects.filter(
        tranzaction_type='ДАТЬ', agent__in=user_agents
    ).aggregate(Sum('amount'))['amount__sum']
    total_taken = Debt.objects.filter(
        tranzaction_type='ВЗЯТЬ', agent__in=user_agents
    ).aggregate(Sum('amount'))['amount__sum']
    balance = (total_given or 0) - (total_taken or 0)

    context = {
        'total_given': total_given,
        'total_taken': total_taken,
        'balance': balance,
    }
    return render(request, 'accounts/statistics.html', context)


@login_required
def agents_balance(request):
    user_agents = Agent.objects.filter(user=request.user)

    agents_balance = {}
    for agent in user_agents:
        given = Debt.objects.filter(
            tranzaction_type='ДАТЬ', agent=agent
        ).aggregate(Sum('amount'))['amount__sum']
        taken = Debt.objects.filter(
            tranzaction_type='ВЗЯТЬ', agent=agent
        ).aggregate(Sum('amount'))['amount__sum']
        balance = (given or 0) - (taken or 0)
        agents_balance[agent] = balance

    context = {
        'agents_balance': agents_balance,
    }
    return render(request, 'accounts/agents_balance.html', context)


@login_required
def debts_history(request):
    user_agents = Agent.objects.filter(user=request.user)
    debts_history = Debt.objects.filter(
        agent__in=user_agents
    ).order_by('-date')

    context = {
        'debts_history': debts_history,
    }
    return render(request, 'debts/history.html', context)


@login_required
def turnover(request):
    user_agents = Agent.objects.filter(user=request.user)

    given_by_month = Debt.objects.filter(
        tranzaction_type='ДАТЬ', agent__in=user_agents
    )\
        .annotate(month=TruncMonth('date'))\
        .values('month')\
        .annotate(amount=Sum('amount'))\
        .order_by('-month')
    taken_by_month = Debt.objects.filter(
        tranzaction_type='ВЗЯТЬ', agent__in=user_agents
    )\
        .annotate(month=TruncMonth('date'))\
        .values('month')\
        .annotate(amount=Sum('amount'))\
        .order_by('-month')

    context = {
        'given_by_month': given_by_month,
        'taken_by_month': taken_by_month,
    }
    return render(request, 'debts/turnover.html', context)
