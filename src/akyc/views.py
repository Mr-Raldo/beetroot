import json
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q

from rest_framework import status
from akyc.serializers import ProfileSerializer
from akyc.models import Profile
from akyc.firebase_api import add_profile_to_firebase
"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to users/urls.py file for more pages.
"""


@api_view(['GET',])
def profile_to_firebase(request):
    profiles =  Profile.objects.all()
    for profile in profiles:
        data = ProfileSerializer(profile)
        add_profile_to_firebase(data)
        
    
class UsersView(PermissionRequiredMixin, TemplateView):
    permission_required = ("user.view_user", "user.delete_user", "user.change_user", "user.add_user")


    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


@api_view(['GET', 'POST'])
def users_list(request, format=None):
    if request.method == 'GET':
        print(request.data)
        users = Profile.objects.all()
        serializer = ProfileSerializer(users, many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        # user_data_str = request.POST.get('user', '')
        print('request.data)',request.data)
        print('request.data)',request.data['searchTerm'])
        # user_data = json.loads(user_data_str)
        searchTerm = request.data['searchTerm']
        # searchResults = Profile.objects.contains(searchTerm)
        matching_profiles = Profile.objects.filter(
            first_name__icontains=searchTerm
        )
        
        print('matching_profiles', matching_profiles)
        serializer = ProfileSerializer(matching_profiles, many=True)
        return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)
        # print(user_data)

    # Handle other HTTP methods if needed
    return Response({'message': 'Invalid HTTP method'})

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id, format=None):
    try:
        user = Profile.objects.get(pk=id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response({'user': serializer.data})

    elif request.method == 'PUT':
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def wallets_list(request, format=None):
    users = Profile.objects.all()
    serializer = WalletSerializer(users, many=True)
    return Response({'wallets': serializer.data})

def wallet_transactions_list(request, format=None):
    users = Profile.objects.all()
    serializer = WalletTransactionSerializer(users, many=True)
    return Response({'wallet_transactions': serializer.data})


def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context