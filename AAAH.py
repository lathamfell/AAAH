import curses
import smtplib
import random
import re

def sendCancellation():
  # set email values
  fromAddress = 'do.not.reply@engr.orst.edu'
  studentAddress = 'felll@engr.orst.edu'
  advisorAddress = 'lathamfell@gmail.com'
  subject = 'Advising Signup Cancellation'
  date = 'Thursday, November 15th, 2012'
  timeStart = '11:00 am'
  timeEnd = '11:15 am'
  body = 'Advising Signup with Fell, Latham CANCELLED\n' \
    'Name: Latham Fell\n' \
    'Email: felll@engr.orst.edu\n' \
    'Date: ' + date + '\n' \
    'Time: ' + timeStart + ' - ' + timeEnd + '\n\n\n' \
    'Please contact support@engr.oregonstate.edu if you ' \
    'experience problems'
  # construct email in proper format
  msg = 'From: ' + fromAddress + '\n' + \
        'To: ' + studentAddress + ' ' + advisorAddress + '\n' + \
        'Subject: ' + subject + '\n\n' + \
        body
  # send the email
  s = smtplib.SMTP('mail.oregonstate.edu')
  s.sendmail(fromAddress, [studentAddress, advisorAddress], msg)

def main():
  # string to hold appointment ID
  appmtID = ''
  # string to provide user feedback
  feedback = ''
  # first row of appointments to be displayed on pad
  pad_row = 0
  # how many rows of the pad can be seen at a time
  visibleRows = 7
  # holds scrolling commands
  padCmd = ''
  # initialize application screen
  screen = curses.initscr()
  # enable curses to translate special key inputs, such as arrow keys
  screen.keypad(1)
  # turn off cbreak
  curses.cbreak()
  # turn on echo
  curses.echo()
  # enable window scrolling
  # screen.scrollok(1)
  # user input loop
  while True:

    # reset padCmd
    padCmd = ''
    screen.clear()
    screen.refresh()
    screen.addstr('                     ' \
                  'Automated Advising Appointment Handler' \
                  '                     ',
                  curses.A_BOLD)
    screen.addstr('\nID      ' \
                  'Student                 ' \
                  'Advisor                 ' \
                  'Date        ' \
                  'Start  ' \
                  'End  ', curses.A_UNDERLINE)
    # check how many appointments are in the database
    appmtCount = 15
    # create pad
    pad = curses.newpad(appmtCount + 1, 80)
    # write appointments to pad
    for i in range(appmtCount):
      # initialize x position
      x = 0
      # set appointment variables
      ID = i + 100000
      studentUsername = 'felll'
      advisorUsername = 'mcgrath'
      date = '2015-01-20'
      start = '14:20'
      end = '15:20'
      # write appointments to pad
      pad.addstr(i, x, str(ID))
      pad.addstr(i, x + 8, studentUsername)
      pad.addstr(i, x + 32, advisorUsername)
      pad.addstr(i, x + 56, date)
      pad.addstr(i, x + 68, start)
      pad.addstr(i, x + 75, end) 
    # display the pad
    pad.refresh(pad_row, 0, 3, 0, 3 + visibleRows, 79)
    # pad lower border
    screen.hline(3 + visibleRows + 1, 0, curses.A_UNDERLINE, 80)
    # user menu
    screen.addstr(12, 0, '\nUse the arrow keys to scroll through appointments.')
    screen.addstr('\nTo cancel an appointment, type the ID and press Enter.')
    screen.addstr('\nTo refresh the schedule, press r.')
    screen.addstr('\nTo quit, press q.')
    screen.addstr('\n\n' + feedback + '\n')
    screen.addstr('\nAppointment ID: ')
    screen.addstr(appmtID)
    screen.refresh()
    # get user input
    command = screen.getch()
    # process user input
    # if up or down arrow, scroll pad
    if command == curses.KEY_DOWN and pad_row <= appmtCount - visibleRows - 2:
      pad_row += 1
      pad.refresh(pad_row, 0, 3, 0, 3 + visibleRows, 79)
    elif command == curses.KEY_UP and pad_row > 0:
      pad_row -= 1
      pad.refresh(pad_row, 0, 3, 0, 3 + visibleRows, 79)
    # quit command
    elif command == ord('q') or command == ord('Q'):
      break
    # refresh appointments
    elif command == ord('r') or command == ord('R'):
      feedback = 'Schedule refreshed'
      pad_row = 0
    # if backspace, delete a char from appointment ID string
    elif command == 8:
      if len(appmtID) < 1:
        pass
      else:
        appmtID = appmtID[:len(appmtID) - 1]
    # if Enter, look for appointment 
    elif command == 10:
      if len(appmtID) == 0:
        feedback = ''
      elif len(appmtID) < 6 and len(appmtID) > 0:
        feedback = 'Appointment ID is too short'
        appmtID = ''
      else:
        appmtID = int(appmtID)
        if appmtID < 100000 or appmtID > 150000:
          feedback = 'That is not a valid appointment ID'
          appmtID = ''
        else:
          feedback = 'Cancellation email sent for appointment ' + str(appmtID)
          sendCancellation()
          appmtID = ''
    # if digit, add it to appointment ID string
    try:
      if re.match('\d', chr(command)):
        appmtID += chr(command)
    except:
      pass

# terminate the curses application
  curses.nocbreak()
  screen.keypad(0)
  curses.echo()
  curses.endwin()

if __name__ == '__main__':
  main()
