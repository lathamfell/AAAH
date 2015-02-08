# # Table creation
# # Replace 'felll-db' with database name

#  CREATE TABLE `felll-db`.`appointment` (
# `uid` VARCHAR( 255 ) NOT NULL ,
# `studentName` VARCHAR( 255 ) NOT NULL ,
# `studentAddress` VARCHAR( 255 ) NOT NULL ,
# `advisorName` VARCHAR( 255 ) NOT NULL ,
# `advisorAddress` VARCHAR( 255 ) NOT NULL ,
# `startDatetime` VARCHAR( 255 ) NOT NULL ,
# `endDatetime` VARCHAR( 255 ) NOT NULL,
# 'dateWithDay' VARCHAR( 255 ) NOT NULL,
# 'startTime12H' VARCHAR( 255 ) NOT NULL,
# 'endTime12H' VARCHAR( 255 ) NOT NULL
# PRIMARY KEY ( `uid` )
# ) ENGINE = InnoDB 

# # Insert new appointment

# INSERT INTO `felll-db`.`appointment` (
# `uid` ,
# `studentName` ,
# `studentAddress` ,
# `advisorName` ,
# `advisorAddress` ,
# `startDatetime` ,
# `endDatetime` ,
# 'dateWithDay' ,
# 'startTime12H' ,
# 'endTime12H'
# )
# VALUES (
# 'mcgrath20150125T1530' , 
# 'Brabham, Matthew Lawrence' , 
# 'mbrabham@onid.oregonstate.edu' , 
# 'McGrath, D Kevin' , 
# 'mcgrath@eecs.oregonstate.edu' , 
# '20150330T150000' , 
# '20150330T153000' ,
# 'Monday, January 30th, 2015'
# '3:00pm',
# '3:30pm'
# );

# # Delete appointment
# DELETE FROM `appointment` 
# WHERE CONVERT(`appointment`.`uid` USING utf8) = '1501251500' 
# LIMIT 1;

import MySQLdb
import warnings
import json

def main():
  print "Enter a to add a JSON test appointment (set attributes in code first).\n" \
        "Enter r to remove a JSON appointment (set uid in code first).\n" \
        "Enter s to add a SQL appointment (set attr in code first).\n" \
        "Enter e to see if SQL appointment exists (set uid in code first).\n" \
        "Enter d to drop the SQL table.\n" \
        "Enter c to clear all appointments.\n" \
        "Enter q to exit."
  while True:
    command = raw_input()
    if command == 'a' or command == 'A':
      addAppointment("1401301506",
                     "Brabham, Matrhew Lawrence",
                     "lathamfell@gmail.com",
                     "McGrath, D Kevin",
                     "felll@engr.orst.edu",
                     "20150330T160000",
                     "20150330T173000",
                     "Monday, January 30th, 2015",
                     "3:00pm",
                     "3:30pm")
    elif command == 'r' or command == 'R':
      removeAppointment("1001301500")
    elif command == 's' or command == 'S':
      addAppointmentSQL("1401301506",
                        "Brabham, Matrhew Lawrence",
                        "lathamfell@gmail.com",
                        "McGrath, D Kevin",
                        "felll@engr.orst.edu",
                        "20150330T160000",
                        "20150330T173000",
                        "Monday, January 30th, 2015",
                        "3:00pm",
                        "3:30pm")
    elif command == 'e' or command == 'E':
      if appointmentExistsSQL("1401301506"):
        print 'True'
      elif not appointmentExistsSQL("1401301506"):
        print 'False'
      else:
        print 'Error'
    elif command == 'd' or command == 'D':
      dropTable()
    elif command == 'c' or command == 'C':
      removeAllAppointments()
    else:
      break

def appointmentCount():
  try:
    appointmentsJSON = json.load(open("../AAAH/appointmentsList"))
    return len(appointmentsJSON)
  except:
    # if error in opening file, there are no appointments yet
    return 0

def getAppointment(uid):
  if appointmentExists(uid):
    appointmentsJSON = json.load(open("../AAAH/appointmentsList"))
    for i in xrange(len(appointmentsJSON)):
      if appointmentsJSON[i]["uid"] == uid:
        return appointmentsJSON[i]
        break
  else:
    # return empty JSON list
    return json.loads(json.dumps([]))

def getAllAppointments():
  if appointmentCount() > 0:
    appointmentsJSON = json.load(open("../AAAH/appointmentsList"))
    return appointmentsJSON
  else:
    # return empty JSON list
    return json.loads(json.dumps([]))

