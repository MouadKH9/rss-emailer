import feedparser
import sched
import time
from bs4 import BeautifulSoup
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "news@sustainiastocks.com"
receiver_email = "news@sustainiastocks.com"
smtp_server = "localhost"
smtp_port = 1025

sentArticles = []


def sendEmail(subject, body):
    print("Sending email with subject {}".format(subject))
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    body = MIMEText(body, "html")
    message.attach(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(sender_email, receiver_email, message.as_string())


def getData():
    dataFeed = feedparser.parse(
        "https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeEFpRXEMGSQ5SSFBXFERXEkBeXEUDGkRJXhddV1NSFw==")

    print("Received {} lines:".format(len(dataFeed)))
    for entry in dataFeed.entries:
        if entry.guid in sentArticles:
            continue
        sentArticles.append(entry.guid)
        url = entry.link
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.find('div', class_="bw-release-story")
        if body is None:
            continue
        sendEmail(entry.title, body)
    s.enter(5, 1, getData)


s = sched.scheduler(time.time, time.sleep)

s.enter(0, 1, getData)
s.run()
