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

def main():
  print "Enter a to add a test appointment.\n" \
        "Enter r to remove the test appointment.\n" \
        "Enter q to exit."
  while True:
    command = raw_input()
    if command == "a" or command == "A":
      addAppointment()
    elif command == "r" or command == "R":
      removeAppointment()
    else:
      break

def appointmentExists(uid):
  return True

def addAppointment(uid, 
                   studentName, 
                   studentAddress,
                   advisorName,
                   advisorAddress,
                   start,
                   end):
  pass

def removeAppointment(uid):
  pass

if __name__ == '__main__':
  main()






















