from django.shortcuts import render, redirect
from .forms import EmailForm, SignupForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'mailer/signup.html', {'form': form})


def sendMail(request):
    messageSent = False
    form = EmailForm()
    template_name = 'mailer/index.html'
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = "Sending an email with Django"
            message = cd['message']
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, [cd['recipient']])
            messageSent = True

    context = {'form':form, 'messageSent':messageSent}
    return render(request, template_name, context)


    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def loginView(request):
    template_name = 'mailer/login.html'
    if request.method == 'POST':
        u = request.POST.get('uname')
        p = request.POST.get('pw')
        user = authenticate(username=u, password=p)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('sendmail_url')
    context = {}
    return render(request, template_name, context)


def logoutView(request):
    logout(request)
    return redirect('login_url')