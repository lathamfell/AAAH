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

def main():
  # trival script to tell when main function is called
  target = open('pyfile', 'w+')
  target.write("my py info")
  target.close()
  sendAppointment("AAAH Party", "Let's get together to celebrate")
  updateDatabase()
  
def sendAppointment(subj, description):
  me = 'felll@engr.orst.edu'
  you = ['latham.fell@base2s.com']
  tz = pytz.timezone("Europe/London")
  startHour = 7
  start = dt.datetime(2015, 1, 17, 16, 30, 0, 0, tz)
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
  event.add('summary', subj)
  event.add('description', description)
  event.add('location', "Room 101")
  event.add('dtstart', start)
  event.add('dtend', dt.datetime(2015, 1, 17, 17, 30, 0, 0, tz))
  event.add('dtstamp', tz.localize(dt.datetime.now()))
  event['uid'] = 'mcgrath' + str(randomNumber())
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

def updateDatabase():
  # db = MySQLdb.connect('oniddb.cws.oregonstate.edu', 
  #                      'felll-db',
  #                      'Qo8KoTmgkOUFj7bs', 
  #                      'felll-db')
  # cur = db.cursor()
  pass

def randomNumber():
  return random.randrange(1, 1000000+1)

if __name__ == '__main__':
  main()
