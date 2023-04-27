from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from apps.debts.models import Debt, Agent
from apps.debts.forms import DebtForm, AgentForm


@login_required
def debts_list(request):
    # Получение всех долгов пользователя,
    # где пользователь - кредитор или должник
    user_debts = Debt.objects.filter(
        creditor=request.user
    ) | Debt.objects.filter(creditor=request.user)
    context = {
        'debts': user_debts
    }
    return render(request, 'debts/list.html', context)


@login_required
def debt_detail(request, debt_id):
    # Получение конкретного долга пользователя
    debt = get_object_or_404(Debt, id=debt_id, creditor=request.user)
    # или debtor=request.user, в зависимости от роли пользователя
    context = {
        'debt': debt
    }
    return render(request, 'debts/detail.html', context)


@login_required
def create_agent(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.user = request.user
            agent.save()
            return redirect('agent_detail', agent_id=agent.id)
    else:
        form = AgentForm()
    context = {
        'form': form
    }
    return render(request, 'agents/create.html', context)


@login_required
def agent_detail(request, agent_id):
    # Получение информации об агенте пользователя
    agent = get_object_or_404(Agent, id=agent_id, user=request.user)
    # Получение всех долгов пользователя, связанных с агентом
    agent_debts = Debt.objects.filter(
        agent=agent, creditor=request.user
    ) | Debt.objects.filter(agent=agent, debtor=request.user)
    # Получение общей суммы долгов пользователя, связанных с агентом
    total_amount = agent_debts.aggregate(
        total_amount=Sum('amount')
    ).get('total_amount', 0)
    context = {
        'agent': agent,
        'debts': agent_debts,
        'total_amount': total_amount
    }
    return render(request, 'agents/detail.html', context)


@login_required
def take_loan(request, agent_id):
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.agent_id = agent_id
            debt.debtor = request.user
            debt.save()
            return redirect('agent_detail', agent_id=agent_id)
    else:
        form = DebtForm()
    context = {
        'form': form
    }
    return render(request, 'debts/take_loan.html', context)


@login_required
def give_loan(request, agent_id):
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.agent_id = agent_id
            debt.creditor = request.user
            debt.save()
            return redirect('agent_detail', agent_id=agent_id)
    else:
        form = DebtForm()
    context = {
        'form': form
    }
    return render(request, 'debts/give_loan.html', context)


@login_required
def increase_loan(request, debt_id):
    debt = get_object_or_404(Debt, id=debt_id, creditor=request.user)
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            form.save()
            return redirect('debt_detail', debt_id=debt_id)
    else:
        form = DebtForm(instance=debt)
    context = {
        'form': form
    }
    return render(request, 'debts/increase_loan.html', context)


@login_required
def pay_debt(request, debt_id):
    debt = get_object_or_404(Debt, id=debt_id, debtor=request.user)
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            form.save()
            return redirect('debt_detail', debt_id=debt_id)
    else:
        form = DebtForm(instance=debt)
    context = {
        'form': form
    }
    return render(request, 'debts/pay_debt.html', context)


@login_required
def account_statistics(request):
    # Получение всех долгов пользователя
    user_debts = Debt.objects.filter(
        creditor=request.user
    ) | Debt.objects.filter(debtor=request.user)
    # Получение всех агентов пользователя
    user_agents = Agent.objects.filter(user=request.user)
    # Получение всех долгов пользователя, связанных с каждым агентом
    agent_debts = []
    for agent in user_agents:
        agent_debts.append({
            'agent': agent,
            'debts': Debt.objects.filter(
                agent=agent, creditor=request.user
            ) | Debt.objects.filter(agent=agent, debtor=request.user),
            'total_amount': Debt.objects.filter(
                agent=agent, creditor=request.user
            ).aggregate(total_amount=Sum('amount')).get('total_amount', 0)
        })
    # Получение общей суммы долгов пользователя
    total_amount = user_debts.aggregate(
        total_amount=Sum('amount')
    ).get('total_amount', 0)
    context = {
        'user_agents': user_agents,
        'agent_debts': agent_debts,
        'total_amount': total_amount
    }
    return render(request, 'accounts/statistics.html', context)


@login_required
def transaction_history(request):
    # Получение всех транзакций пользователя
    transactions = Debt.objects.filter(
        creditor=request.user
    ) | Debt.objects.filter(debtor=request.user)
    context = {
        'transactions': transactions
    }
    return render(request, 'accounts/transactions.html', context)


@login_required
def turnover(request):
    # Получение общей суммы долгов пользователя
    user_debts = Debt.objects.filter(
        creditor=request.user
    ) | Debt.objects.filter(debtor=request.user)
    total_amount = user_debts.aggregate(
        total_amount=Sum('amount')
    ).get('total_amount', 0)

    # Получение общей суммы оборотов пользователя с каждым агентом
    agent_turnover = []
    user_agents = Agent.objects.filter(user=request.user)
    for agent in user_agents:
        agent_turnover.append({
            'agent': agent,
            'turnover': Debt.objects.filter(
                agent=agent, creditor=request.user
            ).aggregate(
                turnover=Sum('amount')
            ).get('turnover', 0) - Debt.objects.filter(
                agent=agent, debtor=request.user
            ).aggregate(turnover=Sum('amount')).get('turnover', 0)
        })

    context = {
        'user_agents': user_agents,
        'agent_turnover': agent_turnover,
        'total_amount': total_amount
    }
    return render(request, 'accounts/turnover.html', context)
