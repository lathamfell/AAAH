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
  print "Enter a to add a test appointment (set attributes in code first).\n" \
        "Enter r to remove an appointment (set uid in code first).\n" \
        "Enter c to clear all appointments.\n" \
        "Enter q to exit."
  while True:
    command = raw_input()
    if command == "a" or command == "A":
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
    elif command == "r" or command == "R":
      removeAppointment("1001301500")
    elif command == "c" or command == "C":
      removeAllAppointments()
    elif command == 's' or command == 'S':
      addAppointmentSQL()
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

def addAppointmentSQL():
  print 'in function'
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
           STUDENTNAME VARCHAR(255) NOT NULL,
           STUDENTADDRESS VARCHAR(255) NOT NULL,
           ADVISORNAME VARCHAR(255) NOT NULL,
           ADVISORADDRESS VARCHAR(255) NOT NULL,
           STARTDATETIME VARCHAR(255) NOT NULL,
           ENDDATETIME VARCHAR(255) NOT NULL,
           DATEWITHDAY VARCHAR(255) NOT NULL,
           STARTTIME12H VARCHAR(255) NOT NULL,
           ENDTIME12H VARCHAR(255) NOT NULL )"""
  cursor.execute(sql)
  # add the appointment
  
  db.close()

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






















