from django.urls import include,path
from .views import UsersView
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import users_list, user_detail
from akyc.profile.profile_list.views import ProfileListView, ProfileList
from akyc.profile.profile_add.views import ProfileAddView
from akyc.profile.profile_update.views import ProfileUpdateView
from akyc.profile.profile_delete.views import ProfileDeleteView
from akyc.profile.profile_detail.views import  profileDetailView
from akyc.firebase_api import profile_to_firebase, sendMessage
from rest_framework import routers
router = routers.SimpleRouter()
urlpatterns = [
    path('sendMessage', sendMessage, name='sendMessage'),
    
    path('profile_to_firebase',profile_to_firebase, name='profile_to_firebase'),
    path('users-list', users_list, name='users-list'),
    path(
        "akyc/profiles/add/",
        login_required(ProfileAddView.as_view(template_name="app_user_view_add_profile.html")),
        name="akyc-profiles-add",
    ),
    path(
        "akyc/profiles/",
        login_required(ProfileListView.as_view(template_name="app_user_profile_list.html")),
        name="akyc-profiles",
    ),
    path(
        "akyc/profiles/list/",
        login_required(ProfileList.as_view(template_name="profile/profile_all.html")),
        name="akyc-profiles-list",
    ),
    path (
        "akyc/profiles/detail/<int:pk>",
        login_required(ProfileUpdateView.as_view(template_name="profiles/profile_update.html")),
        name="akyc-profiles-detail",
    ),
    path(
        "akyc/profiles/details/overview/<int:pk>",
        login_required(profileDetailView.as_view(template_name="profile/profile_details_overview.html")),
        name="akyc-profiles-details-overview",
    ),
    path (
        "akyc/profiles/update/<int:pk>",
        login_required(ProfileUpdateView.as_view(template_name="profiles/profile_update.html")),
        name="akyc-profiles-update",
    ),
    path (
        "akyc/profiles/delete/<int:pk>/",
        login_required(ProfileDeleteView.as_view()),
        name="akyc-profiles-delete",
    ),
    path(
        "app/user/list/",
        login_required(UsersView.as_view(template_name="app_user_list.html")),
        name="app-user-list",
    ),
    path(
        "users/",users_list
    ),
    path(
        "users/<int:id>",user_detail
    ),
    path(
        "app/user/view/account/",
        login_required(UsersView.as_view(template_name="app_user_view_account.html")),
        name="app-user-view-account",
    ),
    path(
        "app/user/view/security/",
        login_required(UsersView.as_view(template_name="app_user_view_security.html")),
        name="app-user-view-security",
    ),
    path(
        "app/user/view/billing/",
        login_required(UsersView.as_view(template_name="app_user_view_billing.html")),
        name="app-user-view-billing",
    ),
    path(
        "app/user/view/notifications/",
        login_required(UsersView.as_view(template_name="app_user_view_notifications.html")),
        name="app-user-view-notifications",
    ),
    path(
        "app/user/view/connections/",
        login_required(UsersView.as_view(template_name="app_user_view_connections.html")),
        name="app-user-view-connections",
    ),

]

urlpatterns = format_suffix_patterns(urlpatterns)
