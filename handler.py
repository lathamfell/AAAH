import smtplib
import email
import time
import email.MIMEMultipart
import email.MIMEBase
import email.MIMEText
import datetime
import icalendar
import pytz
import random
import sys
from AAAHDatabase import appointmentExists, addAppointment, removeAppointment

def main():
  # set timezone
  tz = pytz.timezone('PST8PDT')
  # write to debug log
  with open("handler_log", 'a') as logfile:
    logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
    logfile.write(" : main function called")
  # bring message in from pipe as an array
  msg_pipe = sys.stdin.readlines()
  # join every array element into a single string
  msg_string = ('').join(msg_pipe)
  # turn string into message object
  msg = email.message_from_string(msg_string)
  # send icalendar invite
  # in production, 'me' will be dmcgrath@eecs.oregonstate.edu
  me = "felll@engr.orst.edu"
  # in production, 'you' will be dmcgrath@eecs.oregonstate.edu
  you = ["lathamfell@gmail.com", "latham.fell@base2s.com"]
  # categorize message as signup or cancellation
  if msg['subject'] == "Advising Signup Cancellation":
    signup = False
  else:
    signup = True
  # parse email body for data
  for line in msg.get_payload().split('\n'):
    # pull student full name. Example: "Brabham, Matthew Lawrence"
    if line.startswith('Name:'):
      studentName = line[5:].strip()
    # pull student email address
    if line.startswith('Email:'):
      studentAddress = line[6:].strip()
    # set advisor name and address
    advisorName = "McGrath, D Kevin"
    advisorAddress = "dmcgrath@eecs.oregonstate.edu"
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
  start = datetime.datetime(year, month, day, startHour, startMinute, 0, 0, tz)
  end = datetime.datetime(year, month, day, endHour, endMinute, 0, 0, tz)
  # create uid
  uid = "dmcgrath" + start.strftime("%Y%m%dT%H%M%S")
  # check for invalid requests
  if signup and appointmentExists(uid):
    # appointment slot taken. Ignore email
    # write to log for debugging purposes
    with open("handler_log", 'a') as logfile:
      logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
      logfile.write(" : ignored email for busy appointment slot")
  elif not signup and not appointmentExists(uid):
    # cancellation for appointment that doesn't exist. Ignore email
    # write to log for debugging purposes
    with open("handler_log", 'a') as logfile:
      logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
      logfile.write(" : ignored cancel email for non-existent appmt")
  else:
    # request is valid. Process email
    # build icalendar object
    cal = icalendar.Calendar()
    cal.add('prodid', "-//AAAH//engr.orst.edu//")
    cal.add('version', "2.0")
    if signup:
      body = ""
      subject = "Advising Appointment for " + studentName
      cal.add('method', 'REQUEST')
      cal.add('status', 'confirmed')
    else:
      body = "Appointment Cancellation for " + studentName + '\n' + \
             "When: " + date + " " + time + '\n' + \
             "Where: Office of Kevin McGrath"
      subject = "Appointment Cancellation for " + studentName
      cal.add('method', 'CANCEL')
      cal.add('status', 'cancelled')
    # build the event
    event = icalendar.Event()
    for attendee in you:
      event.add('attendee', attendee)
    event.add('organizer', me)
    event.add('category', "Event")
    event.add('summary', subject)
    event.add('description', body)
    event.add('location', "Office of Kevin McGrath")
    event.add('dtstart', start)
    event.add('dtend', end)
    event.add('dtstamp', tz.localize(datetime.datetime.now()))
    event['uid'] = uid
    event.add('priority', 5)
    event.add('sequence', 1)
    event.add('created', tz.localize(datetime.datetime.now()))
    # add the event to the icalendar object
    cal.add_component(event)
    # build the outgoing email
    msg = email.MIMEMultipart.MIMEMultipart('alternative')
    msg["Subject"] = subject
    msg["From"] = me
    msg["To"] = ", ".join(you)
    msg["Content-class"] = "urn:content-classes:calendarmessage"
    msg.attach(email.MIMEText.MIMEText(body))
    # build the icalendar invite attachment
    filename = "invite.ics"
    if signup:
      part = email.MIMEBase.MIMEBase('text', 'calendar', 
                                     method='REQUEST', name=filename)
    else:
      part = email.MIMEBase.MIMEBase('text', 'calendar',
                                     method='CANCEL', name=filename)
    part.set_payload(cal.to_ical())
    email.Encoders.encode_base64(part)
    part.add_header('Content-Description', filename)
    part.add_header('Content-class', "urn:content-classes:calendarmessage")
    part.add_header("Filename", filename)
    part.add_header("Path", filename)
    # attach the invite to the outgoing email
    msg.attach(part)
    # send the email
    s = smtplib.SMTP("mail.oregonstate.edu")
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.quit()
    # update the database
    if signup:
      addAppointment(uid, 
                     studentName, 
                     studentAddress,
                     advisorName,
                     advisorAddress,
                     start,
                     end)
      # write to log for debugging purposes
      with open("handler_log", 'a') as logfile:
        logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
        logfile.write(" : processed signup email " + uid)
    else:
      removeAppointment(uid)
      # write to log for debugging purposes
      with open("handler_log", 'a') as logfile:
        logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
        logfile.write(" : processed cancel email " + uid)

if __name__ == '__main__':
  main()
