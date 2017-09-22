import sched
import time
import threading
import datetime

from twilio.rest import Client

from app.constants.twilio import ACCOUNT_SID, AUTH_TOKEN 
from app.models.event import Event


client = Client(ACCOUNT_SID, AUTH_TOKEN)
scheduler = sched.scheduler(time.time, time.sleep)


def schedule_event_alert(event):
    seconds_until_alert = seconds_between_now_and(event)
    if seconds_until_alert > 0:
        scheduler.enter(seconds_until_alert, 1, notify_attendees, (event))


def add_dummy_event():
    print 'add dummy'
    scheduler.enter(1000, 1, add_dummy_event, ())


def start_scheduler():
    # keep scheduler alive
    add_dummy_event()

    t = threading.Thread(target=scheduler.run)
    t.daemon = True
    t.start()


# Helper functions


def notify_attendees(event):
    if seconds_between_now_and(event) > 300:
        return 

    for attendee in event.users: 
        # if they are attending and have a phone number
        # if attendee.status == 0 and attendee.user.phone:
        # msg = 'Reminder: Event {} coming up.'.format(event.name)
        # send_sms(attendee.user.phone, msg)
        pass
    pass
    

def send_sms(phone_number, message):
    message = client.messages.create(
	to=phone_number, 
	from_="+16156976052",
	body=message)


def seconds_between_now_and(event):
    alert_time = datetime.datetime.fromtimestamp(event.start_date)
    now = datetime.datetime.now()
    return (alert_time - now).total_seconds()
