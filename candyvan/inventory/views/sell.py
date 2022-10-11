from django.shortcuts import render, redirect

from ..models import CandyUser, Item, Sale, Transaction, Revenue

import json
import datetime


# sales :)
def sell_post(request):
    user = CandyUser.objects.get(id=request.session['user_id'])
    print("\n".join(f"{x}: {y}" for x, y in request.POST.items()))
    sales = {
        Item.objects.get(name=name): int(values[0])
        for name, values in request.POST.items()
        if not name.startswith("csrf")
    }

    profit = 0
    revenue = 0
    main_sale = None

    for item, quantity in sales.items():
        if not item:
            return "Model does not exist. " \
                   "Please contact Administrator for assistance."
        if item.quantity - quantity < 0:
            return f"{item.name} has only {item.quantity} items available, " \
                   f"larger than {quantity}."
        if quantity <= 0:
            return "Quantity can't be negative! >:("

        item.quantity -= quantity

        sale = Sale(user=user, item=item, quantity=quantity)
        if main_sale is None:
            main_sale = sale
        else:
            sale.parent_entry = main_sale

        item.save()
        sale.save()

        profit += item.sell_price * quantity
        revenue += (item.sell_price - item.buy_price) * quantity

    transaction = Transaction(user=user, amount=profit, sale=main_sale)
    transaction.save()

    try:
        revenue_entry = Revenue.objects.get(date=datetime.date.today())
        revenue_entry.revenue += revenue
    except Revenue.DoesNotExist:
        revenue_entry = Revenue(revenue=revenue)
    revenue_entry.save()

    return redirect("sell")


def sell(request):
    if not request.session.get('user_id'):
        return redirect("login")

    item_data = {
        x.name: {"available": x.quantity, "price": float(x.sell_price)}
        for x in Item.objects.all()
    }

    if request.method == "POST":
        rtnvalue = sell_post(request)
        if isinstance(rtnvalue, str):
            return render(
                request, 'inventory/sell.html',
                {'item_data': json.dumps(item_data), 'error': rtnvalue})
        else:
            return rtnvalue

    return render(request, 'inventory/sell.html',
                  {'item_data': json.dumps(item_data), 'error': ""})
