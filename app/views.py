import csv
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta, date
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from dateutil.relativedelta import relativedelta
from .forms import MyModelForm
import pandas as pd
import os
from .jobs import Job
from .update import start
from .models import *
from .encoding import encryption


def signup(request):
    if request.method == 'POST':
        # Get form data from request
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'signup.html')

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html')

        # Create new user
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()

        # Redirect to login page
        # Assuming 'login' is the name of your login URL pattern
        return redirect('')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page, or a page of your choice
            # Change 'success' to the name of your success URL pattern
            return redirect('success')
        else:
            # Return an 'invalid login' error message
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page


def register(request):
    # Handle user registration
    return HttpResponse("Hello")


def home(request):
    return render(request, "base.html")


def inserdata(Listoffiles,filePath):
    newdf = {
        'Name': [],
        'Phone': [],
        'Amount': [],
        'Date': [],
        'PaymentPeriod': [],
        'firstMsg': [],
        'secondMsg': [],
        # 'companyName' : []
    }
    path=str(filePath)
    df = pd.read_csv(path[1:])

    newdf['Name'].append(df['Name'].values.tolist())
    newdf['Phone'].append(df['Phone Number'].values.tolist())
    newdf['Amount'].append(df['Amount'].values.tolist())
    newdf['PaymentPeriod'].append(df['Payment Period'].values.tolist())

    date_col = pd.DatetimeIndex(df["Dates"])
    df['Year'] = date_col.year
    df['month'] = date_col.month
    year = df['Year'].values.tolist()
    month = df['month'].values.tolist()
    datesfromexcel = df['Dates'].values.tolist()
    PaymentPeriod = df['Payment Period'].values.tolist()

    initialYear = min(year)
    finalYear = 2024

    yearDiff = (finalYear-initialYear)
    yearslist = []
    for j in range(yearDiff+1):
        yearslist.append(initialYear+j)
    new_date_new = []
    Dates = []
    firstMsg = []
    SecondMsg = []
    currentDate = datetime .today()
        # print(len(df))
    for k in range(len(df)):
           for m in range(len(yearslist)):
                if yearslist[m] == year[k]:
                    multiple = (len(yearslist)-m-1)
                    if '/' in datesfromexcel[k]:
                        modifydate = datesfromexcel[k].replace('/', '-')
                        date_object = datetime.strptime(modifydate, '%d-%m-%Y')
                        new_date_new.append(
                            date_object + relativedelta(months=12*multiple))
                        print(k)
                        print(new_date_new)
                        Dates.append(new_date_new[k].strftime("%Y-%m-%d"))

                        Msg1obj = new_date_new[k]-timedelta(days=10)
                        Msg2obj = new_date_new[k]-timedelta(days=5)

                        firstMsg.append(Msg1obj.strftime("%Y-%m-%d"))
                        SecondMsg.append(Msg2obj.strftime("%Y-%m-%d"))

                        if Msg1obj < currentDate.replace(hour=0, minute=0, second=0, microsecond=0) and Msg2obj < currentDate.replace(hour=0, minute=0, second=0, microsecond=0):
                            if PaymentPeriod[k] == 'Monthly':
                                new_date_new[k] = (
                                    new_date_new[k]+relativedelta(months=1))
                                Dates[k] = (
                                    new_date_new[k].strftime("%Y-%m-%d"))
                                Msg1obj = new_date_new[k]-timedelta(days=10)
                                Msg2obj = new_date_new[k]-timedelta(days=5)

                                firstMsg[k] = (Msg1obj.strftime("%Y-%m-%d"))
                                SecondMsg[k] = (Msg2obj.strftime("%Y-%m-%d"))

                            elif PaymentPeriod[k] == 'Quaterly':
                                new_date_new[k] = (
                                    new_date_new[k]+relativedelta(months=3))
                                Dates[k] = (
                                    new_date_new[k].strftime("%Y-%m-%d"))
                                Msg1obj = new_date_new[k]-timedelta(days=10)
                                Msg2obj = new_date_new[k]-timedelta(days=5)

                                firstMsg[k] = (Msg1obj.strftime("%Y-%m-%d"))
                                SecondMsg[k] = (Msg2obj.strftime("%Y-%m-%d"))

                            elif PaymentPeriod[k] == 'Half Yearly':

                                new_date_new[k] = (
                                    new_date_new[k]+relativedelta(months=6))
                                Dates[k] = (
                                    new_date_new[k].strftime("%Y-%m-%d"))

                                Msg1obj = new_date_new[k]-timedelta(days=10)
                                Msg2obj = new_date_new[k]-timedelta(days=5)

                                firstMsg[k] = (Msg1obj.strftime("%Y-%m-%d"))
                                SecondMsg[k] = (Msg2obj.strftime("%Y-%m-%d"))

                            elif PaymentPeriod[k] == 'Yearly':
                                new_date_new[k] = (
                                    new_date_new[k]+relativedelta(months=12))
                                Dates[k] = (
                                    new_date_new[k].strftime("%Y-%m-%d"))

                                Msg1obj = new_date_new[k]-timedelta(days=10)
                                Msg2obj = new_date_new[k]-timedelta(days=5)

                                firstMsg[k] = (Msg1obj.strftime("%Y-%m-%d"))
                                SecondMsg[k] = (Msg2obj.strftime("%Y-%m-%d"))
                            else:
                                pass
                        else:
                            pass

                    break

                else:
                    pass
    newdf['firstMsg'].append(firstMsg)
    newdf['secondMsg'].append(SecondMsg)
    newdf['Date'].append(Dates)
    # enc_df=encryption(pd.DataFrame(newdf))
    print(newdf)
    return pd.DataFrame(newdf)


