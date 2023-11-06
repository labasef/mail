# Send emails with python

This project provides a simple wrapper function to the smtplib library to send emails.
The code in this project can be used as a module, as a package or as an executable script.

### Warning
smtp authentication must be enabled

## send_mail

The function send_mail takes the following arguments:

- subject (str): the subject of the email
- text (str): the body of the email
- files (List[str]): [optional] the list of files to attach to the email
- send_to (List[str]): the list of recipient for the email; can also be set via an environment variable "MAIL_LIST"
- send_from (str): the sender's email; can also be set via an environment variable "MAIL_FROM"
- server (str): the smtp server used to send the email; can also be set via an environment variable "MAIL_SERVER"
- login_user (str): the user to authenticate to the smtp server; can also be set via an environment variable "MAIL_USER"
- login_pass (str): the user's password to authenticate to the smtp server; can also be set via an environment variable "MAIL_PWD"

### Environment variables

The environment variables can be set using the shell command:
```commandline
export MAIL_FROM="test@example.com"
```

It is also possible to use the file `.env_template`

It then can be loaded using the shell:
```commandline
source .env_template
```
or in-code using the python library `python-dotenv`
```python
from dotenv import load_dotenv
load_dotenv(".env_template")
```

Note that environment variables will be overridden by the function arguments if both are set.

## Package

This project can also be installed as a package using pip:
```commandline
pip install .
```

Then you can import it in-code:
```python
from mail import send_mail
```

This package comes with a `__main__.py` script, so you can also run it directly:
```commandline
python3 -m mail [-h] [-s SUBJECT] -t SEND_TO [SEND_TO ...] -f SEND_FROM [--env ENV [ENV ...]] [--file FILE [FILE ...]] text
```

## Executable

You can execute the script `__main__.py` using the python interpreter:
```commandline
python3 /path/to/__main__.py [-h] [-s SUBJECT] -t SEND_TO [SEND_TO ...] -f SEND_FROM [--env ENV [ENV ...]] [--file FILE [FILE ...]] text
```
The script `__main__.py` is made executable, so you can execute it directly:
```commandline
./path/to/__main__.py [-h] [-s SUBJECT] -t SEND_TO [SEND_TO ...] -f SEND_FROM [--env ENV [ENV ...]] [--file FILE [FILE ...]] text
```