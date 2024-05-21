from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import User
# Create your views here.


def redirect_(request):
    # at url base it will redirect automatically to login/register url
    return redirect("login")


def login(request):
    # view that define the business logic of login request

    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get("username")).first()
        # check hashed password with DB
        if user and check_password(request.POST.get("password"), user.password):
            # define the session
            request.session['user_id'] = user.id
            return render(request, 'EliteDownload/cloud.html',
                          {'username': user.username})
        else:
            return render(request, 'EliteDownload/login.html',
                          {'error': 'Username o password non validi.'})

    return render(request, 'EliteDownload/login.html')

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'EliteDownload/register',
                          {"error", "Campi errati. Per favore, correggi i campi sottostanti."})
        else:
            # create a new user: password is hashed
            user = User.objects.create(
                username = request.POST.get("username"),
                name = request.POST.get("name"),
                surname = request.POST.get("surname"),
                password = make_password(request.POST.get("password")),
                email = request.POST.get("email"),
            )
            # save new User into DB
            user.save()
            messages.success(request, "Utente creato. Procedi ora con il login")
            return redirect("login")

    return render(request, 'EliteDownload/register.html')

def cloud(request):
    return render(request, 'EliteDownload/cloud.html')