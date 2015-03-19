# AAAH

Automated Advising Appointment Handler

Created for Oregon State University EECS Advising Appointments

## Notes
- This system only works on EECS flip servers but may be easily modified to work elsewhere.
- If you forward your ENGR mail, you will need to disable email forwarding. Email forwarding overrides the procmail filter.
    - In order to check forwarding state, navigate to https://secure.engr.oregonstate.edu:8000/teach.php and click "Email Forwarding". Find this under "Email Tools" in the right menu.   

## Getting Started
1. Choose a method of installation (quick or step by step) and follow the directions below.

2. If you'd like to verify that the filter has been set-up correctly, enter the command under "User Validation". This will send a test appointment to your ENGR mail. The meeting should also be visible in the Command Line Interface (CLI). To test cancellation, locate the test meeting in the CLI and cancel by entering the number. A cancellation email should be sent to your ENGR mail.
 
3. Manage appointments via the CLI. They can be added to or removed from your Outloook calendar using the iCal links sent to your email. Use the directions below or on-screen for navigating the CLI.

## Quick Install

Copy/paste the following command into your home directory on flip.

    git clone https://github.com/lathamfell/AAAH.git && ln -s ~/AAAH/.procmailrc ~/.procmailrc && python test_install.py

## Step by Step Install

1. Clone or download the code into your home directory on flip:

    `git clone https://github.com/lathamfell/AAAH.git`

2. After cloning or downloading, ensure the code is in this subfolder in your home directory:

    `~/AAAH`

    Note: If you have downloaded the code, it may be necessary to change the name of the subfolder from "AAAH-master" to "AAAH".

3. Navigate to your home directory and create a symlink with the following command:

    `ln -s ~/AAAH/.procmailrc ~/.procmailrc`
    
## User Validation

The following command will send a test appointment signup message, which you can cancel from the command line interface.

    `python test_install.py`
    

## Usage - Command Line Interface:

1. In the `~/AAAH` directory, enter the command:

    `python AAAH.py`

2. A list of scheduled appointments will be displayed. Up to 14 appointments will be visible at one time. Use the arrow keys to scroll through the full list.

[CLI Interface Screenshot](CLI_Screenshot.png)

3. To cancel an appointment, type the appoinment ID, followed by the Enter key. This will send a cancellation email to the student and send an iCal to you to remove the appointment from your calendar.

4. To refresh the list of appointments, type 'r'. This will remove the cancelled appointments from your display.

5. To quit the AAAH tool, type 'q'. You will be returned to the `~/AAAH` directory.