def index(request):
    # datainsertion
    if request.method == "POST":
        file = request.FILES.getlist("file")
        for i in file:
            File(file=i, user=request.user).save()
        Listoffiles = File.objects.filter(user=request.user)
        # If you expect only one file per user, you can get it like this:
        if Listoffiles.exists():
            for i in range(len(Listoffiles)):
                file_path = Listoffiles[i].file.url
                Dataframe = inserdata(Listoffiles,file_path)
                path=str(file_path)
                print(path)
                readcsv = pd.read_csv(path[1:])
                for j in range(len(readcsv)):
                    Client(Name=Dataframe['Name'][0][j], Phone_Number=Dataframe['Phone'][0][j], Amount=Dataframe['Amount'][0][j], Dates=Dataframe['Date'][0][j],
                           Payment_Period=Dataframe['PaymentPeriod'][0][j], First_Message_Date=Dataframe['firstMsg'][0][j], Second_Message_Date=Dataframe['secondMsg'][0][j], user=request.user).save()
                os.remove(path[1:])
                File.objects.get(pk=Listoffiles[i].pk).delete()
        else:
            pass
    #

    return render(request, 'index.html')


def analyzer(request):
    print(request.user)
    try:
        data = Client_Analyzer.objects.filter(user=request.user).values()
        return render(request, "analyzer.html", {'data': data})

    except:
        data = None
        return render(request, "analyzer.html", {'data': data})


def visualization(request):
    print(request.user)
    try:
        data = Client.objects.filter(user=request.user).values()
        print(data[0].get("Name"))
        return render(request, "visualization.html", {'data': data})

    except:
        data = None
        return render(request, "visualization.html", {'data': data})


def search_vis(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        data = Client.objects.filter(Name__icontains=query)
    else:
        data = Client.objects.none()
    return render(request, 'visualization.html', {'data': data})


def messageautomation(request):

    if True not in [obj.Attempt for obj in Attempts.objects.filter(user=request.user)]:
        Attempts(Attempt=True, user=request.user).save()
        start(request.user)
    else:
        return HttpResponse("Can't!")

    return HttpResponse("Done!")
