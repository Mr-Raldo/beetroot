from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.views.generic import TemplateView
from web_project import TemplateLayout
from akyc.profile.profile_forms import ProfileForm
from akyc.models import Profile
from django.contrib.auth.mixins import PermissionRequiredMixin

class ProfileUpdateView(PermissionRequiredMixin, TemplateView):
    permission_required = ("profile.update_profile")

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['profile_id'] = self.get_profile(self.kwargs['pk'])
        return context

    def post(self, request, pk):
        profile = self.get_profile(pk)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            if not self.profile_exists(form.cleaned_data, profile):
                form.save()
                messages.success(request, 'Profile Updated')
            else:
                messages.error(request, 'Profile Already Exists')
        else:
            messages.error(request, 'Adding Profile Failed')
        return redirect('profiles')

    def get_profile(self, pk):
        return Profile.objects.get(pk=pk)

    def profile_exists(self, cleaned_data, current_profile):
        matching_profiles = Profile.objects.filter(
            Q(customer__iexact=cleaned_data['profile'])
        ).exclude(pk=current_profile.pk)
        return matching_profiles.exists()
