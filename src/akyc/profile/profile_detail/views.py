from django.views.generic import TemplateView
from django.db.models import Q
from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project import TemplateLayout
from akyc.models import Profile

class profileDetailView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['profile'] = self.get_profile(self.kwargs['pk'])
        return context
    def get_profile(self, pk):
        return Profile.objects.get(pk=pk)
