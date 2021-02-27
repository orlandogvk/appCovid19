#https://whaleandjaguar.co/

from django.shortcuts import render, redirect

# Create your view here
from .forms import CreateUserForm
import requests

#Api COVID
import json
# Auth
from django.views.decorators.csrf import csrf_protect, csrf_exempt

#Alerts
from django.contrib import messages

#Auth login
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Resigter user and auth
@csrf_exempt
def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:

        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+ user)

                return redirect('login')

        context = {'form':form}
        return render(request,'accounts/register.html',context)

@csrf_exempt
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                    login(request, user)
                    return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        
        context = {}
        return render(request,'accounts/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')




@login_required(login_url='login')
# Dashboard
def home(request):
    url = "https://covid-19-data.p.rapidapi.com/country"

    querystring = {"name":"colombia"}

    headers = {
        'x-rapidapi-key': "57c9e31d2fmsh39d71cc61951b32p1eac1cjsn46bac7a652ad",
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    data = response[0]

    context = {
               'country':data['country'],
               'code':data['code'],
               'confirmed':data['confirmed'],
               'recovered':data['recovered'],
               'critical': data['critical'],
               'deaths':data['deaths'],
               'latitude':data['latitude'],
               'longitude':data['longitude'],
               'lastChange':data['lastChange'],
               'lastUpdate':data['lastUpdate'],
              }

    for d in context:
        print(d,' = ',context[d])

    return render(request,'accounts/index.html',context)




