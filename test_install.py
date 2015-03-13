import sys
from time import sleep
from AAAHEmail import sendSignup, sendCancellation
from AAAHDatabase import appointmentCountSQL, getAppointmentSQL, \
getAllAppointmentsSQL, appointmentExistsSQL, \
createTable, databaseCount

def main():
	print "Testing to see that AAAH has been installed properly..."
	print "Sending test signup... please wait."
	before = appointmentCountSQL()
	# before_appts = getAllAppointmentsSQL()
	sendSignup(1)
	sleep(2)
	after = appointmentCountSQL()
	if before == after - 1:
		print "SUCCESS! Appointment has been successfully added to your database."
		print "Run command 'python AAAH.py' to view your database and remove the test."
	else:
		print "FAILURE. Appointment was not added properly."
		print "Did you disable email forwarding?"
		print "https://secure.engr.oregonstate.edu:8000/teach.php?type=forward"


if __name__ == '__main__':
	main()
