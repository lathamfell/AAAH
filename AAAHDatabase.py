import MySQLdb
import warnings
from contextlib import closing
import json

def main():
	print "Enter s to add a SQL appointment (set attr in code first).\n" \
	"Enter w to remove a SQL appointment (set uid in code first).\n" \
	"Enter e to see if SQL appointment exists (set uid in code first).\n" \
	"Enter l to print the number of appointments in database.\n" \
	"Enter i to create the SQL table.\n" \
	"Enter d to drop the SQL table.\n" \
	"Enter q to exit."
	while True:
		command = raw_input()
		if command == 's' or command == 'S':
			addAppointmentSQL("1401301500",
				"Brabham, Matrhew Lawrence",
				"lathamfell@gmail.com",
				"McGrath, D Kevin",
				"felll@engr.orst.edu",
				"2015-01-30 15:00:00-08:00",
				"2015-01-30 15:30:00-08:00",
				"Monday, January 30th, 2015",
				"3:00pm",
				"3:30pm")
		elif command == 'w' or command == 'W':
			removeAppointmentSQL("1401301506")
		elif command == 'e' or command == 'E':
			print appointmentExistsSQL("1401301506")
		elif command == 'l' or command == 'L':
			print appointmentCountSQL()
		elif command == 'i' or command == 'I':
			createTable()
		elif command == 'd' or command == 'D':
			dropTable()
		else:
			break

def createTable():
	# connect
	db = getConnection()
	# confirm there aren't any appointments yet
	if appointmentCountSQL() < 1:
		with closing(db.cursor()) as cur:
			# disable warning issued when dropping table that doesn't exist
			warnings.filterwarnings('ignore', 'Unknown table.*')
			cur.execute("DROP TABLE IF EXISTS APPOINTMENT")
			sql = """CREATE TABLE APPOINTMENT (
				UID VARCHAR(255) PRIMARY KEY NOT NULL ,
				STUDENT_NAME VARCHAR(255) NOT NULL,
				STUDENT_ADDRESS VARCHAR(255) NOT NULL,
				ADVISOR_NAME VARCHAR(255) NOT NULL,
				ADVISOR_ADDRESS VARCHAR(255) NOT NULL,
				START_DATETIME VARCHAR(255) NOT NULL,
				END_DATETIME VARCHAR(255) NOT NULL,
				DATE_WITH_DAY VARCHAR(255) NOT NULL,
				START_TIME_12H VARCHAR(255) NOT NULL,
				END_TIME_12H VARCHAR(255) NOT NULL )"""
			try:
				cur.execute(sql)
				db.commit()
				db.close()
				return True
			except:
				# rollback in case there was an error
				db.rollback()
				db.close()
				return False
	# disconnect
	db.close()
	return True

def appointmentCountSQL():
	db = getConnection()
	with closing(db.cursor()) as cur:
		sql = "SELECT * FROM APPOINTMENT"
		try:
			cur.execute(sql)
			count = cur.rowcount
			db.close()
			return count
		except:
			# if table doesn't exist yet, there are 0 appointments
			db.close()
			return 0

def getAppointmentSQL(uid):
	if appointmentExistsSQL(uid):
		db = getConnection()
		with closing(db.cursor()) as cur:
			sql = "SELECT * FROM APPOINTMENT WHERE UID = '%s'" % (uid)
			cur.execute(sql)
			result = cur.fetchone()
			db.close()
			return result
	else:
		return "Unexpected error while getting appointment " + uid

def getAllAppointmentsSQL():
	if appointmentCountSQL() > 0:
		db = getConnection()
		with closing(db.cursor()) as cur:
			sql = "SELECT * FROM APPOINTMENT"
			cur.execute(sql)
			result = cur.fetchall()
			db.close()
			return result  
	else:
		return "Unexpected error while getting all appointments"

def appointmentExistsSQL(uid):
	db = getConnection()
	with closing(db.cursor()) as cur:
		sql = "SELECT COUNT(1) FROM APPOINTMENT WHERE UID = '%s'" % (uid)
		try:
			cur.execute(sql)
			if cur.fetchone()[0]:
				db.close()
				return True
		except:
			# catch exception generated if table doesn't exist
			db.close()
	return False

def addAppointmentSQL(uid, 
	studentName, 
	studentAddress,
	advisorName,
	advisorAddress,
	startDatetime,
	endDatetime,
	dateWithDay,
	startTime12H,
	endTime12H):
	# connect
	db = getConnection()
	# make sure table exists
	if createTable():
		with closing(db.cursor()) as cur:
			# add the appointment
			sql = "INSERT INTO APPOINTMENT( \
				UID, \
				STUDENT_NAME, \
				STUDENT_ADDRESS, \
				ADVISOR_NAME, \
				ADVISOR_ADDRESS, \
				START_DATETIME, \
				END_DATETIME, \
				DATE_WITH_DAY, \
				START_TIME_12H, \
				END_TIME_12H ) \
				VALUES ('%s', '%s', '%s', '%s', '%s', \
				'%s', '%s', '%s', '%s', '%s' )" % \
				(uid,
					studentName,
					studentAddress,
					advisorName,
					advisorAddress,
					startDatetime,
					endDatetime,
					dateWithDay,
					startTime12H,
					endTime12H )
			try:
				cur.execute(sql)
				db.commit()
			except:
				# rollback in case there was an error
				db.rollback()
	# disconnect
	db.close() 

def removeAppointmentSQL(uid):
	db = getConnection()
	with closing(db.cursor()) as cur:
		sql = "DELETE FROM APPOINTMENT WHERE UID = '%s'" % (uid)
		try:
			cur.execute(sql)
			db.commit()
			if DEBUG:
				# write to log for debugging purposes
				with open("../AAAH/db_log", 'a') as logfile:
					logfile.write('\n' + str(tz.localize(datetime.datetime.now())))
					logfile.write(" : deleted " + uid + " from db") 
		except:
			# rollback in case there was an error
			db.rollback()
	# disconnect
	db.close() 

def dropTable():
	# connect
	db = getConnection()
	with closing(db.cursor()) as cur:
		# disable warning issued when dropping table that doesn't exist
		warnings.filterwarnings('ignore', 'Unknown table.*')
		cur.execute("DROP TABLE IF EXISTS APPOINTMENT")
		db.commit()
		db.close()

def getConnection():
	return MySQLdb.connect('mysql.eecs.oregonstate.edu', 'cs419-g2', 
		'e9wwhXXyKxpWu7Hx', 'cs419-g2')

if __name__ == '__main__':
	main()
