from django import forms
from django.forms import ModelForm,modelformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class SignUpForm(UserCreationForm): #UserCreationForm
    username   =  forms.CharField(max_length=50)
    first_name = forms.CharField()
    last_name  = forms.CharField()
    password1  = forms.CharField(widget=forms.PasswordInput())
    password2  = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','first_name','last_name','password1', 'password2','email')
        def __init__(self,*args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)

ACCEPT = (
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe'),
        ('no_rsvp', 'Hasn\'t RSVPed yet')
    )
    
class EventForm(forms.ModelForm):
    title = forms.CharField(max_length = 50)
    description = forms.TextInput(attrs={'cols' : "50", 'rows': "4", })
    #publish_date = forms.DateTimeField()
    time = forms.DateTimeField()
    #updated = forms.DateField()
    address = forms.CharField(max_length = 50)
    email_subject = forms.CharField(max_length = 20)
    email_message = forms.TextInput(attrs={'cols' : "50", 'rows': "4", })
    guest_email = forms.CharField(label="guest emails(seperate name by ';' eg:xg41@duke.edu;my@gmail.com)",widget = forms.Textarea)
    vendor_email = forms.CharField(label="vendor emails(seperate name by ';' eg:xg41@duke.edu;my@gmail.com)",widget = forms.Textarea)
    owner_email = forms.EmailField()
    plus_one   =  models.NullBooleanField()
    class Meta:
        model = Event
        fields = ('title','description','publish_date','time','updated','address','email_subject','email_message','guest_email','vendor_email','owner_email','plus_one')


class QuestionForm(forms.ModelForm):
    description = forms.CharField(widget = forms.Textarea)
    #question_type = forms.CharField() 
    vendor_editable = forms.NullBooleanField()  
    vendor_permission = forms.NullBooleanField()
    class Meta:
        model = Question
        fields = ('description','question_type','vendor_editable','vendor_permission')
 
class ChoiceForm(forms.ModelForm):
    choice_text = forms.CharField(label="multi choices(seperate name by ';' eg:banana;apple)",widget = forms.Textarea)
    class Meta:
        model = Choice
        fields=('choice_text',)     
        
class TextResopnse(forms.ModelForm):
    answer = forms.CharField(widget = forms.Textarea)
    finalize = forms.NullBooleanField() #guest
    class Meta:
        model = Answer
        fields=('answer','finalize')
        
class RsvpForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields=['rsvp_choice']

class PlusoneForm(forms.ModelForm):
    class Meta:
        model = PlusOne
        fields=['plus']