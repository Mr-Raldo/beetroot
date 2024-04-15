from datetime import date
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
from web_project import TemplateLayout
from akyc.profile.profile_forms import ProfileForm
from akyc.models import Profile
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.conf import settings
import json
from auth.helpers import send_verification_email
from akyc.models import Profile
import uuid
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from akyc.serializers import ProfileSerializer

class ProfileAddView(PermissionRequiredMixin, TemplateView):
    permission_required = ("profiles.add_profile")

    def get_context_data(self, **kwargs):
        form = ProfileForm()
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['current_date'] = date.today().strftime("%Y-%m-%d")
        context['form'] = form
        return context

    def post(self, request):
        form = ProfileForm(request.POST)
        print('ProfileAddView form', request.POST)
        if form.is_valid():
            print('form is valid')
            print('form.cleaned_data', form.cleaned_data)
            user_data = form.cleaned_data
            print('user_data')
            print(user_data)
            username = user_data['first_name'] + ' ' + user_data['last_name']
            password = user_data['phone']
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            email = user_data['email']
            phone = user_data['phone']
            password = password
            # neighbourhood = user_data['neighbourhood']
            # city = user_data['city']
            # country = user_data['country']
            # self_description = user_data['self_description']
            # specialization = user_data['specialization']
            # trading_as = user_data['trading_as']
            # account_type = user_data['account_type']
            # profile_image =  request.FILES.get('profile_image')
        # Create the user and set their password
            created_user = User.objects.create_user(username=username, email=email, password=password)
            created_user.set_password(password)
            created_user.save()
            # Add the user to the 'client' group (or any other group you want to use as default for new users)
            user_group, created = Group.objects.get_or_create(name="client")
            created_user.groups.add(user_group)

            # Generate a token and send a verification email here
            token = str(uuid.uuid4())
            # Set the token in the user's profile
            # Check if a user with the same username or email already exists
            if Profile.objects.filter(user=created_user, email=email).exists():
                messages.error(request, "User already exists, Try logging in.")
                return redirect("register")
            elif Profile.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return redirect("register")
            elif Profile.objects.filter(phone=phone).exists():
                messages.error(request, "Username already exists.")
                return redirect("register")
            profile_instance = Profile.objects.create(
            user = created_user,
            first_name = first_name,
            last_name = last_name,
            email_token = token,
            email = email,
            phone = phone,
            # city = city,
            # neighbourhood = neighbourhood,
            # country = country,
            # self_description = self_description,
            # specialization = specialization,
            # trading_as = trading_as,
            # account_type = account_type,
            # profile_image = profile_image
            )
            # send_verification_email(email, token)

            # if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            #     messages.success(request, "Verification email sent successfully")
            # else:
            #     messages.error(request, "Email settings are not configured. Unable to send verification email.")

            # request.session['email'] = email ## Save email in session
            # serializer = ProfileSerializer(profile_instance)
        else:
            print('form is not valid')
            messages.error(request, 'Profile Failed')
        return redirect('/akyc/profiles/')

    def profile_exists(self, cleaned_data):
        return Profile.objects.filter(
            customer__iexact=cleaned_data['profile'],
        ).exists()
