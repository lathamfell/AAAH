# AAAH
Automated Advising Appointment Handler

To use, clone into your home directory on flip.

Set your .procmailrc to:

# .procmailrc
# for CS419 final project
PATH=/bin:/usr/bin:/usr/local/bin
MAILDIR=$HOME/AAAH/mailbox
DEFAULT=$MAILDIR/inbox
LOGFILE=$MAILDIR/proclogfile
SHELL=/bin/sh

:0:
* ^Subject.*Advising Signup Cancellation
{
  :0 c
  cancellation

  :0
  | /usr/bin/python handler.py
}

:0:
* ^Subject.*Advising Signup
{
  :0 c
  signup

  :0
  | /usr/bin/python handler.py
}
