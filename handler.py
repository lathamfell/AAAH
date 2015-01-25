import MySQLdb
import smtplib
import email
import time
import email.MIMEMultipart
import email.MIMEBase
import email.MIMEText
import datetime as dt
import icalendar
import pytz
import random
import sys

def main():
  # bring message in from pipe as an array
  msg_pipe = sys.stdin.readlines()
  # join every array element into a single string
  msg_string = ('').join(msg_pipe)
  # turn string into message object
  msg = email.message_from_string(msg_string)
  # send icalendar invite  
  sendAppointment("AAAH Party", "Let's get together to celebrate")
  me = 'felll@engr.orst.edu'
  you = ['lathamfell@gmail.com']
  tz = pytz.timezone('PST8PDT')
  startHour = 7
  start = dt.datetime(2015, 1, 30, 16, 30, 0, 0, tz)
  cal = icalendar.Calendar()
  cal.add('prodid', '-//AAAH//engr.orst.edu//')
  cal.add('version', '2.0')
  cal.add('method', "REQUEST")
  event = icalendar.Event()
  for attendee in you:
    event.add('attendee', attendee)
  event.add('organizer', "felll@engr.orst.edu")
  event.add('status', "confirmed")
  event.add('category', "Event")
  event.add('summary', "AAAH Party")
  event.add('description', "Let's get together to celebrate")
  event.add('location', "Room 101")
  event.add('dtstart', start)
  event.add('dtend', dt.datetime(2015, 1, 30, 17, 30, 0, 0, tz))
  event.add('dtstamp', tz.localize(dt.datetime.now()))
  event['uid'] = 'mcgrath' + str(random.randrange(1, 999998+1))
  event.add('priority', 5)
  event.add('sequence', 1)
  event.add('created', tz.localize(dt.datetime.now()))

  cal.add_component(event)

  msg = email.MIMEMultipart.MIMEMultipart('alternative')

  msg["Subject"] = subj
  msg["From"] = "felll@engr.orst.edu"
  msg["To"] = ", ".join(you)
  msg["Content-class"] = "urn:content-classes:calendarmessage"

  msg.attach(email.MIMEText.MIMEText(description))

  filename = "invite.ics"
  part = email.MIMEBase.MIMEBase('text', "calendar", method="REQUEST", name=filename)
  part.set_payload(cal.to_ical())
  email.Encoders.encode_base64(part)
  part.add_header('Content-Description', filename)
  part.add_header('Content-class', "urn:content-classes:calendarmessage")
  part.add_header("Filename", filename)
  part.add_header("Path", filename)
  msg.attach(part)

  s = smtplib.SMTP("mail.oregonstate.edu")
  s.sendmail(msg["From"], [msg["To"]], msg.as_string())
  s.quit()

  # update database
  updateDatabase()

def updateDatabase():
  # db = MySQLdb.connect('oniddb.cws.oregonstate.edu', 
  #                      'felll-db',
  #                      'Qo8KoTmgkOUFj7bs', 
  #                      'felll-db')
  # cur = db.cursor()
  pass

if __name__ == '__main__':
  main()
