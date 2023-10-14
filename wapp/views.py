from django.shortcuts import redirect, render
import requests
import pytz
from datetime import datetime,timezone
from django.contrib import messages
import environ

env=environ.Env()
environ.Env.read_env()

def ipInfo(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    data = load(res)
    return data["city"]

def index(request):
    if request.method == "POST":
        city=request.POST['city']
        context=maindata(city)
        return render(request,'index.html',context)
    else:
        city=ipInfo()
        if city:
            context=maindata(city)
            return render(request,'index.html',context)
        else:
            context={'msg':'error'}
            return render(request,'index.html',context)
        
def maindata(city):
    apikey=env('API_KEY')
    URL='http://api.openweathermap.org/data/2.5/weather'
    PARAMS={'q':city,'appid':apikey,'units':'metric'}
    r=requests.get(url=URL,params=PARAMS)
    res=r.json()
    description=res['weather'][0]['description']
    icon=res['weather'][0]['icon']
    temp=res['main']['temp']
    country=res['sys']['country']
    feels=res['main']['feels_like']
    pressure=res['main']['pressure']
    humidity=res['main']['humidity']
    sunr=datetime.fromtimestamp(res['sys']['sunrise'],tz=pytz.utc)
    suns=datetime.fromtimestamp(res['sys']['sunset'],tz=pytz.utc)
    day=datetime.now(timezone.utc)
    context={ 'msg':'success','feels':feels,'pressure':pressure,'humidity':humidity,'description':description,'icon':icon,'temp':temp,'day':day,'sunr':sunr,'suns':suns,'country':country}
    return context