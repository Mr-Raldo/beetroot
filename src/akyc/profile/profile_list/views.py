import uuid
import json
from django.views.generic import TemplateView, ListView
from web_project import TemplateLayout
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.conf import settings
from auth.views import AuthView
from auth.helpers import send_verification_email
from akyc.serializers import ProfileSerializer, WalletSerializer
from akyc.models import Profile, Wallet
"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to users/urls.py file for more pages.
"""

class ProfileListView(PermissionRequiredMixin, TemplateView):
    permission_required = ("user.view_user", "user.delete_user", "user.change_user", "user.add_user")
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context

class ProfileList(ListView):
    model = Profile
    template_name = 'producers/producer_all.html'  # This template won't be used

    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all()
        data = []
        wallet_serializer = WalletSerializer()
        for profile in profiles:
            serializer = ProfileSerializer(profile)
            if profile:
                try:   # Using get() to retrieve the object based on the condition
                        wallet = Wallet.objects.get(user=profile)
                        if wallet:
                            wallet_serializer = WalletSerializer(wallet)
                except Wallet.DoesNotExist:
                        pass

            data.append({
                'profile':serializer.data,
                'wallet': wallet_serializer.data,
                'id': profile.id,
                'full_name': profile.user.username,
                'customer_id': profile.id,
                'email': profile.email,
                'role':  profile.role,
                'account_type': profile.account_type,
                'specialization': profile.is_premium_subscribed,
                'phone': profile.phone,
                'order_count': profile.service_order_producer.count(),  # Assuming related_name in ServiceOrder for producer
                'total_spent':  0,
                'trading_as':profile.trading_as,
           
            })
        return JsonResponse({'data': data})
