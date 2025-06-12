from django import forms
from .models import *

class UpdateGameScoresForm(forms.ModelForm):
  '''
  A form to update the details for a given game.
  '''
  #Stores the attributes for the given game.
  class Meta:
    model = GameScores
    fields = ['mock_mc', 'all_percent', 'all_rating', 'tc_percent', 'tc_rating', 'user_percent', 'user_rating', 'critics_consensus']


#Form used to manually create a user's profile form.
class CreateProfileForm(forms.ModelForm):
  '''A form to create Profile data.'''
  first_name = forms.CharField(label="First Name", required=True)
  last_name = forms.CharField(label="Last Name", required=True)
  city = forms.CharField(label="City", required=True)
  email_address = forms.CharField(label="Email Address", required=True)

  profile_image_url = forms.URLField(max_length=10000, label="Profile Image", required=True, widget=forms.TextInput(attrs={'placeholder': 'No URLs greater than 200 characters.', 'style': 'min-width: 150px; max-width: 500px; width: 190%;'}))

  class Meta:
    model = Profile
    fields = ['first_name','last_name','city','email_address','profile_image_url']

#Form used to manually update a user's profile form.
class UpdateProfileForm(forms.ModelForm):
  '''A form to update Profile data.'''
  city = forms.CharField(label="City", required=True)
  email_address = forms.CharField(label="Email Address", required=True)
  profile_image_url = forms.URLField(max_length=10000, label="Profile Image", required=True, widget=forms.TextInput(attrs={'placeholder': 'No URLs greater than 200 characters.', 'style': 'min-width: 150px; max-width: 500px; width: 190%;'}))

  class Meta:
    model = Profile 
    fields = ['city','email_address','profile_image_url']
