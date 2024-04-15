
from django import forms
from akyc.models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','email','street_address','phone')
