from twilio.rest import Client
import smtplib

ACCOUNT_SID = "AC110ef33aa51eadd1574d1f437d94a8ac"
AUTH_TOKEN = "5ae2b360c5918a646970219d09c83eb4"

USERNAME = "dimimeto@gmail.com"
PASSWORD = "hxvtupjyukgivhxx"

class NotificationManager:

    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_notificaton(self, body):

        message = self.client.messages.create(body=body, from_="+18508090310", to="+306976106764")

        print(message.sid)

    def send_emails(self, message, emails, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=USERNAME, password=PASSWORD)
            for email in emails:
                connection.sendmail(from_addr=USERNAME, to_addrs=email, msg=f"Subject:New low price flight!\n\n"
                                                                            f"{message}\n{google_flight_link}".encode("utf-8"))