def appointmentExists(uid):
  if appointmentCount() > 0:
    appointmentsJSON = json.load(open("../AAAH/appointmentsList"))
    for appointment in appointmentsJSON:
      if appointment['uid'] == uid:
        return True
    return False
  else:
    return False

def appointmentExistsSQL(uid):
  db = MySQLdb.connect('mysql.eecs.oregonstate.edu', 'cs419-g2', 
                       'e9wwhXXyKxpWu7Hx', 'cs419-g2')
  cursor = db.cursor()
  sql = "SELECT COUNT(1) FROM APPOINTMENT \
         WHERE UID = '%s'" % (uid)
  cursor.execute(sql)
  if cursor.fetchone()[0]:
    return True
  else:
    return False

def addAppointment(uid, 
                   studentName, 
                   studentAddress,
                   advisorName,
                   advisorAddress,
                   startDatetime,
                   endDatetime,
                   dateWithDay,
                   startTime12H,
                   endTime12H):
  try:
    appointmentsJSON = json.load(open("../AAAH/appointmentsList"))
    # appointment list already exists
    if not appointmentExists(uid):
      appointmentsJSON.append({'uid': uid,
                               'studentName': studentName,
                               'studentAddress': studentAddress,
                               'advisorName': advisorName,
                               'advisorAddress': advisorAddress,
                               'startDatetime': startDatetime,
                               'endDatetime': endDatetime,
                               'dateWithDay': dateWithDay,
                               'startTime12H': startTime12H,
                               'endTime12H': endTime12H })
    with open("../AAAH/appointmentsList", 'w+') as appointmentsList:
      json.dump(appointmentsJSON, appointmentsList)
  except:
    # appointment list doesn't exist yet
    with open("../AAAH/appointmentsList", 'w+') as appointmentsList:
      json.dump([{'uid': uid,
                 'studentName': studentName,
                 'studentAddress': studentAddress,
                 'advisorName': advisorName,
                 'advisorAddress': advisorAddress,
                 'startDatetime': startDatetime,
                 'endDatetime': endDatetime,
                 'dateWithDay': dateWithDay,
                 'startTime12H': startTime12H,
                 'endTime12H': endTime12H }], appointmentsList)

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
  db = MySQLdb.connect('mysql.eecs.oregonstate.edu', 'cs419-g2', 
                       'e9wwhXXyKxpWu7Hx', 'cs419-g2')
  # create new appointments table
  cursor = db.cursor()
  # disable warning issued when dropping table that doesn't exist
  warnings.filterwarnings('ignore', 'Unknown table.*')
  cursor.execute("DROP TABLE IF EXISTS APPOINTMENT")
  sql = """CREATE TABLE APPOINTMENT (
           UID  VARCHAR(255) NOT NULL,
           STUDENT_NAME VARCHAR(255) NOT NULL,
           STUDENT_ADDRESS VARCHAR(255) NOT NULL,
           ADVISOR_NAME VARCHAR(255) NOT NULL,
           ADVISOR_ADDRESS VARCHAR(255) NOT NULL,
           START_DATETIME VARCHAR(255) NOT NULL,
           END_DATETIME VARCHAR(255) NOT NULL,
           DATE_WITH_DAY VARCHAR(255) NOT NULL,
           START_TIME_12H VARCHAR(255) NOT NULL,
           END_TIME_12H VARCHAR(255) NOT NULL )"""
  cursor.execute(sql)
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
    cursor.execute(sql)
    db.commit()
  except:
    # rollback in case there was an error
    db.rollback()
  # disconnect
  db.close()

def dropTable():
  # connect
  db = MySQLdb.connect('mysql.eecs.oregonstate.edu', 'cs419-g2', 
                       'e9wwhXXyKxpWu7Hx', 'cs419-g2')
  # create new appointments table
  cursor = db.cursor()
  # disable warning issued when dropping table that doesn't exist
  warnings.filterwarnings('ignore', 'Unknown table.*')
  cursor.execute("DROP TABLE IF EXISTS APPOINTMENT")  

def removeAppointment(uid):
  if appointmentExists(uid):
    appointmentsJSON = json.load(open("../AAAH/appointmentsList"))
    for i in xrange(len(appointmentsJSON)):
      if appointmentsJSON[i]['uid'] == uid:
        appointmentsJSON.pop(i)
        break
    with open("../AAAH/appointmentsList", 'w+') as appointmentsList:
      json.dump(appointmentsJSON, appointmentsList)

def removeAllAppointments():
  if appointmentCount() > 0:
    with open("../AAAH/appointmentsList", 'w+') as appointmentsList:
      json.dump([], appointmentsList)

if __name__ == '__main__':
  main()






















