import curses
import smtplib
import re
import sys
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
	title_string = 'Automated Advising Appointment Handler [Group 2]\n'
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

	# check how many appointments are in the database
	appmtCount = appointmentCountSQL()
	# create database table if it doesn't exist yet
	if appmtCount < 1:
		createTable()

	# pull all appointments from db and sort them
	appmtList = getAllAppointmentsSQL()
	if appmtCount > 1:
		appmtList = sorted(appmtList, key=lambda x: x[5])

	# user input loop
	while True:
		# how many rows of the pad can be seen at a time
		window_y, window_x = screen.getmaxyx()
		if (window_x < 55 or window_y < 11):
			sys.exit("\nYour window size is too small\n")
		visibleRows = window_y - 12
		# reset padCmd
		padCmd = ''
		screen.clear()
		screen.refresh()
		if (window_x > 50):
			screen.addstr(0, (window_x-len(title_string))/2, title_string, curses.A_BOLD)
		screen.addstr(1, 0, 'ID', curses.A_UNDERLINE)
		screen.addstr(1, 4, 'Student', curses.A_UNDERLINE)
		screen.addstr(1, window_x-27, 'Date', curses.A_UNDERLINE)
		screen.addstr(1, window_x-15, 'Start', curses.A_UNDERLINE)
		screen.addstr(1, window_x-7, 'End', curses.A_UNDERLINE)

		# create pad
		pad = curses.newpad(appmtCount + 1, window_x)
		
		if appmtCount > 0:
			# write appointments to pad
			i = 0
			for row in appmtList:
				# set appointment variables
				ID = row[0]
				UIID = i
				studentName = row[1]
				startDatetime = row[5]
				date = startDatetime[:10]
				startTime = row[8]
				endTime = row[9]
				# write appointments to pad
				pad.addstr(i, 0, str(UIID))
				pad.addstr(i, 4, studentName)
				pad.addstr(i, window_x - 27, date)
				pad.addstr(i, window_x - 15, startTime)
				pad.addstr(i, window_x - 7, endTime) 
				i += 1

		# display the pad
		pad.refresh(pad_row, 0, 2, 0, 3 + visibleRows, window_x)
		# pad lower border
		screen.hline(window_y-8, 0, '_', window_x)
		# user menu
		if (window_x > 51 & window_y > 12):
			screen.addstr(window_y-7, 0, 'Use the arrow keys to scroll through appointments.\n')
			screen.addstr('To cancel an appointment, type the ID and press Enter.\n')
			screen.addstr('To refresh the schedule manually, press r.\n')
		screen.addstr('To quit, press q.\n')
		screen.addstr(feedback + '\n')
		screen.addstr('Appointment ID: ')
		screen.addstr(user_input)
		screen.refresh()
		# get user input
		command = screen.getch()
		# process user input
		# if up or down arrow, scroll pad
		if command == curses.KEY_DOWN and pad_row <= appmtCount - visibleRows - 2:
			pad_row += 1
			pad.refresh(pad_row, 0, 3, 0, 3 + visibleRows, window_x)
		elif command == curses.KEY_UP and pad_row > 0:
			pad_row -= 1
			pad.refresh(pad_row, 0, 3, 0, 3 + visibleRows, window_x)
		# quit command
		elif command == ord('q') or command == ord('Q'):
			break
		# refresh appointments
		elif command == ord('r') or command == ord('R'):
			appmtCount = appointmentCountSQL()
			appmtList = getAllAppointmentsSQL()
			if appmtCount > 1:
				appmtList = sorted(appmtList, key=lambda x: x[5])
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
					# sleep for 1 second seconds allows handler time to remove the appt.
					sleep(1)
					appmtCount = appointmentCountSQL()
					appmtList = getAllAppointmentsSQL()
					if appmtCount > 1:
						appmtList = sorted(appmtList, key=lambda x: x[5])
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
