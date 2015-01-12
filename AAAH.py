import curses
import smtplib

# counter to debug appointment refresh
counter = 0

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
  try:
    s.sendmail(fromAddress, [studentAddress, advisorAddress], msg)
    print 'Cancellation email sent'
  except:
    print 'Cancellation email not sent, unknown error'

def showAppointments(screen):
  # redisplay appointments to console
  screen.addstr(4, 0, '\nAPPOINTMENTS FROM DATABASE GO HERE\n')
  # display refresh count for debugging
  global counter
  screen.addstr('REFRESHED ' + str(counter) + ' TIMES')
  counter += 1

def main():
  # initialize application screen
  screen = curses.initscr()
  # keep keys from being echoed while in curses mode
  curses.noecho()
  # enable application to respond instantly to key presses
  curses.cbreak()
  # enable curses to translate special key inputs, such as arrow keys
  screen.keypad(1)
  # user input loop
  while True:
    screen.addstr('Welcome to AAAH!  The Automated Advising ' \
      'Appointment Handler\n')
    screen.addstr('Please note this system is personally calibrated ' \
      'to D Robert McGrath\n')
    screen.addstr('\nProfessor McGrath, your current advising ' \
      'appointment schedule is:\n')
    showAppointments(screen)
    screen.addstr('\n\nThe following options are available:\n')
    screen.addstr('1: Cancel an existing appointment\n')
    screen.addstr('2: Refresh appointment schedule\n')
    screen.addstr('3: Exit\n')
    screen.addstr('\nPlease enter your selection: ')
    screen.refresh()
    # get user input
    command = screen.getch()
    # process user input
    if command == ord('1'):
      sendCancellation()
      screen.clear()
      screen.refresh()
    elif command == ord('2'):
      showAppointments(screen)
    elif command == ord('3'):
      break
    else:
      screen.addstr('\nSorry, that is not a valid option')

# terminate the curses application
  curses.nocbreak()
  screen.keypad(0)
  curses.echo()
  curses.endwin()

if __name__ == '__main__':
  main()
