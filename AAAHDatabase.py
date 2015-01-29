# # Table creation
# # Replace 'felll-db' with database name

#  CREATE TABLE `felll-db`.`appointment` (
# `uid` VARCHAR( 255 ) NOT NULL ,
# `studentName` VARCHAR( 255 ) NOT NULL ,
# `studentAddress` VARCHAR( 255 ) NOT NULL ,
# `advisorName` VARCHAR( 255 ) NOT NULL ,
# `advisorAddress` VARCHAR( 255 ) NOT NULL ,
# `start` DATETIME NOT NULL ,
# `end` DATETIME NOT NULL ,
# PRIMARY KEY ( `uid` )
# ) ENGINE = InnoDB 

# # Insert new appointment

# INSERT INTO `felll-db`.`appointment` (
# `uid` ,
# `studentName` ,
# `studentAddress` ,
# `advisorName` ,
# `advisorAddress` ,
# `start` ,
# `end`
# )
# VALUES (
# 'mcgrath20150125T1530', 
# 'Brabham, Matthew Lawrence', 
# 'mbrabham@onid.oregonstate.edu', 
# 'McGrath, D Kevin', 
# 'mcgrath@eecs.oregonstate.edu', 
# '2015-01-25 15:30:00', 
# '2015-01-25 16:30:00'
# );

# # Delete appointment
# DELETE FROM `appointment` 
# WHERE CONVERT(`appointment`.`uid` USING utf8) = 'mcgrath20150125T1530' 
# LIMIT 1;

import MySQLdb
import json

def main():
  print "Enter a to add a test appointment.\n" \
        "Enter r to remove the test appointment.\n" \
        "Enter q to exit."
  while True:
    command = raw_input()
    if command == "a" or command == "A":
      addAppointment("dmcgrath20150130T150002",
                     "Brabham, Matthew Lawrence",
                     "latham.fell@base2s.com",
                     "McGrath, D Kevin",
                     "felll@engr.orst.edu",
                     "20150130T150000",
                     "20150130T153000")
    elif command == "r" or command == "R":
      removeAppointment("dmcgrath20150130T150002")
    else:
      break

def appointmentExists(uid):
  try:
    appointmentsJSON = json.load(open("appointmentsList"))
    for appointment in appointmentsJSON:
      if appointment['uid'] == uid:
        return True
    return False
  except:
    # if error in opening file, there are no appointments yet
    return False

def addAppointment(uid, 
                   studentName, 
                   studentAddress,
                   advisorName,
                   advisorAddress,
                   start,
                   end):
  try:
    appointmentsJSON = json.load(open("appointmentsList"))
    # appointment list already exists
    if not appointmentExists(uid):
      appointmentsJSON.append({'uid': uid,
                               'studentName': studentName,
                               'studentAddress': studentAddress,
                               'advisorName': advisorName,
                               'advisorAddress': advisorAddress,
                               'start': start,
                               'end': end})
    with open("appointmentsList", 'w+') as appointmentsList:
      json.dump(appointmentsJSON, appointmentsList)
  except:
    # appointment list doesn't exist yet
    with open("appointmentsList", 'w+') as appointmentsList:
      json.dump([{'uid': uid,
                 'studentName': studentName,
                 'studentAddress': studentAddress,
                 'advisorName': advisorName,
                 'advisorAddress': advisorAddress,
                 'start': start,
                 'end': end}], appointmentsList)

def removeAppointment(uid):
  if appointmentExists(uid):
    appointmentsJSON = json.load(open("appointmentsList"))
    for i in xrange(len(appointmentsJSON)):
      if appointmentsJSON[i]["uid"] == uid:
        appointmentsJSON.pop(i)
        break
    with open("appointmentsList", 'w+') as appointmentsList:
      json.dump(appointmentsJSON, appointmentsList)

if __name__ == '__main__':
  main()






















