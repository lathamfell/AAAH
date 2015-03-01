# AAAH
Automated Advising Appointment Handler
Created for Oregon State University Advising Appointments

## Quick Install

    git clone https://github.com/lathamfell/AAAH.git && ln -s ~/AAAH/.procmailrc ~/.procmailrc

## Installation

1. Clone or download the code into your home directory on flip:

    `git clone https://github.com/lathamfell/AAAH.git`

2. After cloning or downloading, ensure the code is in this subfolder in your home directory:

    `~/AAAH`

    Note: If you have downloaded the code, it may be necessary to change the name of the subfolder from "AAAH-master" to "AAAH".

3. Navigate to your home directory and create a symlink with the following command:

    `ln -s ~/AAAH/.procmailrc ~/.procmailrc`

## Usage - Command Line Interface:

1. In the `~/AAAH` directory, enter the command:

    `python AAAH.py`

2. A list of scheduled appointments will be displayed. Groups of 14 appointments will be visible at once. Use the arrow keys to scroll through the full list.

3. To cancel an appointment, type the appoinment ID, followed by the Enter key. This will send a cancellation email to the student and send an iCal to you to remove the appointment from your calendar.

4. To refresh the list of appointments, type 'r'. This will remove the cancelled appointments from your display.

5. To quit the AAAH tool, type 'q'. You will be returned to the `~/AAAH` directory.

3. 
