import os
from os.path import basename
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import List


class SendMailException(Exception):
    pass


def send_mail(subject: str, text: str,
              files: List[str] = None,
              *,
              send_to: List[str] = None,
              server: str = None,
              send_from: str = None,
              login_user: str = None,
              login_pass: str = None):
    """
    Email sending function.
    The parameters: send_to, server, send_from, login_user and login_pass will be read either from environment variables
     or keyword arguments; note that keyword arguments will override environment variable
    :param subject: the subject of the email
    :param text: the body of the email
    :param send_to: the list of recipient email addresses; Associated environment variable is "MAIL_TO" as a single
    string with email separated by commas "," ex: "mail1@example.com,mail2@example.com"
    :param files: the email's list of attached files
    :param server: the email provider server; Associated environment variable is "MAIL_SERVER"
    :param send_from: the sender's email address; Associated environment variable is "MAIL_FROM"
    :param login_user: the server authentication user; Associated environment variable is "MAIL_USER"
    :param login_pass: the server authentication password; Associated environment variable is "MAIL_PWD"
    :return: True if the email was sent
    """
    try:
        # Load mail configuration
        server = server or os.getenv("MAIL_SERVER")
        assert server is not None, "server kwarg must be provided or environment variable MAIL_SERVER must be set"
        send_from = send_from or os.getenv("MAIL_FROM")
        assert send_from is not None, "send_from kwarg must be provided or environment variable MAIL_FROM must be set"
        login_user = login_user or os.getenv("MAIL_USER")
        assert login_user is not None, "login_user kwarg must be provided or environment variable MAIL_USER must be set"
        login_pass = login_pass or os.getenv("MAIL_PWD")
        assert login_pass is not None, "login_pass kwarg must be provided or environment variable MAIL_PWD must be set"
        send_to = send_to or os.getenv("MAIL_TO").split(',')
        assert isinstance(send_to, list), ("send_to must be a list if passed as kwarg or a environmant variable as a "
                                           "single string with email "
                                           "separated by commas if passed as an environment variable")

        msg = MIMEMultipart()
        COMMASPACE = ', '
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        if files:
            assert isinstance(files, list), "files must be a list of file path"
        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        smtp = smtplib.SMTP(server, 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(login_user, login_pass)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        return True
    except Exception as e:
        raise SendMailException("Could not send email", e)
