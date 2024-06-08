from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Client(models.Model):
    Name = models.TextField(max_length=150,default="none")
    Phone_Number = models.TextField(max_length=150,default="none")
    Payment_Period = models.TextField(max_length=150,default="none")
    Dates = models.TextField(max_length=150,default="none")
    First_Message_Date = models.TextField(max_length=150,default="none")
    Second_Message_Date = models.TextField(max_length=150,default="none")
    Amount = models.TextField(max_length=150,default="none")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"{self.Name} - {self.Amount} - {self.Dates} - {self.Payment_Period} -{self.First_Message_Date} - {self.Second_Message_Date}"
class File(models.Model):
    file = models.FileField(upload_to='files')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
#     def save(self, *args, **kwargs):
#         if not self.user_id:
#             # Set the default user here
#             default_user = User.objects.get(username='root')
#             self.user = default_user
#         super().save(*args, **kwargs)



class Client_Analyzer(models.Model):
    Name = models.TextField(max_length=150,default="none")
    Phone_Number = models.TextField(max_length=150,default="none")
    Payment_Period = models.TextField(max_length=150,default="none")
    Dates = models.TextField(max_length=150,default="none")
    First_Message_Date = models.TextField(max_length=150,default="none")
    Second_Message_Date = models.TextField(max_length=150,default="none")
    Amount = models.TextField(max_length=150,default="none")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"{self.Name} - {self.Amount} - {self.Dates} - {self.Payment_Period} -{self.First_Message_Date} - {self.Second_Message_Date}"

# class MessageAttemptStatus(models.Model):
#     Attempt=models.BooleanField(default=False)
#     user = models.ForeignKey(Client, on_delete=models.CASCADE,default=1)

class Attempts(models.Model):
    Attempt=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)



# root_user = User.objects.get(username='root')

# # Creating an instance of YourModel and assigning the user
# your_model_instance = MessageAttemptStatus.objects.create(user=root_user)