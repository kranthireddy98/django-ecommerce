
from django.shortcuts import redirect, render

from django.contrib import messages,auth

from .models import Account

from .form import RegistrationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.creat_user(
                first_name=first_name,last_name=last_name,email=email,password=password,username=username
            )
            user.phone_number = phone_number
            user.save()
            #user activation
            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message      = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain' : current_site,
                'uid'    : urlsafe_base64_encode(force_bytes(user.pk)),
                'token'  : default_token_generator.make_token(user)

            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Thank you Registering for us. click on link sent in the email to activate your account.')

            

            return redirect('/accounts/login?command=verification&email='+email)
    
    else:
        form = RegistrationForm()

    context = {
        'form' : form
    }
    return render(request,'accounts/register.html',context)


def login(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user  = auth.authenticate(email=email,password=password)

        if user:
            auth.login(request,user)
            messages.success(request,'you are logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid Login credentials')
            return redirect('login')
   
    # if request.user.is_authenticated:
    #     return redirect('home')
    return render(request,'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
   
    messages.success(request,'you are logged out')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user  = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation your account is activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link')
        return redirect('register')

@login_required(login_url= 'login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

def forgotPassword(request):
    if request.method ==  'POST':
        email = request.POST['email']
        
        if Account.objects.filter(email=email).exists:
            user = Account.objects.get(email__iexact = email)
            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message      = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain' : current_site,
                'uid'    : urlsafe_base64_encode(force_bytes(user.pk)),
                'token'  : default_token_generator.make_token(user)

            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
           

            messages.success(request,'password email has been sent to your email Address')
            return redirect('login')
        else:
            messages.error(request,'Account does not exists')
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user  = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'please reset your Password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('forgotPassword')
     

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Successfully Changed')
            return redirect('login')
            
        else:
            messages.error(request,'Password does not match')
            return redirect('resetPassword')
            
    else:
        return render(request,'accounts/reset_password.html')
