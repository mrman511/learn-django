from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['first_name', 'email', 'username', 'password1', 'password2']
    labels = {
      'first_name': 'Name',
      
    }
    # widgets ={ 
    #   'tags': forms.CheckboxSelectMultiple(),
    # }
    

  def __init__(self, *args, **kwargs):
    super(CustomUserCreationForm, self).__init__(*args, **kwargs)
    # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Title'})
    # self.field['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Description'})
    # self.field['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Description'})

    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})

  #   #fields = '__all__'

class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = [
      'name', 
      'email', 
      'username', 
      'location', 
      'bio', 
      'short_intro', 
      'profile_image', 
      'social_github',
      'social_linkedIn',
      'social_twitter',
      'social_youtube',
      'social_website',
      ]

class SkillForm(ModelForm):
  class Meta:
    model= Skill
    fields = ['name', 'description']

class MessageForm(ModelForm):
  class Meta:
    model = Message
    fields = [
      'subject',
      'body',
    ]

    labels = {
      'subject': 'Your message subject here',
      'body': 'Your message here',
    }

  def __init__(self, *args, **kwargs):
    super(MessageForm, self).__init__(*args, **kwargs)
    # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Title'})
    # self.field['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Description'})
    # self.field['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Description'})

    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})  

