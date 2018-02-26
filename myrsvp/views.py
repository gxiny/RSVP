from django.shortcuts import render,render_to_response,get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from .forms import *
from  django.contrib.auth.models import User
from .models import *
from django.core.mail import EmailMultiAlternatives
import socket,re
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from guardian.shortcuts import assign_perm, get_perms, remove_perm
from guardian.core import ObjectPermissionChecker
from guardian.decorators import permission_required


# Create your views here.
wrong_email = "The email format is wrong"
AnswerDoesNotExist = "This question has no answer"
have_regist = "You have responded to this event"
worng_login = "Your username or email or password is wrong"
worng_user = "The user is not alive"



class UserForm(forms.Form):
    username = forms.CharField(label = 'username',max_length=50)
    email = forms.CharField(label = 'email',max_length=50)
    password = forms.CharField(label = 'password',max_length=50,widget=forms.PasswordInput())
  

def regist(request):
    if request.method == 'POST':
        uf = SignUpForm(request.POST)
        if uf.is_valid():
            #get data
            uf.save()
            username = uf.cleaned_data.get('username')
            password = uf.cleaned_data.get('password1')
            first_name = uf.cleaned_data.get('first_name')
            last_name = uf.cleaned_data.get('last_name')
            email = uf.cleaned_data.get('email')
            return render(request,'rsvp/homepage.html',{'uf':uf})           
    else:
        uf = SignUpForm()
    return render (request,'rsvp/regist.html',{'uf':uf})

def signin(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
       # uf = UserCreationForm(request.POST)
        if uf.is_valid():
            #get username and password
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #compare with database
            #user = User.objects.filter(username__exact = username,password__exact = password)
        username = request.POST['username']
        raw_password = request.POST['password']
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/rsvp/home/')
            else:
                return render(request,'rsvp/wrong.html',{'wrong_message':worng_user})
        else:
            return render(request,'rsvp/wrong.html',{'wrong_message':worng_login})                    
    else:
        uf = UserForm()
    return render (request,'rsvp/login.html',{'uf':uf})


def signout(request):
    logout(request)
    return render(request,'rsvp/logout.html')

@login_required  
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit = False)
            time = form.cleaned_data['time']
            address = form.cleaned_data['address']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            #updated = form.cleaned_data['updated']
            email_subject = form.cleaned_data['email_subject']
            email_message = form.cleaned_data['email_message']
            owner_email = form.cleaned_data['owner_email']
            vendor_email = form.cleaned_data['vendor_email']
            guest_email = form.cleaned_data['guest_email']  
            event.save()
            ###########
            everyguest_email = guest_email.split(';')
            for guest_e in everyguest_email:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", guest_e) == None:
                    return render(request,'rsvp/wrong.html',{'wrong_message':wrong_email})                   
                if not User.objects.filter(email=guest_e).exists():
                    send_invitation(email_subject,email_message,owner_email,guest_e)
            return redirect('create_question',pk=event.pk)
        
    else:
        form = EventForm()
    return render(request, 'rsvp/create_event.html', {'form': form})
    
def send_invitation(email_subject,email_message,owner_email,guest_email):
    subject, from_email, to = email_subject, owner_email, guest_email
    text_content = "You have a new invitation. Rsgister for RSVP now"
    html_content = '<p>You have a new invitation. Register for RSVP system now</p >'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()  

