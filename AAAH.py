import curses
import smtplib

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
  # string to provide user feedback
  feedback = ''
  # first row of appointments to be displayed on pad
  pad_row = 0
  # holds scrolling commands
  padCmd = ''
  # initialize application screen
  screen = curses.initscr()
  # turn on echo
  curses.echo()
  # turn off cbreak
  curses.nocbreak()
  # enable curses to translate special key inputs, such as arrow keys
  screen.keypad(1)
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
    screen.addstr('\nID  ' \
                  'Student                   ' \
                  'Advisor                   ' \
                  'Date        ' \
                  'Start  ' \
                  'End  ', curses.A_UNDERLINE)
    # create pad
    pad = curses.newpad(1000, 80)
    # write appointments to pad
    for i in range(20):
      # initialize x position
      x = 0
      # set appointment variables
      number = i + 1
      studentUsername = 'felll'
      advisorUsername = 'mcgrath'
      date = '2015-01-20'
      start = '14:20'
      end = '15:20'
      # write appointment to screen
      pad.addstr(i, x, str(number))
      pad.addstr(i, x + 4, studentUsername)
      pad.addstr(i, x + 30, advisorUsername)
      pad.addstr(i, x + 56, date)
      pad.addstr(i, x + 68, start)
      pad.addstr(i, x + 75, end) 
    # display the pad
    pad.refresh(pad_row, 0, 3, 0, 9, 79)
    # pad lower border
    screen.hline(10, 0, curses.A_UNDERLINE, 80)
    # user menu
    screen.addstr(12, 0, 'The following options are available:\n')
    screen.addstr('1: Cancel an existing appointment\n')
    screen.addstr('2: Scroll through appointments\n')
    screen.addstr('3: Refresh appointment schedule\n')
    screen.addstr('4: Exit\n')
    screen.addstr('\n' + feedback + '\n')
    screen.addstr('\nPlease enter your selection: ')
    screen.refresh()
    # get user input
    command = screen.getstr()
    # process user input
    if command == '1':
      screen.addstr('\nPlease enter the appointment ID, ' \
        'or "b" to go back: ')
      feedback = ''
      screen.refresh()
      appmtID = screen.getstr()
      if appmtID == 'b':
        pass
      else:
        try: 
          appmtID = int(appmtID)
          if appmtID < 1 or appmtID > 20:
            feedback = 'That is not a valid appointment ID'
          else:
            feedback = 'Cancellation email sent for appointment ' + str(appmtID)
            sendCancellation()      
        except:
          feedback = 'That is not a valid appointment ID'
    elif command == '2':
      # turn off echo
      curses.noecho()
      # turn on cbreak
      curses.cbreak()
      # turn off cursor
      curses.curs_set(0)
      screen.addstr('\nPress up and down arrows to scroll, or "b" to go back ')
      while padCmd != ord('b'):
        padCmd = screen.getch()
        if padCmd == curses.KEY_DOWN:
          pad_row += 1
        if padCmd == curses.KEY_UP:
          pad_row -= 1
        pad.refresh(pad_row, 0, 3, 0, 9, 79)
      # restore curses settings
      curses.echo()
      curses.nocbreak()
      curses.curs_set(1)
      feedback = ''
    elif command == '3':
      feedback = 'Appointments refreshed'
      pad_row = 0
    elif command == '4':
      break
    else:
      feedback = 'Sorry, that is not a valid option'

# terminate the curses application
  curses.nocbreak()
  screen.keypad(0)
  curses.echo()
  curses.endwin()

if __name__ == '__main__':
  main()
