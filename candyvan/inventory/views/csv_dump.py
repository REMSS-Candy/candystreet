from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect

from ..forms import CSVForm
from ..models import CandyUser, Item, Sale, ItemHistory

import io
import csv
import datetime


def dump_data_from_db(start_date):
    # Structure: rtndata[date][item_id]['start'|'sold'] = item_quantity
    # Order should be preserved for dict since 3.6
    rtndata = {}

    daydelta = datetime.timedelta(days=1)
    date = start_date - daydelta

    while date <= datetime.date.today():
        date += daydelta
        sales = Sale.objects.filter(time__gte=date) \
                            .filter(time__lte=date+daydelta)
        histories = ItemHistory.objects.filter(date=date)

        if not (sales and histories):
            continue

        data_today = {}

        for item_start in histories:
            item = item_start.item
            item_data = {
                "start": item_start.quantity,
                "sold": 0
            }

            sold = sum([sale.quantity for sale in sales if sale.item == item])
            item_data["sold"] = sold

            data_today[item.id] = item_data

        rtndata[date.isoformat()] = data_today

    return rtndata


def format_sales_csv(start_date):
    data = dump_data_from_db(start_date)
    items = Item.objects.all().order_by('id')

    file = io.StringIO(newline="")
    writer = csv.writer(file)

    writer.writerow(["Type", "Date"] + [item.name for item in items])

    for date, data_day in data.items():
        writer.writerows([
            ["START INV", date] + [
                data_day[item.id]["start"] if item.id in data_day else "0"
                for item in items
            ],
            ["SOLD INV", date] + [
                data_day[item.id]["sold"] if item.id in data_day else "0"
                for item in items
            ]
        ])

    file.seek(0)

    return file.read()


def format_item_stat_csv(start_date):
    data = dump_data_from_db(start_date)
    items = Item.objects.all().order_by('id')

    file = io.StringIO(newline="")
    writer = csv.writer(file)

    writer.writerow(
        ["Item", "Cost", "Selling Price", "Markup", "Daily Avg. Sold %"])

    for item in items:
        name = item.name
        cost = item.buy_price
        sell_price = item.sell_price
        markup = round(sell_price / cost * 100)
        daily_sales = [data_day[item.id] for data_day in data.values()
                       if item.id in data_day]

        daily_percentages = [round(sale['sold'] / sale['start'] * 100)
                             for sale in daily_sales]

        daily_avg = round(sum(daily_percentages) / len(daily_percentages))

        writer.writerow(
            [name, cost, sell_price, f"{markup}%", f"{daily_avg}%"])

    file.seek(0)

    return file.read()


def csv_post(request):
    form = CSVForm(request.POST)
    if not form.is_valid():
        return redirect("csv")

    date = form.cleaned_data['date']

    today = timezone.now().date().isoformat()
    filename = f"{date.isoformat()}_{today}.csv"

    if "submit_sales" in request.POST:
        filename = f"sales_{filename}"
        data = format_sales_csv(date)

        return HttpResponse(data, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    elif "submit_items" in request.POST:
        filename = f"items_{filename}"
        data = format_item_stat_csv(date)

        return HttpResponse(data, headers={
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    else:
        resp = HttpResponse("whar happne???")
        resp.status_code = 400
        return resp


def csv_view(request):
    if not request.session.get('user_id'):
        return redirect("login")

    user = CandyUser.objects.get(id=request.session['user_id'])

    if not user.is_staff:
        return redirect("sell")

    if request.method == "POST":
        return csv_post(request)

    form = CSVForm()

    return render(request, "inventory/admin-csv.html", {"form": form})
