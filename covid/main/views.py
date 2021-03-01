#https://whaleandjaguar.co/

from django.shortcuts import render, redirect
from datetime import datetime,timedelta


# Create your view here
from .forms import CreateUserForm, DateForm, CodeForm, DateCodeForm
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



# Dashboard
@login_required(login_url='login')

# Main results
def home(request):
    now = datetime.now()
    url = "https://covid-19-data.p.rapidapi.com/totals"

    headers = {
        'x-rapidapi-key': "57c9e31d2fmsh39d71cc61951b32p1eac1cjsn46bac7a652ad",
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers).json()
    data = response[0]
    #current time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    
    #parse format date
    date1 = data['lastChange']
    date2 = data['lastUpdate']
    
    time_zone1 = int(date1[-6:][:3])
    item_date = datetime.strptime(date1.replace(".000", "")[:-6], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=-time_zone1)

    time_zone2 = int(date2[-6:][:3])
    item_dateUpdt = datetime.strptime(date2.replace(".000", "")[:-6], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=-time_zone2)

    context = {
               'date_time':date_time,
               'confirmed':data['confirmed'],
               'recovered':data['recovered'],
               'critical': data['critical'],
               'deaths':data['deaths'],
               'lastChange':item_date,
               'lastUpdate':item_dateUpdt,
    }

    return render(request,'accounts/index.html',context)


#Search by date
@csrf_exempt
def dateForm(request):

    if request.method =='POST':
     
        form = DateForm(data=request.POST)
        if form.is_valid():
           
            data_date = str(form.cleaned_data.get('date_input'))
            url = "https://covid-19-data.p.rapidapi.com/report/totals"
           
            querystring = {"date":data_date}
          
            headers = {
                'x-rapidapi-key': "57c9e31d2fmsh39d71cc61951b32p1eac1cjsn46bac7a652ad",
                'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
                }

            response = requests.request("GET", url, headers=headers, params=querystring).json()

            if len(response)>0:
                data=response[0]
            
                context = {
                'confirmed':data['confirmed'],
                'recovered':data['recovered'],
                'critical': data['critical'],
                'deaths':data['deaths'],
                'active':data['active'],
                'date':data['date'],
                }
                for d in context:
                    print(d,' = ',context[d])
                return render(request,'accounts/date.html',context)
    else:
        form = DateForm()
    return render(request,'accounts/date.html',{'form':form})
 

#Search by cod's country 

def countryCovid(request):
    
    if request.method =='POST':
        form = CodeForm(data=request.POST)
        if form.is_valid():
            data_code = form.cleaned_data.get('code')
        
            url = "https://covid-19-data.p.rapidapi.com/country/code"

            querystring = {"code":data_code}

            headers = {
                'x-rapidapi-key': "57c9e31d2fmsh39d71cc61951b32p1eac1cjsn46bac7a652ad",
                'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
                }

            response = requests.request("GET", url, headers=headers, params=querystring).json()

            

            if len(response)>0:

                data = response[0]

                #parse format date
            
                date1 = data['lastChange']
                date2 = data['lastUpdate']
                
                time_zone1 = int(date1[-6:][:3])
                item_date = datetime.strptime(date1.replace(".000", "")[:-6], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=-time_zone1)

                time_zone2 = int(date2[-6:][:3])
                item_dateUpdt = datetime.strptime(date2.replace(".000", "")[:-6], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=-time_zone2)
                    
                context = {
                        'country':data['country'],
                        'code':data['code'],
                        'confirmed':data['confirmed'],
                        'recovered':data['recovered'],
                        'critical': data['critical'],
                        'deaths':data['deaths'],
                        'latitude':data['latitude'],
                        'longitude':data['longitude'],
                        'lastChange':item_date,
                        'lastUpdate':item_dateUpdt,
                        }

                for d in context:
                    print(d,' = ',context[d])

                return render(request,'accounts/country.html',context)
    else:
        form = CodeForm()
    return render(request,'accounts/country.html',{'form':form})


#Search by date & code   DateCodeForm

def countryDate(request):
    
    if request.method=='POST':
        form = DateCodeForm(data=request.POST)
      
        if form.is_valid():

            data_date = str(form.cleaned_data.get('dateIn'))
            data_code = form.cleaned_data.get('codeIn')
          
            url = "https://covid-19-data.p.rapidapi.com/report/country/code"

            querystring = {"date":data_date,"code":data_code}

            headers = {
                'x-rapidapi-key': "57c9e31d2fmsh39d71cc61951b32p1eac1cjsn46bac7a652ad",
                'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
                }

            response = requests.request("GET", url, headers=headers, params=querystring).json()

            if len(response)>0:
                data = response[0]
              
                if 'confirmed' in data['provinces'][0]:
                    province_value = data['provinces'][0]['province']
                    confirmed_value = data['provinces'][0]['confirmed']
                    recovered_value = data['provinces'][0]['recovered']
                    deaths_value = data['provinces'][0]['deaths']
                    active_value = data['provinces'][0]['active']

                    context = {
                        'country':data['country'],
                        'province':province_value,
                        'confirmed':confirmed_value,
                        'recovered':recovered_value,
                        'deaths':deaths_value,
                        'active':active_value,
                        'latitude':data['latitude'],
                        'longitude':data['longitude'],
                        'date':data['date']
                    }
                    for d in context:
                        print(d,' = ',context[d])
                    return render(request,'accounts/country_date.html',context)
                else:
                    province_value = data['provinces'][0]['province']
                    context = {
                        'country':data['country'],
                        'province':province_value,
                        'latitude':data['latitude'],
                        'longitude':data['longitude'],
                        'date':data['date']
                    }
                    for d in context:
                        print(d,' = ',context[d])
                    return render(request,'accounts/country_date.html',context)
                               
    else:
        form = DateForm()
    return render(request,'accounts/country_date.html',{'form':form})

