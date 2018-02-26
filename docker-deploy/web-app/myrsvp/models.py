from django.db import models
from django.utils import timezone
from django.core import mail
#from django.contrib.auth.models import User
import datetime
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length = 100)
    #creater = models.CharField(max_length = 50,default=username)
    description = models.TextField(max_length = 1000)
    publish_date = models.DateTimeField(default=timezone.now)
    time = models.DateTimeField(blank=False, null=False, default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length = 100)
    email_subject = models.CharField(max_length = 20, null=True)
    email_message = models.TextField(max_length = 200,null=True) 
    owner_email = models.EmailField(null=True)
    vendor_email = models.CharField(max_length=200,null=True)
    guest_email = models.CharField(max_length=200,null=True)
    plus_one   =  models.NullBooleanField(default = True)
  
    def __str__(self):
        return self.title
        
    class Meta:
        permissions = (
            ("regist", "can regist for event"),
        )
      
        
class Question(models.Model):
    MULTICHOICE = 0
    TEXT = 1
    QUESTION_TYPE_CHOICES = (
        (MULTICHOICE, "multiple choice"),
        (TEXT, "text question"),
    )
    
    question = models.ForeignKey(Event,null = True,on_delete = models.CASCADE,related_name="question")
    description = models.TextField(max_length = 50,blank=True)
    question_type = models.IntegerField(default = MULTICHOICE, choices=QUESTION_TYPE_CHOICES)
    vendor_editable = models.NullBooleanField(default = True,blank=True)  
    vendor_permission = models.NullBooleanField(default = True,blank=True)
  
    def __str__(self) :
        return self.description        
        
class Choice(models.Model):
    choice = models.OneToOneField(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200,null=True)
    #user = models.ManyToManyField(User)

    def __str__(self) :
        return self.choice_text        
        
        
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name = "question_answer")
    answer = models.CharField(max_length = 200)
    finalize = models.NullBooleanField(default = False) #guest
    user = models.ForeignKey(User,null=True,on_delete = models.CASCADE,related_name="user")
  
    class Meta:
        permissions = (
            ("visibility", "can see answers"),
        )
  
    def __str__(self) :
        return self.answer
        
class RSVP(models.Model):   
    ATTEND = 'A'
    NOTATTEND = 'N'
    NOTDECIDE = 'D'
     
    ATTEND_OR_NOT = (
        (ATTEND, "attend"),
        (NOTATTEND, "sorry, cannot attend"),
        (NOTDECIDE,"have not decided yet"),
    )
    rsvp =  models.ForeignKey(Event,on_delete=models.CASCADE,null=True,related_name="rsvp")
    rsvp_choice = models.CharField(max_length=1,default = ATTEND, choices=ATTEND_OR_NOT)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="user_rsvp")
    class Meta:
        unique_together = (("rsvp", "user"),)
        
class PlusOne(models.Model):
    id = models.AutoField(primary_key=True)
    plus = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    plus_one = models.ForeignKey(Event,on_delete=models.CASCADE,null=True,related_name="event_plusone")
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="user_plusone")