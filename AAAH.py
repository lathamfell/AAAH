import curses
import smtplib
import re
from time import sleep
from AAAHEmail import sendCancellation
from AAAHDatabase import appointmentCountSQL, getAppointmentSQL, \
getAllAppointmentsSQL, appointmentExistsSQL, \
createTable

def main():
	# string to hold appointment ID
	user_input = ''
	# string to provide user feedback
	feedback = ''
	# first row of appointments to be displayed on pad
	pad_row = 0
	# how many rows of the pad can be seen at a time
	visibleRows = 12
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
		screen.addstr('                 ' \
			'Automated Advising Appointment Handler [Group 2]\n\n',
			curses.A_BOLD)
		screen.addstr('ID          ' \
			'Student                                  ' \
			'Date        ' \
			'Start   ' \
			'End   ', curses.A_UNDERLINE)

		# check how many appointments are in the database
		appmtCount = appointmentCountSQL()
		# create pad
		pad = curses.newpad(appmtCount + 1, 80)
		# pull all appointments from db and sort them
		appmtList = 0
		if appmtCount > 0:
			appmtList = getAllAppointmentsSQL()
			# write appointments to pad
			i = 0
			for row in appmtList:
				# initialize x position
				x = 0
				# set appointment variables
				ID = row[0]
				UIID = i
				studentName = row[1]
				startDatetime = row[5]
				date = startDatetime[:10]
				startTime = row[8]
				endTime = row[9]
				# write appointments to pad
				pad.addstr(i, x, str(UIID))
				pad.addstr(i, x + 12, studentName)
				pad.addstr(i, x + 53, date)
				pad.addstr(i, x + 65, startTime)
				pad.addstr(i, x + 73, endTime) 
				i += 1

		# display the pad
		pad.refresh(pad_row, 0, 2, 0, 3 + visibleRows, 79)
		# pad lower border
		screen.hline(visibleRows + 4, 0, '_', 80)
		# user menu
		screen.addstr(visibleRows+5, 0, 'Use the arrow keys to scroll through appointments.\n')
		screen.addstr('To cancel an appointment, type the ID and press Enter. The list will refresh automatically.\n')
		screen.addstr('To refresh the schedule manually, press r.\n')
		screen.addstr('To quit, press q.\n')
		screen.addstr('\n' + feedback + '\n')
		screen.addstr('Appointment ID: ')
		screen.addstr(user_input)
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
			if len(user_input) < 1:
				pass
			else:
				user_input = user_input[:len(user_input) - 1]
		# if Enter, look for appointment 
		elif command == 10:
			if len(user_input) == 0:
				feedback = ''
			# elif len(user_input) < 10 and len(user_input) > 0:
			#   feedback = 'Appointment ID is too short'
			#   user_input = ''
			elif (int(user_input) >= appmtCount):
				feedback = 'Index '+ user_input +' out of range'
				user_input = ''
			else:
				uid = appmtList[int(user_input)][0]
				# feedback = str(uid[0])
				row = getAppointmentSQL(uid)
				if not appointmentExistsSQL(uid):
					feedback = 'ERROR...That is not a valid appointment ID'
					nuser_input = ''
				else:
					feedback = "SUCCESS!\n"
					# pull appointment row from db
					sendCancellation(row[1], # studentName
						row[2], # studentAddress
						row[4], # advisorAddress
						row[7], # date with day
						row[8], # start time 12H
						row[9]) # end time 12H
					feedback = 'Cancellation email sent for appointment ' + user_input + ' [' + row[1] + ']'
					user_input = ''
					# sleep for .5? seconds allows handler time to remove the appt.
					sleep(0.5)
			# if digit, add it to appointment ID string
		try:
			if re.match('\d', chr(command)):
				user_input += chr(command)
		except:
			pass

	# terminate the curses application
	curses.nocbreak()
	screen.keypad(0)
	curses.echo()
	curses.endwin()

if __name__ == '__main__':
	main()
