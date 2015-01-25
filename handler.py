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
  # in production, 'me' will be dmcgrath@eecs.oregonstate.edu
  me = 'felll@engr.orst.edu'
  # in production, 'you' will be dmcgrath@eecs.oregonstate.edu
  you = ['lathamfell@gmail.com']
  tz = pytz.timezone('PST8PDT')
  #target = open('test' + str(random.randrange(1, 998+1)), 'w+')
  # pull date from email
  for line in msg.get_payload().split('\n'):
    # pull appointment date
    if line.startswith('Date:'):
      date = line[5:].strip()
      day = int(date.split(',')[1].split(' ')[2][:-2].strip())
      year = int(date.split(',')[2].strip())
      monthString = date.split(',')[1].split(' ')[1].strip()
      if monthString == 'January':
        month = 1
      elif monthString == 'February':
        month = 2
      elif monthString == 'March':
        month = 3
      elif monthString == 'April':
        month = 4
      elif monthString == 'May':
        month = 5
      elif monthString == 'June':
        month = 6
      elif monthString == 'July':
        month = 7
      elif monthString == 'August':
        month = 8
      elif monthString == 'September':
        month = 9
      elif monthString == 'October':
        month = 10
      elif monthString == 'November':
        month = 11
      elif monthString == 'December':
        month = 12
      else:
        pass
    # pull appointment start and end time
    if line.startswith('Time:'):
      time = line[5:].strip()
      # get start time data
      start = time.split('-')[0].strip()
      startHour = int(start.split(':')[0].strip())
      startMinute = int(start.split(':')[1][:2].strip())
      startCycle = start.split()[1]
      if startCycle == 'pm':
        startHour += 12
      # get end time data
      end = time.split('-')[1].strip()
      endHour = int(end.split(':')[0].strip())
      endMinute = int(end.split(':')[1][:2].strip())
      endCycle = end.split()[1]
      if endCycle == 'pm':
        endHour += 12
  # save appointment start and end time
  start = dt.datetime(year, month, day, startHour, startMinute, 0, 0, tz)
  end = dt.datetime(year, month, day, endHour, endMinute, 0, 0, tz)
  # build icalendar object
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
  event.add('dtend', end)
  event.add('dtstamp', tz.localize(dt.datetime.now()))
  event['uid'] = 'mcgrath' + str(random.randrange(1, 999998+1))
  event.add('priority', 5)
  event.add('sequence', 1)
  event.add('created', tz.localize(dt.datetime.now()))

  cal.add_component(event)

  msg = email.MIMEMultipart.MIMEMultipart('alternative')

  msg["Subject"] = "AAAH Party"
  msg["From"] = "felll@engr.orst.edu"
  msg["To"] = ", ".join(you)
  msg["Content-class"] = "urn:content-classes:calendarmessage"

  msg.attach(email.MIMEText.MIMEText("Let's get together to celebrate"))

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