@login_required    
def event_delete(request,pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('myevent') 


@login_required    
def event_edit(request,pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event.time = form.cleaned_data['time']
            event.address = form.cleaned_data['address']
            event.title = form.cleaned_data['title']
            event.description = form.cleaned_data['description']
            #updated = form.cleaned_data['updated']
            event.email_subject = form.cleaned_data['email_subject']
            event.email_message = form.cleaned_data['email_message']
            event.owner_email = form.cleaned_data['owner_email']
            event.vendor_email = form.cleaned_data['vendor_email']
            event.guest_email = form.cleaned_data['guest_email']  
            event.save()
            ###########
            everyguest_email = event.guest_email.split(';')
            for guest_e in everyguest_email:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", guest_e) == None:
                    return HttpResponseRedirect('/create_event/?message=wrong_email')                   
                if not User.objects.filter(email=guest_e).exists():
                    send_invitation(event.email_subject,event.email_message,event.owner_email,guest_e)
            return redirect('create_question',pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'rsvp/event_edit.html', {'form': form})
    
@login_required 
def create_question(request,pk):  
    event = get_object_or_404(Event,pk=pk)  
    if request.method == 'POST':
        question_form = QuestionForm(request.POST) 
        if question_form.is_valid():
            #get data
            #form.save()
            description = question_form.cleaned_data.get('description')
            question_type = question_form.cleaned_data.get('question_type')
            vendor_editable = question_form.cleaned_data.get('vendor_editable')
            vendor_permission = question_form.cleaned_data.get('vendor_permission')
            question = Question(
                question = event,
                description =  description,
                question_type = question_type,
                vendor_editable = vendor_editable,
                vendor_permission = vendor_permission,
                )
            question.save()
            if question_type == 0:
                return redirect('create_choice',event_pk=event.pk,question_pk=question.pk)
            return redirect('./')
            #return redirect('event_detail',pk=pk)
            #return render(request,'rsvp/create_event.html',{form':form})           
    else:
        question_form = QuestionForm()
    return render (request,'rsvp/create_question.html',{'question_form':question_form})

@login_required    
def question_delete(request,pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect('myevent') 

@login_required    
def question_edit(request,pk):
    q = get_object_or_404(Question, pk=pk)
    event = q.question
    if request.method == 'POST':
        question_form = QuestionForm(request.POST) 
        if question_form.is_valid():
            #get data
            #form.save()
            q.description = question_form.cleaned_data.get('description')
            q.question_type = question_form.cleaned_data.get('question_type')
            q.vendor_editable = question_form.cleaned_data.get('vendor_editable')
            q.vendor_permission = question_form.cleaned_data.get('vendor_permission')
            q.save()
            if q.question_type == 0:
                return redirect('create_choice',event_pk=event.pk,question_pk=q.pk)
            #####email
            everyguest_email = event.guest_email.split(';')
            for guest_e in everyguest_email:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", guest_e) == None:
                    return HttpResponseRedirect('/create_event/?message=wrong_email')                   
                if not User.objects.filter(email=guest_e).exists():
                    send_invitation(event.email_subject,event.email_message,event.owner_email,guest_e)
            return redirect('./')         
    else:
        question_form = QuestionForm()
    return render (request,'rsvp/create_question.html',{'question_form':question_form})

@login_required
def create_choice(request,event_pk,question_pk):
    question = get_object_or_404(Question,pk=question_pk)  
    event = get_object_or_404(Event,pk=event_pk)
    if request.method == 'POST':
        choice_form = ChoiceForm(request.POST) 
        if choice_form.is_valid():
            choice_text = choice_form.cleaned_data.get('choice_text')
            choice = Choice(
                choice = question,
                choice_text = choice_text,
                )
        choice.save()
        return redirect('create_question',pk=event.pk)
    else :
        choice_form = ChoiceForm()
    return render(request,'rsvp/create_choice.html',{'choice_form':choice_form})

@login_required
def rsvp(request,event_pk):
    event  = get_object_or_404(Event,pk = event_pk)
    if request.method == 'POST':
        form = RsvpForm(request.POST) 
        if form.is_valid():
            rsvp_choice = form.cleaned_data.get('rsvp_choice')
            rsvp = RSVP(
                rsvp = event,
                rsvp_choice = rsvp_choice,
                user = request.user,
                )
            try:
                rsvp.save()
            except :
                return render(request,'rsvp/wrong.html',{'wrong_message':have_regist})
            return redirect('../')
            
    else :
        form = RsvpForm()
    return render(request,'rsvp/rsvp.html',{'form':form,'event':event})  

@login_required
def plusone(request,event_pk):
    event  = get_object_or_404(Event,pk = event_pk)
    if request.method == 'POST':
        form = PlusoneForm(request.POST) 
        if form.is_valid():
            plus = form.cleaned_data.get('plus')
            plus_one = PlusOne(
                plus = plus,
                plus_one = event,
                user = request.user,
                )
            plus_one.save()
            return redirect('../')            
    else :
        form = PlusoneForm()
    return render(request,'rsvp/plusone.html',{'form':form,'event':event})  


@login_required
def vendor_view(request,pk):
    question = get_object_or_404(Question,pk=pk)
    allanswers = question.question_answer.all()        
    return render(request,'rsvp/vendor_view.html',{'allanswers':allanswers})

@login_required          
def homepage(request):
    username = request.user.username
    return render(request,'rsvp/homepage.html',{'username':username})
    
def test(request):
    #user = get_object_or_404(User, pk=pk)
    username = request.COOKIES.get('email','')
    return render(request,'rsvp/test.html',{'username':username})
    
@login_required    
def myevent(request):
    username = request.user.username
    email = request.user.email
    myevents = Event.objects.filter(owner_email = email).order_by('time')
    for event in myevents:
        assign_perm('change_event',request.user,event)
        assign_perm('delete_event',request.user,event)
        questionlist = event.question.all()
        for question in questionlist:
            assign_perm('change_question',request.user,question)
            assign_perm('delete_question',request.user,question)
    return render(request,'rsvp/my_event.html',{'myevents':myevents})

@login_required  
def vendorevent(request):
    username = request.user.username
    email = request.user.email
    vendorevents = []
    allevents = Event.objects.all()
    for event in allevents:
        vendor_email_list = event.vendor_email.split(';')
        for one_email in vendor_email_list:
            if email == one_email:
                vendorevents.append(event)
    for event in vendorevents:
        remove_perm('change_event', request.user,event)
        remove_perm('delete_event',request.user,event)
        questionlist = event.question.all()
        for question in questionlist:
            if question.vendor_editable:
                assign_perm('change_question',request.user,question)
            remove_perm('delete_question',request.user,question)         
    
    return render(request,'rsvp/vendor_event.html',{'vendorevents':vendorevents})

@login_required  
def guestevent(request):
    username = request.user.username
    email = request.user.email
    guestevents = []
    allevents = Event.objects.all()
    for event in allevents:
        guest_email_list = event.guest_email.split(';')
        for one_email in guest_email_list:
            if email == one_email:
                guestevents.append(event)
    
    for event in guestevents:
        remove_perm('change_event', request.user,event)
        remove_perm('delete_event',request.user,event) 
        assign_perm('regist',request.user,event)
        questionlist = event.question.all()
        for question in questionlist:
            remove_perm('change_question',request.user,question)
            remove_perm('delete_question',request.user,question)
            
    return render(request,'rsvp/guest_event.html',{'guestevents':guestevents})

@login_required
def event_detail(request,pk):
    event = get_object_or_404(Event,pk=pk)
    questionlist = event.question.all()
    for question in questionlist:
        des = question.description
        try:    
            answers = question.question_answer.all()
        except:
            return render(request,'rsvp/event_detail.html',{'event':event,'questionlist':questionlist})
            
        for answer in answers:
            if answer.finalize:
                questionlist = event.question.all().exclude(description = des)       
    return render(request,'rsvp/event_detail.html',{'event':event,'questionlist':questionlist})   

@login_required    
def question_detail(request,event_pk,question_pk):
    question = get_object_or_404(Question,pk=question_pk) 
    event    = get_object_or_404(Event,pk = event_pk)  
    if question.question_type == 1:
        if request.method == 'POST':
            form = TextResopnse(request.POST) 
            if form.is_valid():
                answer = form.cleaned_data.get('answer')
                finalize = form.cleaned_data.get('finalize')
                text_response = Answer(
                    question = question,
                    answer   = answer,
                    finalize = finalize,
                    user     = request.user,
                )
                text_response.save()
                return render(request,'rsvp/succeed.html',{'event':event})
        else :
            form = TextResopnse()
        return render(request,'rsvp/question_detail.html',{'form':form,'event':event,'question':question})

    else :
        choicelist = question.choice.choice_text.split(';')
        return render(request,'rsvp/question_detail.html',{'question':question,'event':event,'choicelist':choicelist})  
    return render(request,'rsvp/succeed.html')  

def succeed(request):
    return render(request,'rsvp/succeed.html',{'succeed':succeed}) 

def wrong(request):
    return render(request,'rsvp/wrong.html',{'wrong':wrong})  
  