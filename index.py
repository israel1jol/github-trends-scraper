from bs4 import BeautifulSoup
import requests
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

FROM = os.getenv("FROM")
TO = os.getenv("TO")
PASS = os.getenv("PASS")

now = datetime.datetime.now()

def main():
    body = "<h2>Github Trends for "+str(now)+" </h2><br><hr><br>"
    titles = []
    descrs = []
    links = []
    print("Scraping from github...")
    res = requests.get("https://www.github.com/trending")
    data = res.content
    soup = BeautifulSoup(data, "html.parser")
    for trend in soup.find_all("h1", {"class":"h3 lh-condensed"}):
        titles.append(trend.text.strip())
    for trend in soup.find_all("p", {"class":"col-9 color-fg-muted my-1 pr-4"}):
        descrs.append(trend.text.strip())
    
    print("Content Extracted")
    for i, title in enumerate(titles):
        link = "/".join(title.split(" /\n\n      "))
        body += "<article><a href=https://www.github.com/"+link+" target='_blank'>"+title+"</a>"+"<p>"+descrs[i]+"</p>"+"</article><br>"

    send_mail(body)

def send_mail(body : str):
    print("Sending mail")
    msg = MIMEMultipart()
    msg["Subject"] = "Github Trends for "+str(now)
    msg["From"] = FROM
    msg["To"] = TO
    msg.attach(MIMEText(body, "html"))

    transport = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    transport.set_debuglevel(0)
    transport.ehlo()
    transport.login(FROM, PASS)
    transport.sendmail(FROM, TO, msg.as_string())
    print("Mail Sent")
    transport.quit()


main()