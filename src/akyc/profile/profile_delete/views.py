from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView
from django.contrib import messages
from akyc.models import Profile
from django.contrib.auth.mixins import PermissionRequiredMixin

class ProfileDeleteView(PermissionRequiredMixin, DeleteView):

    permission_required = ("profiles.delete_profile")

    def get(self, request, pk):
        profile = get_object_or_404(Profile, id=pk)
        profile.delete()
        messages.success(request, 'Transaction Deleted')
        return redirect('profiles')
