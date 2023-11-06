#! /usr/bin/python

import sys
import argparse
from mail import send_mail

# Declare argument parser
parser = argparse.ArgumentParser(description="A simple interface to send emails")

parser.add_argument('-s', '--subject', type=str, help="the email's subject")

parser.add_argument('-t', '--send_to', type=str, nargs='+', action='extend',
                    help="the email's recipient list", required=True)

parser.add_argument('-f', "--send_from", type=str, help="the sender's email")

parser.add_argument('--env', nargs='+', type=str, action='extend',
                    help="provide the required environment variables as VAR=value if they are not set otherwise. "
                         "The required environment variables are the following: MAIL_SERVER, MAIL_USER and MAIL_PWD")

parser.add_argument('--file', nargs='+', type=str, action='extend',
                    help="path to email attached file")

# read email content from stdin or args
text = None
if not sys.stdin.isatty():
    input_stream = sys.stdin
    text = input_stream.read()
else:
    parser.add_argument("text", type=str, help="the content of the email")

# prepare arguments for calling send_mail function
args = parser.parse_args()

text = text if text else args.text
subject = args.subject
send_to = args.send_to

# parse environment variables flag
server, login_user, login_pass = None, None, None
for item in args.env or []:
    k, v = item.split("=")
    if k == "MAIL_SERVER":
        server = v
    elif k == "MAIL_USER":
        login_user = v
    elif k == "MAIL_PWD":
        login_pass = v

# if the sent_from email is not set, use the login_user mail
send_from = args.send_from or login_user

# call send_mail function
send_mail(subject, text,
          files=args.file,
          send_to=send_to,
          send_from=send_from,
          server=server,
          login_user=login_user,
          login_pass=login_pass)


