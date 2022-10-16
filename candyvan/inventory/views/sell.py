from django.shortcuts import render, redirect

from ..models import CandyUser, Item, Sale, Transaction, Revenue, ItemHistory

import json
import datetime


def update_itemhistory():
    if ItemHistory.objects.filter(date=datetime.date.today()):
        return

    print("Creating new item histories")

    for item in Item.objects.all():
        history = ItemHistory(
            item=item,
            buy_price=item.buy_price,
            sell_price=item.sell_price,
            quantity=item.quantity
        )
        history.save()

    return


def get_today_revenue_entry():
    try:
        revenue_entry = Revenue.objects.get(date=datetime.date.today())
    except Revenue.DoesNotExist:
        revenue_entry = Revenue(revenue=0)

    return revenue_entry


def add_sale_to_revenue(item, quantity):
    profit_per_item = item.sell_price - item.buy_price
    revenue = quantity * profit_per_item

    revenue_entry = get_today_revenue_entry()
    revenue_entry.revenue += revenue
    revenue_entry.save()


def record_sale(user, item, quantity, parent=None):
    sale = Sale(user=user, item=item, quantity=quantity)
    if parent is not None:
        sale.parent = parent

    item.quantity -= quantity

    item.save()
    sale.save()

    return sale


def sell_post(request):
    user = CandyUser.objects.get(id=request.session['user_id'])
    print("\n".join(f"{x}: {y}" for x, y in request.POST.items()))

    sales = {
        Item.objects.get(name=name): int(value)
        for name, value in request.POST.items()
        if not name.startswith("csrf")
    }

    update_itemhistory()

    profit = 0
    main_sale = None

    for i, value in enumerate(sales.items()):
        item, quantity = value
        if not item:
            return f"Model {list(request.POST.keys())[i]} does not exist. " \
                   "Please contact Administrator for assistance."
        if item.quantity < quantity:
            return f"{item.name} has only {item.quantity} items available, " \
                   f"larger than {quantity}."
        if quantity <= 0:
            return "Quantity can't be zero or negative! >:("

        sale = record_sale(user, item, quantity, main_sale)
        if main_sale is None:
            main_sale = sale

        add_sale_to_revenue(item, quantity)
        profit += item.sell_price * quantity

    transaction = Transaction(user=user, amount=profit, sale=main_sale)
    transaction.save()

    return redirect("sell")


def sell(request):
    if not request.session.get('user_id'):
        return redirect("login")
    user = CandyUser.objects.get(id=request.session['user_id'])

    item_data = {
        x.name: {"available": x.quantity, "price": float(x.sell_price)}
        for x in Item.objects.all()
    }

    if request.method == "POST":
        rtnvalue = sell_post(request)
        if isinstance(rtnvalue, str):
            return render(
                request, 'inventory/sell.html',
                {'item_data': json.dumps(item_data), 'error': rtnvalue,
                 'admin': user.is_staff})
        else:
            return rtnvalue

    return render(request, 'inventory/sell.html', {
        'item_data': json.dumps(item_data), 'error': "", 'admin': user.is_staff
    })
