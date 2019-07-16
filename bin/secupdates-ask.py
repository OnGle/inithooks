#!/usr/bin/python3
# Copyright (c) 2010 Alon Swartz <alon@turnkeylinux.org>
"""Install security updates"""

import sys
import getopt
import signal

from executil import ExecError, getoutput
from subprocess import check_output, CalledProcessError
from dialog_wrapper import Dialog

TEXT = """By default, this system is configured to automatically install security updates on a daily basis:

https://www.turnkeylinux.org/security-updates

For maximum protection, we also recommend installing the latest security updates right now.

This can take a few minutes. You need to be online.
"""

CONNECTIVITY_ERROR = """Unable to connect to package archive.

Please try again once your network settings are configured by using the following shell command:

    turnkey-install-security-updates
"""

def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s [options]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)

def main():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ['help'])
    except getopt.GetoptError as e:
        usage(e)

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

    d = Dialog("TurnKey GNU/Linux - First boot configuration")
    install = d.yesno("Security updates", TEXT, "Install", "Skip")

    if not install:
        sys.exit(1)

    try:
        check_output(["host", "-W", "2", "archive.turnkeylinux.org"])
    except CalledProcessError as e:
        d.error(CONNECTIVITY_ERROR)
        sys.exit(1)

if __name__ == "__main__":
    main()

