import curses
import smtplib
import random
import re
from AAAHEmail import sendCancellation
from AAAHDatabase import appointmentCount, getAppointment, \
                         getAllAppointments, appointmentExists
from AAAHDatabase import appointmentCountSQL, getAppointmentSQL, \
                         getAllAppointmentsSQL, appointmentExistsSQL, \
                         createTable
from operator import itemgetter

def main():
  # string to hold appointment ID
  uid = ''
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
  # create database table if it doesn't exist yet
  if appointmentCountSQL < 1:
    createTable()
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
    screen.addstr('\nID          ' \
                  'Student                                   ' \
                  'Date        ' \
                  'Start  ' \
                  'End    ', curses.A_UNDERLINE)

    # """ This code block uses old JSON 'database' """
    # # check how many appointments are in the database
    # appmtCount = appointmentCount()
    # # create pad
    # pad = curses.newpad(appmtCount + 1, 80)
    # # get the appointments and sort them
    # appmtList = getAllAppointments()
    # appmtList = sorted(appmtList, key=itemgetter('uid'))
    # # write appointments to pad
    # i = 0
    # for i in xrange(len(appmtList)):
    #   # initialize x position
    #   x = 0
    #   # set appointment variables
    #   ID = appmtList[i]['uid']
    #   studentName = appmtList[i]['studentName']
    #   startDatetime = appmtList[i]['startDatetime']
    #   date = startDatetime[:10]
    #   startTime = startDatetime[11:16]
    #   endDatetime = appmtList[i]['endDatetime']
    #   endTime = endDatetime[11:16]
    #   # write appointments to pad
    #   pad.addstr(i, x, str(ID))
    #   pad.addstr(i, x + 12, studentName)
    #   pad.addstr(i, x + 56, date)
    #   pad.addstr(i, x + 68, startTime)
    #   pad.addstr(i, x + 75, endTime) 

    """ This code block uses new MySQL database """
    # check how many appointments are in the database
    appmtCount = appointmentCountSQL()
    # create pad
    pad = curses.newpad(appmtCount + 1, 80)
    # pull all appointments from db and sort them
    if appmtCount > 0:
      appmtList = getAllAppointmentsSQL()
      # write appointments to pad
      i = 0
      for row in appmtList:
        # initialize x position
        x = 0
        # set appointment variables
        ID = row[0]
        studentName = row[1]
        startDatetime = row[5]
        date = startDatetime[:4] + '-' + \
               startDatetime[4:6] + '-' + \
               startDatetime[6:8]
        startTime = row[8]
        endTime = row[9]
        # write appointments to pad
        pad.addstr(i, x, ID)
        pad.addstr(i, x + 12, studentName)
        pad.addstr(i, x + 54, date)
        pad.addstr(i, x + 66, startTime)
        pad.addstr(i, x + 73, endTime) 
        i += 1

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
    screen.addstr(uid)
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
      if len(uid) < 1:
        pass
      else:
        uid = uid[:len(uid) - 1]
    # if Enter, look for appointment 
    elif command == 10:
      if len(uid) == 0:
        feedback = ''
      elif len(uid) < 10 and len(uid) > 0:
        feedback = 'Appointment ID is too short'
        uid = ''
      else:
        if not appointmentExists(uid):
          feedback = 'That is not a valid appointment ID'
          uid = ''
        else:
          # pull appointment from db
          appointment = getAppointment(uid)
          sendCancellation(appointment['studentName'],
                           appointment['studentAddress'],
                           appointment['advisorAddress'],
                           appointment['dateWithDay'],
                           appointment['startTime12H'],
                           appointment['endTime12H'])
          # give feedback
          feedback = 'Cancellation email sent for appointment ' + uid
          uid = ''
    # if digit, add it to appointment ID string
    try:
      if re.match('\d', chr(command)):
        uid += chr(command)
    except:
      pass

# terminate the curses application
  curses.nocbreak()
  screen.keypad(0)
  curses.echo()
  curses.endwin()

if __name__ == '__main__':
  main()
