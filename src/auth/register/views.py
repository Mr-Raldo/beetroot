from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from django.contrib.auth.models import  Group
from django.contrib import messages
from django.conf import settings
from auth.views import AuthView
from auth.helpers import send_verification_email
from akyc.models import Profile
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from akyc.serializers import ProfileSerializer

User = get_user_model()


class RegisterView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("index")  # Replace 'index' with the actual URL name for the home page

        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request):
        user_data_str = request.POST.get('user', '')

            # Convert the JSON string to a dictionary
        user_data = json.loads(user_data_str)
        print('user_data')
        print(user_data)

        username = user_data['first_name'] + ' ' + user_data['last_name']

        first_name = user_data['first_name']
        last_name = user_data['last_name']
        email = user_data['email']
        phone = user_data['phone']
        password = user_data['password']
        neighbourhood = user_data['neighbourhood']
        city = user_data['city']
        country = user_data['country']
        self_description = user_data['self_description']
        ideals = user_data['ideals']
        platform_joining_goals = user_data['platform_joining_goals']
        immeditiate_needs = user_data['immeditiate_needs']
        expected_experience = user_data['expected_experience']
        specialization = user_data['specialization']
        trading_as = user_data['trading_as']
        account_type = user_data['account_type']
        profile_image =  request.FILES.get('profile_image')

        # Check if a user with the same username or email already exists
        if User.objects.filter(username=username, email=email).exists():
            messages.error(request, "User already exists, Try logging in.")
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

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
        Profile.objects.create(
        user = created_user,
        first_name = user_data['first_name'],
        last_name = user_data['last_name'],
        email = user_data['email'],
        phone = user_data['phone'],
        gender = user_data['gender'],
        city = user_data['city'],
        country = user_data['country'],
        self_description = user_data['self_description'],
        ideals = user_data['ideals'],
        platform_joining_goals = user_data['platform_joining_goals'],
        immeditiate_needs = user_data['immeditiate_needs'],
        expected_experience = user_data['expected_experience'],
        specialization = user_data['specialization'],
        trading_as = user_data['trading_as'],
        account_type = user_data['account_type'],
        profile_image = profile_image
        )

        send_verification_email(email, token)

        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            messages.success(request, "Verification email sent successfully")
        else:
            messages.error(request, "Email settings are not configured. Unable to send verification email.")

        request.session['email'] = email ## Save email in session
        # Redirect to the verification page after successful registration
        return redirect("verify-email-page")


class CreateProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request,*args, **kwargs):
        user_data_str = request.data.get('user', '')  # Use request.data instead of request.POST
        try:
            user_data = json.loads(user_data_str)
        except json.JSONDecodeError:
            print('error', 'Invalid JSON data')
            return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
        profile_id = user_data.get('profile_id')
        print('profile_id')
        print(profile_id)
        if profile_id:
            try:
                profile_instance = Profile.objects.get(pk=int(profile_id))
            except Profile.DoesNotExist:
                return Response({'error': 'Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
            print('user_data')
            print(user_data)
            # Use serializer to update the profile_instance
            serializer = ProfileSerializer(profile_instance, data=user_data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                print('serializer.data')
                print(serializer.data)
                return Response({'user': json.dumps(serializer.data)}, status=status.HTTP_202_ACCEPTED)
            else:
                print('serializer.errors', serializer.errors)
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if not profile_id:
            user_data_str = request.POST.get('user', '')
                # Convert the JSON string to a dictionary
            user_data = json.loads(user_data_str)
            print('user_data')
            print(user_data)
            username = user_data['first_name'] + ' ' + user_data['last_name']

            first_name = user_data['first_name']
            last_name = user_data['last_name']
            email = user_data['email']
            phone = user_data['phone']
            password = user_data['password']
            neighbourhood = user_data['neighbourhood']
            city = user_data['city']
            country = user_data['country']
            self_description = user_data['self_description']
            immeditiate_needs = user_data['immeditiate_needs']
            trading_industry = user_data['trading_industry']
            community_role = user_data['community_role']
            business_role = user_data['business_role']
            business_name = user_data['business_name']
            profile_image_url = user_data['profile_image_url']
            specialization = user_data['specialization']
            trading_as = user_data['trading_as']
            account_type = user_data['account_type']
            profile_image =  request.FILES.get('profile_image')
        # Create the user and set their password
            created_user = User.objects.create_user(username=username, email=email, password=password)
            created_user.set_password(password)
            created_user.save()
            if created_user:
                print('created_user', created_user)
                # Add the user to the 'client' group (or any other group you want to use as default for new users)
                user_group, created = Group.objects.get_or_create(name="client")
                created_user.groups.add(user_group)
                print('user_group, created')
                print(user_group, created)

            # Generate a token and send a verification email here
            token = str(uuid.uuid4())
            print('token', token)
            # Set the token in the user's profile
            # Check if a user with the same username or email already exists
            if Profile.objects.filter(user=created_user, email=email).exists():
                print('User already exists, Try logging in.')
                messages.error(request, "User already exists, Try logging in.")
                return redirect("register")
            elif Profile.objects.filter(email=email).exists():
                print('Email already exists.')
                messages.error(request, "Email already exists.")
                return redirect("register")
            elif Profile.objects.filter(phone=phone).exists():
                messages.error(request, "Username already exists.")
                print('Username already exists.')
                return redirect("register")
            profile_instance = Profile.objects.create(
            user = created_user,
            first_name = first_name,
            last_name = last_name,
            email_token = token,
            email = email,
            phone = phone,
            city = city,
            neighbourhood = neighbourhood,
            country = country,
            self_description = self_description,
            specialization = specialization,
            immeditiate_needs = immeditiate_needs,
            trading_industry = trading_industry,
            community_role = community_role,
            business_role = business_role,
            business_name = business_name,
            trading_as = trading_as,
            account_type = account_type,
            # profile_image = profile_image
            profile_image_url=profile_image_url
            )
            if profile_instance:
                print('profile_instance',profile_instance )

                send_verification_email(email, token)

                if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                    messages.success(request, "Verification email sent successfully")
                else:
                    messages.error(request, "Email settings are not configured. Unable to send verification email.")

                request.session['email'] = email ## Save email in session
                serializer = ProfileSerializer(profile_instance)
                print('json.dumps(serializer.data)')
                print(json.dumps(serializer.data))
            return Response({'user': json.dumps(serializer.data)},status=status.HTTP_201_CREATED)
