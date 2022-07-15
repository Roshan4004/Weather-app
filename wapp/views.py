from django.shortcuts import redirect, render
import requests
import pytz
from datetime import datetime,timezone
from django.contrib import messages
# Create your views here.

def index(request):
    try:
        if request.method == 'POST':
            city=request.POST['city']
        else:
            city='Nepal'
        apikey='f5c6ba060f3362674b261b48d58b492e'
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
        context={'feels':feels,'pressure':pressure,'humidity':humidity,'description':description,'icon':icon,'temp':temp,'day':day,'sunr':sunr,'suns':suns,'country':country}
        return render(request,'index.html',context)
    except KeyError:
        messages.info(request,"Please enter a valid city name!!")
        return redirect("/")
