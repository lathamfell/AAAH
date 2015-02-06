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
import getpass
from AAAHDatabase import appointmentExists, addAppointment, removeAppointment

def main():
  # set timezone
  tz = pytz.timezone('PST8PDT')
  
  # write to debug log
  with open("../AAAH/handler_log", 'a') as logfile:
    logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
    logfile.write(" : main function called")
  
  # bring message in from pipe as an array
  msg_pipe = sys.stdin.readlines()
  
  # join every array element into a single string
  msg_string = ('').join(msg_pipe)
  
  # turn string into message object
  msg = email.message_from_string(msg_string)
  
  # send icalendar invite
  user_string = getpass.getuser() + "@engr.orst.edu"

  # For some reason, if multiple emails are entered here, only the first
  #   email will receive the icalendar invite.  So just use one email here
  # message_recipiant = ["lathamfell@gmail.com"]
  # invite should be sent to the same ENGR account
  message_recipiant = [user_string]
  
  # categorize message as signup or cancellation
  if msg['subject'] == "Advising Signup Cancellation":
    signup = False
  else:
    signup = True
  
  # parse email body for data
  for line in msg.get_payload().split('\n'):
    
    # set advisor name and address
    if line.startswith('Advising Signup with '):
      advisorName = line[21:].strip()
      advisorName = advisorName[:-10]
    
    # pull student full name. Example: "Brabham, Matthew Lawrence"
    if line.startswith('Name:'):
      studentName = line[5:].strip()
    
    # pull student email address
    if line.startswith('Email:'):
      studentAddress = line[6:].strip()
    
    # set advisor email address to this user's email
    advisorAddress = user_string
    
    # pull appointment date
    if line.startswith('Date:'):
      dateWithDay = line[5:].strip()
      day = int(dateWithDay.split(',')[1].split(' ')[2][:-2].strip())
      year = int(dateWithDay.split(',')[2].strip())
      monthString = dateWithDay.split(',')[1].split(' ')[1].strip()
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
      startTime12H = time.split('-')[0].strip()
      startHour = int(startTime12H.split(':')[0].strip())
      startMinute = int(startTime12H.split(':')[1][:2].strip())
      startCycle = startTime12H[-2:]
      if startCycle == 'pm':
        startHour += 12
      
      # get end time data
      endTime12H = time.split('-')[1].strip()
      endHour = int(endTime12H.split(':')[0].strip())
      endMinute = int(endTime12H.split(':')[1][:2].strip())
      endCycle = endTime12H[-2:]
      if endCycle == 'pm':
        endHour += 12
 
  # save appointment start and end time
  startDatetime = datetime.datetime(year, month, day, 
                  startHour, startMinute, 0, 0, tz)
  endDatetime = datetime.datetime(year, month, day, 
                endHour, endMinute, 0, 0, tz)
  # create uid
  uid = startDatetime.strftime("%y%m%d%H%M")
  # check for invalid requests
  if signup and appointmentExists(uid):
    # appointment slot taken. Ignore email
    
    # write to log for debugging purposes
    with open("../AAAH/handler_log", 'a') as logfile:
      logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
      logfile.write(" : ignored email for busy appointment slot")

  elif not signup and not appointmentExists(uid):
    # cancellation for appointment that doesn't exist. Ignore email
    
    # write to log for debugging purposes
    with open("../AAAH/handler_log", 'a') as logfile:
      logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
      logfile.write(" : ignored cancel email for non-existent appmt")

  else:
    # request is valid. Process email
    
    # build icalendar object
    cal = icalendar.Calendar()
    cal.add('prodid', "-//Google Inc//Google Calendar 70.9054//EN")
    cal.add('version', "2.0")
    if signup:
      body = ""
      subject = "Advising Appointment for " + studentName
      cal.add('method', 'REQUEST')
      cal.add('status', 'confirmed')
    else:
      body = "Appointment Cancellation for " + studentName + '\n' + \
             "When: " + dateWithDay + '\n' + \
             "Where: Office of " + advisor_string
      subject = "Appointment Cancellation for " + studentName
      cal.add('method', 'CANCEL')
      cal.add('status', 'cancelled')

    # build the event
    event = icalendar.Event()
    for attendee in message_recipiant:
      event.add('attendee', attendee)
    event.add('organizer', user_string)
    event.add('category', "Event")
    event.add('summary', subject)
    event.add('description', body)
    event.add('location', "Office of " + advisorName)
    event.add('dtstart', startDatetime)
    event.add('dtend', endDatetime)
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
    msg["From"] = user_string
    msg["To"] = ", ".join(message_recipiant)
    msg["Date"] = email.utils.formatdate(localtime=True)
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
                     str(startDatetime),
                     str(endDatetime),
                     dateWithDay,
                     startTime12H,
                     endTime12H)

      # write to log for debugging purposes
      with open("../AAAH/handler_log", 'a') as logfile:
        logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
        logfile.write(" : processed signup email " + uid)
    else:
      removeAppointment(uid)

      # write to log for debugging purposes
      with open("../AAAH/handler_log", 'a') as logfile:
        logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
        logfile.write(" : processed cancel email " + uid)

if __name__ == '__main__':
  main()
