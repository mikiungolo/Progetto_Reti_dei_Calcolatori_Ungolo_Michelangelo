from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'EliteDownload/login.html')

def register(request):
    return render(request, 'EliteDownload/register.html')

def download(request):
    return render(request, 'EliteDownload/cloud.html')