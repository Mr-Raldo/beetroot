from rest_framework import serializers
from .models import (ArticleSharingTags, 
                     ResponseSection, 
                     ResponseQuestionnaire, 
                     QuestionnaireSection,
                     Answer, 
                     Response,
                     Feed,
                     FeedImage,
                     Comment,
                     Likes, 
                     DownVote                     
                     )

from akyc.models import (
    Profile
)
from akyc.serializers import ProfileSerializer
class QuestionnaireSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireSection
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'

class ResponseQuestionnaireSerializer(serializers.ModelSerializer):
    sections = ResponseSerializer(many=True)

    class Meta:
        model = ResponseQuestionnaire
        fields = ("id","responder","response_questionnaire","section_title","is_completed","sections")

class ResponseSectionSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True)
    class Meta:
        model = ResponseSection
        fields = ("id","questionnaire_section_id","questionnaire_id","responder","response_questionnaire","section_title","is_completed","responses")
class ArticleSharingTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleSharingTags
        fields = ("id","created_at","tagged_profile_id","article_id","tagged_profile_endorsed","endorsed_at")
       
       
class FeedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedImage
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    commenter = serializers.SerializerMethodField('get_commenter')
    class Meta:
        model = Comment
        fields = '__all__'
        
    def get_commenter(self, obj):
        commentr = obj.commenter
        author = Profile.objects.get(pk=commentr.profile_id)
        serializer = ProfileSerializer(author)
        return serializer.data  
          
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'
        
class DownVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownVote
        fields = '__all__'
                                                
class FeedSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    comments = serializers.SerializerMethodField('get_comments')
    likes = serializers.SerializerMethodField('get_likes')
    downvotes = serializers.SerializerMethodField('get_downvotes')
    author = serializers.SerializerMethodField('get_author')
    
    class Meta:
        model = Feed
        fields = '__all__'
        
    def get_author(self, obj):
        authr = obj.author
        author = Profile.objects.get(pk=authr.profile_id)
        serializer = ProfileSerializer(author)
        return serializer.data   
    def get_images(self, obj):
        images = FeedImage.objects.filter(feed=obj)
        serializer = FeedImageSerializer(images, many=True)
        return serializer.data

        
    def get_comments(self, obj):
        comments = Comment.objects.filter(feed=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data    
    
        
    def get_likes(self, obj):
        images = Likes.objects.filter(feed=obj)
        serializer = LikesSerializer(images, many=True)
        return serializer.data    
    
    def get_downvotes(self, obj):
        downvotes = DownVote.objects.filter(feed=obj)
        serializer = DownVoteSerializer(downvotes, many=True)
        return serializer.data        