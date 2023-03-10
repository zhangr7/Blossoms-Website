import collections.abc

# 👇️ add attributes to `collections` module
# before you import the package that causes the issue
collections.MutableSequence = collections.abc.MutableSequence
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django import template
from .forms import RegisterUserForm, AthleteForm
from .models import Athlete
from teams.models import Teams
from django.http import HttpResponse
import re, csv
import os, sys
from decouple import config

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *


API_ID = config('API_ID')
TRANSACTION_KEY = config('TRANSACTION_KEY')

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('manage')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, "Could not find login credentials, try again")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            user.email = user.username
            user.save()
            login(request, user)
            messages.success(request, "Successfully registered!")
            return redirect('home')
        else:
            errors = ""
            for error in form.errors:
                errors += str(form.errors[error])
            errors = re.sub('<[^<]+?>', "", errors)
            errors = re.split('\.',errors)
            errors = ". ".join(errors)
            messages.error(request, "Registration unsuccessful: {}".format(errors))
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {
        'form': form
    })

def manage(request):
    athlete_list = Athlete.objects.filter(guardian=request.user)
    return render(request, 'manage.html', {'athlete_list': athlete_list})

def add_athlete(request):
    if request.method == "POST":
        form = AthleteForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            athlete = form.save()
            athlete.guardian = request.user
            athlete.save()
            return redirect('manage')
    form = AthleteForm
    return render(request, 'add_athlete.html', {'form': form})

def team_registration(request):
    if request.method == "POST":
        form = request.POST
        athlete = Athlete.objects.get(guardian=request.user, first_name=form['playerFirst'], last_name=form['playerLast'])
        team = Teams.objects.get(group=form['team'])
        athlete.team = team
        athlete.save(update_fields=['team'])
        token = getHostedPaymentPageRequest(form['fee'], form['team'])
        print(athlete.team)
        if request.user.is_authenticated:
            return render(request, 'team_registration.html', {
                'token': token
                })
    else:
        return redirect('manage')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Request"
                    plaintext = template.loader.get_template('password_reset_email.txt')
                    htmltemp = template.loader.get_template('password_reset_email.html')
                    c = {
                    "email":user.email,
                    'domain':'www.blossomswaterpolo.com',
                    'site_name': 'Blossoms Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https',
                    }
                    text_content = plaintext.render(c)
                    html_content = htmltemp.render(c)
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, 'District Blossoms <dev.blossomswpc@gmail.com>', [user.email], headers = {'Reply-To': 'dev.blossomswpc@gmail.com'})
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'An email with reset password instructions has been sent to your inbox. It may take a few minutes to receive.')
                    return redirect ("login")
            messages.error(request, 'We could not find an account associated with the entered email.')
    password_reset_form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form':password_reset_form})

def athlete_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=athletes.csv'
    # Create a csv writer
    writer = csv.writer(response)
    # Designate the model
    athletes = Athlete.objects.all()
    # Add column heading to csv file
    writer.writerow(['Name', 'Age', 'Team', 'Guardian'])
    # Loop thru athletes
    for athlete in athletes:
        writer.writerow([athlete.name, athlete.calculateAge()])
    return response


def getHostedPaymentPageRequest(amount, desc):
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = API_ID
    merchantAuth.transactionKey = TRANSACTION_KEY

    setting1 = apicontractsv1.settingType()
    setting1.settingName = apicontractsv1.settingNameEnum.hostedPaymentButtonOptions
    setting1.settingValue = "{\"text\": \"Pay\"}"

    setting2 = apicontractsv1.settingType()
    setting2.settingName = apicontractsv1.settingNameEnum.hostedPaymentOrderOptions
    setting2.settingValue = "{\"show\": true, \"merchantName\": \"District Blossoms Water Polo Club LLC\"}"

    setting3 = apicontractsv1.settingType()
    setting3.settingName = apicontractsv1.settingNameEnum.hostedPaymentReturnOptions
    setting3.settingValue = "{\"showReceipt\": true, \"cancelUrl\": \"https://www.blossomswaterpolo.com\", \"cancelUrlText\": \"Cancel\"}"

    setting4 = apicontractsv1.settingType()
    setting4.settingName = apicontractsv1.settingNameEnum.hostedPaymentStyleOptions
    setting4.settingValue = "{\"bgColor\": \"#5c86ad\"}"

    setting5 = apicontractsv1.settingType()
    setting5.settingName = apicontractsv1.settingNameEnum.hostedPaymentCustomerOptions
    setting5.settingValue = "{\"showEmail\": true, \"requiredEmail\": true, \"addPaymentProfile\": false}"

    setting6 = apicontractsv1.settingType()
    setting6.settingName = apicontractsv1.settingNameEnum.hostedPaymentPaymentOptions
    setting6.settingValue = "{\"cardCodeRequired\": true}"

    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(setting1)
    settings.setting.append(setting2)
    settings.setting.append(setting3)
    settings.setting.append(setting4)
    settings.setting.append(setting5)
    settings.setting.append(setting6)

    order = apicontractsv1.orderType()
    order.description = desc


    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount

    paymentPageRequest = apicontractsv1.getHostedPaymentPageRequest()
    paymentPageRequest.merchantAuthentication = merchantAuth
    paymentPageRequest.transactionRequest = transactionrequest
    paymentPageRequest.hostedPaymentSettings = settings

    paymentPageController = getHostedPaymentPageController(paymentPageRequest)

    paymentPageController.execute()

    paymentPageResponse = paymentPageController.getresponse()

    if paymentPageResponse is not None:
        if paymentPageResponse.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            print('Successfully got hosted payment page!')

            if paymentPageResponse.messages is not None:
                print('Message Code : %s' % paymentPageResponse.messages.message[0]['code'].text)
                print('Message Text : %s' % paymentPageResponse.messages.message[0]['text'].text)
        else:
            if paymentPageResponse.messages is not None:
                print('Failed to get batch statistics.\nCode:%s \nText:%s' % (paymentPageResponse.messages.message[0]['code'].text,paymentPageResponse.messages.message[0]['text'].text))

    return paymentPageResponse

if(os.path.basename(__file__) == os.path.basename(sys.argv[0])):
    getHostedPaymentPageRequest(5)
