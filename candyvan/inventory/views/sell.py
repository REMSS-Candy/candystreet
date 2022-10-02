from django.shortcuts import render, redirect

from ..models import Item

import json


def sell_post(request):
    pass


def sell(request):
    if not request.session.get('user_id'):
        return redirect("login")
    item_data = {
        x.name: {"available": x.quantity, "price": float(x.sell_price)}
        for x in Item.objects.all()
    }

    return render(request, 'inventory/temporary/sell.html',
                  {'item_data': json.dumps(item_data), 'error': ""})
