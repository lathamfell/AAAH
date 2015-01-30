import smtplib
import names
import datetime
import random

def main():
  print "Enter s to send a test signup.\n" \
        "Enter t to send 10 test signups.\n" \
        "Enter c to send a matching test cancellation.\n" \
        "Enter q to exit."
  while True:
    command = raw_input()
    if command == "s" or command == "S":
      sendSignup(1)
    elif command == "t" or command == "T":
      sendSignup(10)
    elif command == "c" or command == "C":
      sendCancellation()
    else:
      break

def sendSignup(iterations):
  for i in range(iterations):
    # set msg values
    fromAddress = "do.not.reply@engr.orst.edu"
    studentName = names.get_last_name() + ", " + \
                  names.get_first_name() + " " + \
                  names.get_first_name()
    studentAddress = "latham.fell@base2s.com"
    # in production, advisorAddress will be dmcgrath@eecs.oregonstate.edu
    advisorAddress = "felll@engr.orst.edu"
    subject = "Advising Signup with McGrath, D Kevin confirmed for " + studentName
    # pick a random year
    year = random.randrange(2015, 2017 + 1)
    # pick a random month
    month = random.randrange(1, 12 + 1)
    # pick a random day in that month
    if month == 1 or month == 3 or month == 5 or month == 7 or \
       month == 8 or month == 10 or month == 12:
      day = random.randrange(1, 31 + 1)
    if month == 2:
      day = random.randrange(1, 28 + 1)
    if month == 4 or month == 6 or month == 9 or month == 11:
      day = random.randrange(1, 30 + 1)
    # create a python date object
    date = datetime.date(year, month, day)
    # get the month and the day of the week as strings
    weekday = date.strftime('%A')
    monthString = date.strftime('%B')
    # get date suffix
    if 4 <= day <= 20 or 24 <= day <= 30:
      suffix = "th"
    else:
      suffix = ["st", "nd", "rd"][day % 10 - 1]
    # build date string
    dateString = weekday + ", " + monthString + " " + \
                 str(day) + suffix + ", " + str(year)
    # generate random start time
    timeStartHour = random.randrange(7, 19 + 1)
    timeStartOptions = [0, 20, 40]
    timeStartMinute = timeStartOptions[random.randrange(3)]
    timeStart = datetime.time(timeStartHour, timeStartMinute)
    timeStartCycle = timeStart.strftime('%p').lower()
    timeStartHourChar = str(int(timeStart.strftime('%I')))
    timeStartMinuteString = timeStart.strftime('%M')
    timeStartString = timeStartHourChar + ":" + \
                      timeStartMinuteString + \
                      timeStartCycle
    # end time is 20 minutes later
    # create datetime object, which is necessary to use timedelta
    datetimeStart = datetime.datetime(year, month, day, timeStartHour, timeStartMinute)
    datetimeEnd = datetimeStart + datetime.timedelta(minutes=20)
    timeEndHourChar = str(int(datetimeEnd.strftime('%I')))
    timeEndMinuteString = datetimeEnd.strftime('%M')
    timeEndCycle = datetimeEnd.strftime('%p').lower()
    timeEndString = timeEndHourChar + ":" + \
                    timeEndMinuteString + \
                    timeEndCycle
    body = 'Advising Signup with McGrath, D Kevin confirmed\n' \
      'Name: ' + studentName + '\n' \
      'Email: ' + studentAddress + '\n' \
      'Date: ' + dateString + '\n' \
      'Time: ' + timeStartString + ' - ' + timeEndString + '\n\n\n' \
      'Please contact support@engr.oregonstate.edu if you ' \
      'experience problems'
    # construct email
    msg = 'From: ' + fromAddress + '\n' + \
          'To: ' + studentAddress + ' ' + advisorAddress + '\n' + \
          'Subject: ' + subject + '\n\n' + \
          body
    # send the email
    s = smtplib.SMTP('mail.oregonstate.edu')
    s.sendmail(fromAddress, [studentAddress, advisorAddress], msg)

def sendCancellation(studentName, studentAddress, advisorAddress, dateWithDay, startTime12H, endTime12H):
  # set email values
  fromAddress = "do.not.reply@engr.orst.edu"
  subject = "Advising Signup Cancellation"
  body = 'Advising Signup with ' + studentName + ' CANCELLED\n' \
    'Name: ' + studentName + '\n' \
    'Email: ' + studentAddress + '\n' \
    'Date: ' + dateWithDay + '\n' \
    'Time: ' + startTime12H + ' - ' + endTime12H + '\n\n\n' \
    'Please contact support@engr.oregonstate.edu if you ' \
    'experience problems'
  # construct email
  msg = 'From: ' + fromAddress + '\n' + \
        'To: ' + studentAddress + ' ' + advisorAddress + '\n' + \
        'Subject: ' + subject + '\n\n' + \
        body
  # send the email
  s = smtplib.SMTP('mail.oregonstate.edu')
  s.sendmail(fromAddress, [studentAddress, advisorAddress], msg)

if __name__ == '__main__':
  main()
