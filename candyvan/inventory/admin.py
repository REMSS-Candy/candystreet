from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CandyUser, Item, Sale, Transaction, Revenue, ItemHistory

admin.site.register(CandyUser, UserAdmin)
admin.site.register(Item)
admin.site.register(Sale)
admin.site.register(Transaction)
admin.site.register(Revenue)
admin.site.register(ItemHistory)
