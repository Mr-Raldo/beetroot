#views.py

from django.shortcuts import render, redirect
from .forms import ResponseForm
from .serializers import QuestionnaireSectionSerializer, ResponseSerializer, ResponseSectionSerializer, ResponseQuestionnaireSerializer
from .models import (
                    Response as QuestionnaireResponse,
                     ArticleSharingTags, 
                     Answer, 
                     QuestionnaireSection, 
                     ResponseSection, 
                     ResponseQuestionnaire,
                     Feed, FeedImage, Comment, Likes, DownVote
                     )
from akyc.models import Profile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from .serializers import (ArticleSharingTagsSerializer,
                          FeedSerializer,
                          FeedImageSerializer)
import json
User = get_user_model()

def submit_response(request):
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or return a success message
            return redirect('questionnaire_page.html')  # Replace 'success_page' with the actual name of your success page URL
    else:
        form = ResponseForm()
    return render(request, 'questionnaire_page.html', {'form': form})


@api_view(['GET'])
def get_entreprenuer_public_feeds(request,profile_id ):
        print('profile_id')
        author = Profile.objects.get(pk=profile_id)
        feeds = Feed.objects.filter(author=author, is_published=True)
        serializer = FeedSerializer(feeds, many=True)
        print(json.dumps(serializer.data))
        return Response({'feeds':json.dumps(serializer.data)}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def comments(request):
    if request.method == "POST":
        print('request.data')
        print(request.data)
        feed_id = request.data['feed_id']
        commenter_id = request.data['commenter_id']
        comment_text = request.data['comment']
        commenter = Profile.objects.get(pk=commenter_id)
        feed = Feed.objects.get(id=feed_id)
        is_published  = False
        if request.data['is_draft'] == False:
           is_published = True
        Comment.objects.get_or_create(
            feed=feed,
            commenter=commenter,
            comment_text = comment_text,
            is_published = is_published,
            is_trending = False
        )
        feed_instance = Feed.objects.get(id=feed.id)
        serializer = FeedSerializer(feed_instance)
        print('feed_serializer', serializer.data)
        return Response({'feed':json.dumps(serializer.data)}, status=status.HTTP_201_CREATED)    

@api_view(['GET', 'POST'])
def feeds(request):
    if request.method == "POST":
        print('request.data')
        print(request.data)
        profile_id = request.data['profile_id']
        feed_text = request.data['feed_text']
        author = Profile.objects.get(pk=profile_id)
        is_published  = False
        if request.data['is_draft'] == False:
           is_published = True
        feed, created = Feed.objects.get_or_create(
            author=author,
            feed_text = feed_text,
            is_published = is_published,
            is_trending = False
        )
        print('feed, created')
        print(feed, created)
        feed_instance = Feed.objects.get(id=feed.id)
        if created:
            if request.data['has_media'] == True:
                feed_images_urls = request.data['feed_images_urls']
                print('feed_images_urls')
                print(feed_images_urls)
                for url in feed_images_urls:
                    FeedImage.objects.create(
                        feed = feed_instance,
                        image_url = url
                    )
            serializer = FeedSerializer(feed_instance)
            print('feed_serializer', serializer.data)
            return Response({'feed':json.dumps(serializer.data)}, status=status.HTTP_201_CREATED)
        
        serializer = FeedSerializer(feed_instance)
        print('feed_serializer', serializer.data)
        return Response({'feed':json.dumps(serializer.data)}, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "GET":         
        if  request.data['feed_id']:
            feed_instance = Feed.objects.get(id=int(request.data['feed_id']))
            # Serialize the Service object with nested ServiceImage serialization
            serializer = FeedSerializer(feed_instance)
            print('feed_serializer', serializer.data)
            return Response({'feed':json.dumps(serializer.data)}, status=status.HTTP_200_OK)
            
   
                
@api_view(['GET', 'POST'])
def submit_questionnaire_section(request):
    if request.method == "POST":
        print('Post method request.data',request.data )
        print('Post method request.data',request.data['questionaire_id'] )
        # questionnaire_section_id
        questionaire_id = request.data['questionaire_id']
        questionaire_title = request.data['questionaire_title']
        section_title = request.data['answeredQuestionnaireSection']['section_title']
        questionnaire_section_id = request.data['answeredQuestionnaireSection']['id']
        responder_id = int(request.data['owner'])
        print('responder_id', responder_id)
        responder = User.objects.get(pk=responder_id)
        response_questionnaire, created = ResponseQuestionnaire.objects.get_or_create(questionnaire_id=questionaire_id,
                                                                                      title=questionaire_title,
                                                                                      responder=responder,
                                                                                      is_completed=False)
        section, created = ResponseSection.objects.get_or_create(
                                                        response_questionnaire=response_questionnaire, 
                                                        responder=responder,
                                                        questionnaire_id=questionaire_id,
                                                        questionnaire_section_id=questionnaire_section_id,
                                                        section_title=section_title)
        print('responder', responder)
        checkExistingResponseSection = ResponseSection.objects.filter(pk = section.id, is_completed=True).exists()
        if checkExistingResponseSection:
            print('QuestionnaireResponse Does Exist')
            # response = ResponseSection.objects.get(pk = section.id)
            # serializer = ResponseSectionSerializer(response)
            # print('serializer.data',json.dumps(serializer.data) )

            # return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)
            response = ResponseSection.objects.get(pk = section.id)
            serializer = ResponseSectionSerializer(response)
            print('serializer.data',json.dumps(serializer.data) )
            return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)

        print('QuestionnaireResponse.DoesNotExist')
        for qsn in request.data['answeredQuestionnaireSection']['questions']:
            response, created = QuestionnaireResponse.objects.get_or_create(
                    responder=responder,
                    questionnaire_id = questionaire_id,
                    section = section,
                    question = qsn['question'],
                    response = qsn['answer'],
            )
            print(response, created)
        if created:
                section.is_completed = True
                section.save()
                response = ResponseSection.objects.get(pk = section.id)
                serializer = ResponseSectionSerializer(response)
                print('serializer.data',json.dumps(serializer.data) )
                return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)

        return Response({'message': 'Invalid HTTP method'})
    if request.method == "GET":
         res = QuestionnaireResponse.objects.all()
         serializer = QuestionnaireSectionSerializer(res, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def submit_tagged_profiles(request):
    if request.method == "POST":
        print('request.data article_id',request.data['article_id'] )
        print('request.data tags',request.data['tags'] )
        article_id = request.data['article_id']
        tags = request.data['tags'] 
        for tag in request.data['tags']:
            print('tag',tag)
            article_tags, created = ArticleSharingTags.objects.get_or_create(
                    article_id = article_id,
                    tagged_profile_id=tag
            )
            print(article_tags, created)
        if created:
                response = ArticleSharingTags.objects.filter(article_id = article_id)
                serializer = ArticleSharingTagsSerializer(response, many=True)
                print('serializer.data',json.dumps(serializer.data) )
                return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)


        return Response({'message': 'Invalid HTTP method'})
    if request.method == "GET":
         res = QuestionnaireResponse.objects.all()
         serializer = QuestionnaireSectionSerializer(res, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
