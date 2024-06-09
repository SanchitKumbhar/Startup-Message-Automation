import csv
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from datetime import datetime, timedelta, date
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from dateutil.relativedelta import relativedelta
from .forms import MyModelForm
from schedule import every,repeat
import schedule
import pandas as pd
import os
import time
from .models import *
from .encoding import encryption
import json
import requests
from requests import request
from .models import Client_Analyzer,Client
from django.http import  HttpResponse
from threading import Thread
import sched


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


def inserdata(Listoffiles, filePath):
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
    path = str(filePath)
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
                Dataframe = inserdata(Listoffiles, file_path)
                path = str(file_path)
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
    
    user=request.user
    def startautomation(i,list_of_id,dataframe):
        
        def Update(i,j):
            currentDate = datetime.today()
            if j == 'Monthly':
                dateobj = datetime.strptime(i, "%Y-%m-%d")
                new_date_new = dateobj+relativedelta(months=1)
                Dates = (new_date_new.strftime("%Y-%m-%d"))
                Msg1obj = new_date_new-timedelta(days=10)
                Msg2obj = new_date_new-timedelta(days=5)

                FirstMsg = (Msg1obj.strftime("%Y-%m-%d"))
                SecondMsg = (Msg2obj.strftime("%Y-%m-%d"))
                return FirstMsg,SecondMsg,Dates
            elif j == 'Quaterly':
                dateobj = datetime.strptime(i, "%Y-%m-%d")
                new_date_new = dateobj+relativedelta(months=3)
                Dates = (new_date_new.strftime("%Y-%m-%d"))
                Msg1obj = new_date_new-timedelta(days=10)
                Msg2obj = new_date_new-timedelta(days=5)

                FirstMsg = (Msg1obj.strftime("%Y-%m-%d"))
                SecondMsg = (Msg2obj.strftime("%Y-%m-%d"))
                return FirstMsg,SecondMsg,Dates

            elif j == 'Half Yearly':
                dateobj = datetime.strptime(i, "%Y-%m-%d")
                new_date_new = dateobj+relativedelta(months=6)
                Dates = (new_date_new.strftime("%Y-%m-%d"))
                Msg1obj = new_date_new-timedelta(days=10)
                Msg2obj = new_date_new-timedelta(days=5)

                FirstMsg = (Msg1obj.strftime("%Y-%m-%d"))
                SecondMsg = (Msg2obj.strftime("%Y-%m-%d"))
                return FirstMsg,SecondMsg,Dates

            elif j == 'Yearly':
                dateobj = datetime.strptime(i, "%Y-%m-%d")
                new_date_new = dateobj+relativedelta(months=12)
                Dates = (new_date_new.strftime("%Y-%m-%d"))
                Msg1obj = new_date_new-timedelta(days=10)
                Msg2obj = new_date_new-timedelta(days=5)

                FirstMsg = (Msg1obj.strftime("%Y-%m-%d"))
                SecondMsg = (Msg2obj.strftime("%Y-%m-%d"))
                return FirstMsg,SecondMsg,Dates

            else:
                pass

        def SMS_COUNTRY_API(Phone_Number,Date,Name,Amount):
            import requests

            url = "https://www.fast2sms.com/dev/bulkV2"
            name = "sanchit"
            phone = 8010235068
            msg={"This is a test message"}
            payload = f"message={msg}&language=english&route=q&numbers={Phone_Number}"
            headers = {
                'authorization': "h0FwasPTgkfSvupCxQo4rtXbe6qKlW58JVEUNMYmBRy2Oz7DH190LVnWHX5k41JbqNhBmMyRwPlOa3c2",
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            print(response.text)
        #     url = "https://restapi.smscountry.com/v0.1/Accounts/P2B2w8jc3RO6jDdzzk2W/SMSes/"

        #     payload = json.dumps({
        #     "Text": "Dear Sanchit Kumbhar we have sent the reply to Your user complaint from our Customer Services.The token number is 54876 Username is SanchitKumbhar - SMSCOU",
        #     "Number": "918010235068",
        #     "SenderId": "SMSCOU",
        #     "DRNotifyUrl": "https://www.domainname.com/notifyurl",
        #     "DRNotifyHttpMethod": "POST",
        #     "Tool": "API"
        #     })
        #     headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': 'Basic UDJCMnc4amMzUk82akRkenprMlc6aVllU0hlaXZxVUVjaElsWjNqc1hKeHBrWldKS2lZSXVOeHZNbDVETw=='
        #     }

        #     response = requests.request("POST", url, headers=headers, data=payload)


        firstMsg = datetime.strptime(dataframe['First_Message_Date'][i], '%Y-%m-%d').date()
        secondMsg = datetime.strptime(dataframe['Second_Message_Date'][i], 
        '%Y-%m-%d').date()
        payment_period=dataframe['Payment_Period'][i]
        # print(dataframe['First_Message_Date'][i])
        # print(i)

        if firstMsg == date.today():
                # SMS_COUNTRY_API()
                print("!Done!")
                Date= dataframe['Dates'][i]
                Update_first_msg,Update_second_msg,Update_Date=Update(Date,payment_period)
                Name=dataframe['Name'][i]
                Phone_Number=dataframe['Phone_Number'][i]
                Amount=dataframe['Amount'][i]
                obj_to_update = Client.objects.get(pk=list_of_id[i])
                obj_to_update.Name=Name
                obj_to_update.Phone_Number=Phone_Number
                obj_to_update.Amount=Amount
                obj_to_update.Dates=Update_Date
                obj_to_update.First_Message_Date=Update_first_msg
                obj_to_update.Second_Message_Date=Update_second_msg
                obj_to_update.Payment_Period=payment_period
                obj_to_update.user=user
                obj_to_update.save()
                SMS_COUNTRY_API(Phone_Number,Date,Name,Amount)

                Client_Analyzer(Name=Name,Phone_Number=Phone_Number,Amount=Amount,Dates=Update_Date,First_Message_Date=Update_first_msg,Second_Message_Date=Update_second_msg,Payment_Period=payment_period,user=user).save()
        elif secondMsg == date.today():
                Date= dataframe['Dates'][i]
                Update_first_msg,Update_second_msg,Update_Date=Update(Date,payment_period)
                Name=dataframe['Name'][i]
                Phone_Number=dataframe['Phone_Number'][i]
                Amount=dataframe['Amount'][i]
                obj_to_update = Client.objects.get(pk=list_of_id[i])
                obj_to_update.Name=Name
                obj_to_update.Phone_Number=Phone_Number
                obj_to_update.Amount=Amount
                obj_to_update.Dates=Update_Date
                obj_to_update.First_Message_Date=Update_first_msg
                obj_to_update.Second_Message_Date=Update_second_msg
                obj_to_update.Payment_Period=payment_period
                obj_to_update.user=user
                obj_to_update.save()
                Client_Analyzer(Name=Name,Phone_Number=Phone_Number,Amount=Amount,Dates=Update_Date,First_Message_Date=Update_first_msg,Second_Message_Date=Update_second_msg,Payment_Period=payment_period,user=user).save()
                print("Saved!")
        else:
                print("nope!")

    def Job():
    # Query data from the database
        queryset = Client.objects.all()
        user=request.user
        # Initialize an empty dictionary to store data
        data_dict = {}

        # Iterate over the queryset
        for obj in queryset:
            # Iterate over each field in the model
            for field in obj._meta.fields:
                field_name = field.name
                if field_name not in data_dict:
                    # If the field name is not in the dictionary, initialize an empty list for it
                    data_dict[field_name] = []
                # Append the value of the field to the list corresponding to its name in the dictionary
                data_dict[field_name].append(getattr(obj, field_name))

        # Now data_dict contains the data from the database organized into a dictionary of lists


        for i in range(Client.objects.count()):

        # # print(MessageAttemptStatus.objects.filter(user=request.user).values())
            for j in range(Client.objects.count()):
                # Query all objects
                objID = Client.objects.all()
                # Extract IDs
                list_of_id = [obj.id for obj in objID]
            # print(Client.objects.all().values('First_Message_Date')[i].get('First_Message_Date'))
            startautomation(i,list_of_id,pd.DataFrame(data_dict))



    if True not in [obj.Attempt for obj in Attempts.objects.filter(user=request.user)]:


        scheduler = sched.scheduler(time.time, time.sleep)

        def scheduled_job():
            Job()
            scheduler.enter(6, 1, scheduled_job)


        # Schedule the job to run every 6 seconds
        scheduler.enter(6, 1, scheduled_job)

# Start the scheduler in a separate thread


        def run_scheduler():
            scheduler.run()


        scheduler_thread = Thread(target=run_scheduler)
        scheduler_thread.start()


        # def scheduler_status():
        #     return HttpResponse("Scheduler is running.")
        # scheduler_status()

    else:
        return HttpResponse("cant!")
    return HttpResponse("Scheduler is running.")

