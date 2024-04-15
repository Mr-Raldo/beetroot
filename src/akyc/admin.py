# Register your models here.
from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import  Subscription, Wallet, WalletTransaction
from dashboards.sites import dashboards_admin_site

@admin.register(Subscription, site=dashboards_admin_site)
class SubscriptionAdmin(ModelAdmin):
    pass


@admin.register(Wallet, site=dashboards_admin_site)
class WalletAdmin(ModelAdmin):
    pass


@admin.register(WalletTransaction, site=dashboards_admin_site)
class WalletTransactionAdmin(ModelAdmin):
    pass

