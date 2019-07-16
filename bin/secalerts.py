#!/usr/bin/python3
"""Enable system alerts and notifications

Options:
    --email=                if not provided, will ask interactively
    --email-placeholder=    placeholder when asking interactively

"""

import os
import sys
import getopt
import signal

from dialog_wrapper import Dialog, email_re
from subprocess import call

TITLE = "System Notifications and Critical Security Alerts"

TEXT = """Enable local system notifications (root@localhost) to be forwarded to your regular inbox. Notifications include security updates and system messages.

You will also be subscribed to receive critical security and bug alerts through a low-traffic Security and News announcements newsletter. You can unsubscribe at any time.

https://www.turnkeylinux.org/security-alerts

Email:
"""

def fatal(e):
    print("Error:", e, file=sys.stderr)
    sys.exit(1)

def warn(e):
    print("Warning:", e, file=sys.stderr)

def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s [options]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)

def main():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        l_opts = ["help", "email=", "email-placeholder="]
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", l_opts)
    except getopt.GetoptError as e:
        usage(e)

    email = ""
    email_placeholder = ""
    for opt, val in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt == "--email":
            email = val
        elif opt == "--email-placeholder":
            email_placeholder = val

    if email and not email_re.match(email):
        fatal("email is not valid")

    if not email:
        d = Dialog("TurnKey Linux - First boot configuration")
        email = email_placeholder
        while 1:
            retcode, email = d.inputbox(
                TITLE,
                TEXT,
                email,
                "Enable",
                "Skip")

            if retcode == 1:
                email = ""
                break

            if not email_re.match(email):
                d.error('Email is not valid')
                continue

            if d.yesno("Is your email correct?", email):
                break

    if email:
        cmd = os.path.join(os.path.dirname(__file__), 'secalerts.sh')
        call(cmd, email)


if __name__ == "__main__":
    main()

