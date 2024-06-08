import json
import time
import pandas as pd
import requests
from requests import request
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar
from .models import Client_Analyzer,Client
from django.http import  HttpResponse



def startautomation(i,user,list_of_id,dataframe):
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
    print(dataframe['First_Message_Date'][i])
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


def Job(user):
# Query data from the database
    queryset = Client.objects.all()

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
        startautomation(i,user,list_of_id,pd.DataFrame(data_dict))
