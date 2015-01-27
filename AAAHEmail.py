import smtplib

def main():
  print "Enter s to send signup.\n" \
        "Enter c to send cancellation.\n" \
        "Enter q to exit."
  while True:
    command = raw_input()
    if command == "s" or command == "S":
      sendSignup()
    elif command == "c" or command == "C":
      sendCancellation()
    else:
      break

def sendSignup():
  # set msg values
  fromAddress = "do.not.reply@engr.orst.edu"
  studentName = "Brabham, Matthew Lawrence"
  studentAddress = "latham.fell@base2s.com"
  # in production, advisorAddress will be dmcgrath@eecs.oregonstate.edu
  advisorAddress = "felll@engr.orst.edu"
  subject = "Advising Signup with McGrath, D Kevin confirmed for " + studentName
  date = "Friday, January 30th, 2015"
  timeStart = "3:00 pm"
  timeEnd = "3:30 pm"
  body = 'Advising Signup with McGrath, D Kevin confirmed\n' \
    'Name: ' + studentName + '\n' \
    'Email: ' + studentAddress + '\n' \
    'Date: ' + date + '\n' \
    'Time: ' + timeStart + ' - ' + timeEnd + '\n\n\n' \
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

def sendCancellation():
  # set email values
  fromAddress = "do.not.reply@engr.orst.edu"
  studentName = "Brabham, Matthew Lawrence"
  studentAddress = "latham.fell@base2s.com"
  # in production, advisorAddress will be dmcgrath@eecs.oregonstate.edu
  advisorAddress = "felll@engr.orst.edu"
  subject = "Advising Signup Cancellation"
  date = "Friday, January 30th, 2015"
  timeStart = "3:00 pm"
  timeEnd = "3:30 pm"
  body = 'Advising Signup with Fell, Latham CANCELLED\n' \
    'Name: ' + studentName + '\n' \
    'Email: ' + studentAddress + '\n' \
    'Date: ' + date + '\n' \
    'Time: ' + timeStart + ' - ' + timeEnd + '\n\n\n' \
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
