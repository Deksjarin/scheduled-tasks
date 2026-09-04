import pandas as pd
import random
import smtplib
import os

from datetime import datetime
from zoneinfo import ZoneInfo
from email.message import EmailMessage


MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")


# Read birthday data from CSV
df = pd.read_csv("birthdays.csv")


# Get today's date in Budapest
now = datetime.now(ZoneInfo("Europe/Budapest"))
today = (now.month, now.day)


# Create dictionary:
# (month, day) -> person's complete row
birthday_dict = {
    (int(row.month), int(row.day)): row
    for index, row in df.iterrows()
}


# Check whether today is someone's birthday
if today in birthday_dict:

    person = birthday_dict[today]
    name = person["name"]
    email = person["email"]

    # Choose random birthday letter
    random_generator = random.randint(1, 3)

    with open(
        f"./letter_templates/letter_{random_generator}.txt",
        encoding="utf-8"
    ) as letter:
        letter_text = letter.read()
        letter_text = letter_text.replace("[NAME]", name)

    # Create email
    message = EmailMessage()
    message["Subject"] = "Boldog születésnapot!"
    message["From"] = MY_EMAIL
    message["To"] = email
    message.set_content(letter_text)

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.send_message(message)
