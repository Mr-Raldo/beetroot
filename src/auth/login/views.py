from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
# from backend import User
from django.contrib import messages
from auth.views import AuthView
from rest_framework.viewsets import ModelViewSet
from akyc.serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from akyc.models import Profile
import json
from rest_framework.authtoken.models import Token

User = get_user_model()
class LoginView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("index")  # Replace 'index' with the actual URL name for the home page

        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request):
        if request.method == "POST":
            username = request.POST.get("email-username")
            password = request.POST.get("password")

            if not (username and password):
                messages.error(request, "Please enter your username and password.")
                return redirect("login")

            if "@" in username:
                user_email = User.objects.filter(email=username).first()
                if user_email is None:
                    messages.error(request, "Please enter a valid email.")
                    return redirect("login")
                username = user_email.username

            user_email = User.objects.filter(username=username).first()
            if user_email is None:
                messages.error(request, "Please enter a valid username.")
                return redirect("login")

            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                # Login the user if authentication is successful
                login(request, authenticated_user)

                # Redirect to the page the user was trying to access before logging in
                if "next" in request.POST:
                    return redirect(request.POST["next"])
                else: # Redirect to the home page or another appropriate page
                    return redirect("index")
            else:
                messages.error(request, "Please enter a valid username.")
                return redirect("login")

class SigninViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    def create(self, request):
        if request.method == "POST":
            username = ''
            email = ''
            password = ''
            print('request. request.data',request.data)
            if request.data['email'] is not None:
                email = request.data['email']
            else:
                email = request.data['phone'] + '@geza.co.zw'
            password = request.data['password']
            print('request.method == "POST"')
            print(email, password)
            if not (email and password):
                messages.error(request, "Please enter your credentials.")
                return redirect("login")

            if "@" in email:
                print('"@" in email',email)
                user = User.objects.filter(email=email).first()

                if user is None:
                    messages.error(request, "Please enter a valid email.")
                    return Response(status=status.HTTP_404_NOT_FOUND)
                username = user.username

            print('username', username)
            user = User.objects.filter(username=username).first()
            print('user', user)

            if user is None:
                messages.error(request, "Please enter a valid username.")
                return Response(status=status.HTTP_404_NOT_FOUND)

            authenticated_user = authenticate(request, username=username, password=password)
            print('user', authenticated_user)
            if authenticated_user is not None:
                print('authenticated_user is not None', authenticated_user)

                # Login the user if authentication is successful
                res = login(request, authenticated_user)
                try:
                    user = Profile.objects.get(user=authenticated_user)
                    serializer = ProfileSerializer(user)
                    token, created = Token.objects.get_or_create(user=authenticated_user)
                    if token is not None:
                        authRes = {
                            'token':token.key if not created else token.key,
                            'profile': json.dumps(serializer.data),
                        }
                        print('login token',authRes)
                        return Response(authRes,status=status.HTTP_202_ACCEPTED)
                except Profile.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            else:
                print('authenticated_user is None')
                messages.error(request, "Please enter a valid username.")
                return redirect("login")