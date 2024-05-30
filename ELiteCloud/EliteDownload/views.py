from datetime import datetime

import pyotp
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm
from .models import User, File
from .service import send_otp


# Create your views here.

def redirect_(request):
    # at url base it will redirect automatically to login/register url
    return redirect("login")


def login(request):
    # view that define the business logic of login request
    error_message = None

    if ("username" and "email") in request.session:
        del request.session["username"], request.session["email"]

    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get("username")).first()
        # check hashed password with DB
        if user and check_password(request.POST.get("password"), user.password):
            # define the session
            request.session["username"] = user.username
            request.session["email"] = user.email
            send_otp(request)

            return redirect("otp")
        else:
            error_message = "Username o password non validi."

    return render(request, 'EliteDownload/login.html',
                  {'message': error_message, 'title': 'Login'})


def register(request):
    error_message = None

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            error_message = "Campi errati. Per favore, correggi i campi sottostanti."
        else:
            username = request.POST.get("username")
            email = request.POST.get("email")
            user_ex_username = User.objects.filter(username = username).first()
            user_ex_email = User.objects.filter(email=email).first()

            if not user_ex_email:
                if not user_ex_username:
                    # create a new user: password is hashed
                    user = User.objects.create(
                        username = username,
                        name = request.POST.get("name"),
                        surname = request.POST.get("surname"),
                        password = make_password(request.POST.get("password")),
                        email = email,
                    )
                    # save new User into DB
                    user.save()
                    error_message = "Utente creato. Procedi ora con il login"
                    return redirect("login")
                else:
                    error_message = "Username già esistente. Digitare un nuovo username."
            else:
                error_message = "Email già presente. Digitare una mail diversa."

    return render(request, 'EliteDownload/register.html',
                  {'message': error_message, 'title': 'Registrazione'})


# check 2FA after first factor
def otp(request):
    error_message = None

    if request.method == 'POST':
        otp_insert = request.POST["code"]

        # get info to session
        otp_valid_code = request.session["otp_code"]
        otp_date = request.session["otp_date"]

        # check values
        if otp_valid_code and otp_date is not None:
            otp_date = datetime.fromisoformat(otp_date)
            if otp_date > datetime.now():
                # validate otp
                otp_obj = pyotp.TOTP(otp_valid_code, interval = 60)
                if otp_obj.verify(otp_insert):
                    # delete otp informations
                    del request.session["otp_code"], request.session["otp_date"]
                    # user authenticate
                    return redirect("cloud")
                else:
                    error_message = "Codice OTP errato. Reinserisci il codice."
            else:
                error_message = "Tempo scauduto. Devi ripetere la procedura di autenticazione."
        else:
            error_message = "Ripetere la procedura. C'è qualcosa che non ha funzionato."

    return render(request, 'EliteDownload/otp.html',
                  {'title': 'Verifica OTP', 'message': error_message})


# cloud view shows files in DB
def cloud(request):

    cloud = File.objects.all()
    return render(request, 'EliteDownload/cloud.html',
                  {'username': request.session["username"], 'cloud': cloud})


# business logic for download request file
def download(request, file_id):
    # get info of selected path and its path
    file = get_object_or_404(File, pk = file_id)
    file_path = file.file.path
    # open file in read mode and assign Content for downlaod
    response = FileResponse(open(file_path, "rb"))
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = f'attachment; filename="{file.name}"'
    return response