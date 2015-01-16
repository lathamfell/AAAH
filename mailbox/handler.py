# database import
import MySQLdb
# for sending email
import smtplib
# for encoding email
import email
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
#from email import encoders
import os, datetime

def main():
  CRLF = "\r\n"
  # db = MySQLdb.connect('oniddb.cws.oregonstate.edu', 
  #                      'felll-db',
  #                      'Qo8KoTmgkOUFj7bs', 
  #                      'felll-db')
  # cur = db.cursor()
  
  # trival script to tell when main function is called
  target = open('pyfile', 'w+')
  target.write("my py info")
  target.close()

  # send a multipart MIME with simple components
  msg = MIMEMultipart('mixed')
  msg['Subject'] = 'AAAH Release Party'
  me = 'felll@engr.orst.edu'
  you = ['latham.fell@base2s.com', 'latham.e.fell@boeing.com']
  msg['From'] = me
  msg['To'] = ", ".join(you)
  msg['Date'] = email.utils.formatdate(time.time(), localtime=True)
  # component 1, email part
  emailPart = MIMEMultipart('alternative')
  # component 1a, text
  text = 'When: Thursday, January 22, 2015 2:00 PM-2:30 PM. (UTC-08:00) Pacific Time = (US & Canada)'
  textPart = MIMEText(text, 'plain', 'iso-8859-1')
  emailPart.attach(textPart)
  # component 1b, html
  html = '<html><head></head><body>This is html</body><html>'
  htmlPart = MIMEText(html, 'html', 'iso-8859-1')
  emailPart.attach(htmlPart)
  # component 1c, calendar
  ical = "BEGIN:VCALENDAR" + CRLF 
  ical += "METHOD:REQUEST" + CRLF
  ical += "PRODID:AAAH" + CRLF
  ical += "VERSION:2.0" + CRLF
  ical += "BEGIN:VEVENT" + CRLF
  ical += "ORGANIZER;CN='McGrath':MAILTO:felll@engr.orst.edu" + CRLF
  # loop to add all attendees
  for attendee in you:
    ical += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+attendee+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+attendee+CRLF
  ical += "DESCRIPTION;LANGUAGE=en-US:When: Thursday\, January 22\, 2015 2:00 PM-2:30 PM. (UTC-08:00) Pacific Time (US & Canada)\n\n*~*~*~*~*~*~*~*~*~*\n\n\n" + CRLF 
  ical += "SUMMARY;LANGUAGE=en-US:AAAH Release Party" + CRLF
  dtstart = email.utils.formatdate(time.time(), localtime=True)
  ical += "DTSTART;TZID=Pacific Standard Time:" + dtstart + CRLF
  dtend = email.utils.formatdate(time.time(), localtime=True)
  ical += "DTEND;TZID=Pacific Standard Time:" + dtend + CRLF
  ical += "UID:mcgrath" + CRLF
  ical += "CLASS:PUBLIC" + CRLF
  ical += "PRIORITY:5" + CRLF
  dtstamp = email.utils.formatdate(time.time(), localtime=True)
  ical += "DTSTAMP:" + dtstamp + CRLF
  ical += "TRANSP:OPAQUE" + CRLF
  ical += "STATUS:CONFIRMED" + CRLF
  ical += "SEQUENCE:0" + CRLF 
  ical += "END:VEVENT" + CRLF
  ical += "END:VCALENDAR" + CRLF
  calPart = MIMEText(ical, 'calendar;method=REQUEST')
  emailPart.attach(calPart)
  # component 2, ics attachment
  icsPart = MIMEBase('application/ics', ' ;name="invite.ics"')
  icsPart.set_payload(ical)
  email.encoders.encode_base64(icsPart)
  icsPart.add_header('Content-Disposition', 'attachment; filename="invite.ics"')

  # attach the two components
  msg.attach(emailPart)
  msg.attach(icsPart)

  # send it
  s = smtplib.SMTP('mail.oregonstate.edu')
  s.sendmail(me, you, msg.as_string())
  s.quit()


  # part_email = MIMEText(eml_body,"html")
  # part_cal = MIMEText(ical,'calendar;method=REQUEST')

  # msgAlternative = MIMEMultipart('alternative')
  # msg.attach(msgAlternative)

  # ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
  # ical_atch.set_payload(ical)
  # Encoders.encode_base64(ical_atch)
  # ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

  # eml_atch = MIMEBase('text/plain','')
  # Encoders.encode_base64(eml_atch)
  # eml_atch.add_header('Content-Transfer-Encoding', "")

  # msgAlternative.attach(part_email)
  # msgAlternative.attach(part_cal)


if __name__ == '__main__':
  main()
