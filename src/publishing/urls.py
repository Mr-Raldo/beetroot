
# urls.py
from django.urls import path
from . import views 

urlpatterns = [
    path('feeds/', views.feeds, name='feeds'),
    path('comment/', views.comments, name='comment'),
    path('get_entreprenuer_public_feeds/<int:profile_id>/', views.get_entreprenuer_public_feeds, name='get_entreprenuer_public_feeds'),

    path('submit_response/', views.submit_response, name='submit_response'),
    path('submit_questionnaire_section/', views.submit_questionnaire_section, name='submit_questionnaire_section'),
    path('tag-article/', views.submit_tagged_profiles, name='tag-article'),
]
