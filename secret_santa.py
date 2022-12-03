import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Edit people names/emails:
PEOPLE = [
    {"name": "John Doe 0", "email": "jdoe0@email.com"},
    {"name": "John Doe 1", "email": "jdoe1@email.com"},
    {"name": "John Doe 2", "email": "jdoe2@email.com"},
]


def create_emails(people_from, people_to):

    emails_to_send = []

    for this_person, to_person in zip(people_from, people_to):

        email_body = f"""
        Hello, {this_person['name']}!

        You have been assigned to give a gift to:
        
        ---> {to_person['name']}!!!

        Merry Christmas!
        """

        emails_to_send.append(
            {"email_body": email_body, "email_receiver": this_person["email"]}
        )

    return emails_to_send


def send_emails(emails_to_send, sender_address, sender_pass):

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.connect("smtp.gmail.com", 587)
    session.ehlo()
    session.starttls()
    session.login(sender_address, sender_pass)

    for email in emails_to_send:

        receiver_address = email["email_receiver"]

        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = receiver_address
        message["Subject"] = "Your Secret Santa Assignment"
        message.attach(MIMEText(email["email_body"], "plain"))

        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)

    session.quit()


def someone_is_giving_to_themselves(people_from, people_to):
    return any([a == b for a, b, in zip(people_from, people_to)])


def main():

    people_from = PEOPLE.copy()
    people_to = PEOPLE.copy()

    while someone_is_giving_to_themselves(people_from, people_to):
        random.shuffle(people_to)

    emails_to_send = create_emails(people_from, people_to)

    # Edit your email/password
    # for gmail, you may need to create an "app password"
    send_emails(
        emails_to_send,
        sender_address="your-email@email.com",
        sender_pass="password",
    )


main()
