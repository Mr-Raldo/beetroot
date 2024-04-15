from django.contrib import admin
from .models import (ResponseQuestionnaire, 
                     ResponseSection, 
                     QuestionPage, 
                     Answer, 
                     Response,
                     Feed,
                     FeedImage,
                     Comment,
                     Likes, 
                     DownVote  
                     )
from unfold.admin import ModelAdmin
from dashboards.sites import dashboards_admin_site


# admin.site.register(ResponseQuestionnaire, site=dashboards_admin_site)
@admin.register(ResponseQuestionnaire, site=dashboards_admin_site)
class ResponseQuestionnaireAdmin(ModelAdmin):
    empty_value_display = "-not-set-"
    list_display_links = [ "title"]
    # list_select_related = ["entreprenuer"]
    search_fields = ["title",]
    # inlines = [ServiceInline]

    list_display = [
                # "created_at",
        # "upper_case_name",
        "questionnaire_id",
        "title",
        "responder_name",
        "total_sections",
        "is_completed"
    ]

    @admin.display(description="Name")
    def upper_case_name(self,obj):
        return f"{obj.title}".upper()
    
    @admin.display(description="Responder Name/Email/ID")
    def responder_name(self,obj):
        item = obj.responder
        return f"email-{item.email} - ID-{item.id}"


    @admin.display(description="Total Sections")
    def total_sections(self,obj):
        item = obj.sections.count()
        return f"{item}".upper()
# admin.site.register(ResponseSection, site=dashboards_admin_site)
@admin.register(ResponseSection, site=dashboards_admin_site)
class ResponseSectionAdmin(ModelAdmin):
    empty_value_display = "-not-set-"
    list_display_links = [ "id", "section_title"]
    # list_select_related = ["entreprenuer"]
    search_fields = ["section_title",]
    # inlines = [ServiceInline]

    list_display = [
                # "created_at",
        # "upper_case_name",
        "id",
        "section_title",
        "questionnaire_title",
        "responder_name",
        "total_questions",
        "is_completed"
    ]

    @admin.display(description="Name")
    def upper_case_name(self,obj):
        return f"{obj.title}".upper()
    @admin.display(description="Responder Name/Email/ID")
    def responder_name(self,obj):
        item = obj.responder
        return f"email-{item.email} - ID-{item.id}"
    
    @admin.display(description="Total Questions")
    def total_questions(self,obj):
        item = obj.responses.count()
        return f"{item}".upper()
    
    @admin.display(description="Questionnaire Title")
    def questionnaire_title(self,obj):
        item = obj.response_questionnaire
        return f"{item.title}".capitalize()
    @admin.display(description="Responder Name/Email/ID")
    def responder_name(self,obj):
        item = obj.responder
        return f"email-{item.email} - ID-{item.id}"
    
@admin.register(Response, site=dashboards_admin_site)
class ResponseAdmin(ModelAdmin):
    empty_value_display = "-not-set-"
    list_display_links = [ "question", "upper_case_name"]
    # list_select_related = ["entreprenuer"]
    search_fields = ["section",]
    # inlines = [ServiceInline]

    list_display = [
                # "created_at",
        # "question",
        "question",
        "upper_case_name",
        "responder_name",
        "questionnaire_id",
    ]

    @admin.display(description="Section Title")
    def upper_case_name(self,obj):
        item = obj.section
        return f"{item.section_title}".capitalize()
    @admin.display(description="Responder Name/Email/ID")
    def responder_name(self,obj):
        item = obj.responder
        return f"email-{item.email} - ID-{item.id}"
    
@admin.register(Feed, site=dashboards_admin_site)
class FeedAdmin(ModelAdmin):
    empty_value_display = "-not-set-"
    list_display_links = [ "feed_text"]
    # list_select_related = ["entreprenuer"]
    search_fields = ["feed_text",]
    # inlines = [ServiceInline]

    list_display = [
                # "created_at",
        # "upper_case_name",
        "feed_text",
        # "Answernaire_id",
    ]

    @admin.display(description="Name")
    def upper_case_name(self,obj):
        author = obj.author
        return f"{author.first_name}".upper()