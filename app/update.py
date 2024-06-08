from datetime  import datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import Job
# from .models import MessageAttemptStatus

def start(user):    
        
        Scheduler=BackgroundScheduler()
        Scheduler.add_job(Job,'interval',seconds=5,args=[user],end_date=datetime.now() + timedelta(days=365*100))
        Scheduler.start()
