import pandas as pd
import random
import smtplib
import datetime as dt
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")


data = {
    "name": ["Test", "Apa", "Anči"],
    "email": ["pythontestdejan@gmail.com","ikucsera@gmail.com", "akucsera27@gmail.com"],
    "year": ["2026", "2026", "2026"],
    "month": ["09", "09", "11"],
    "day": ["04", "05", "27"]
}

df = pd.DataFrame(data)
df.to_csv("birthdays.csv", mode="w", header=True, index=False)

now = dt.datetime.now()
today_month = now.month
today_day = now.day
today = (today_month, today_day)

birthday_dict = {(int(row.month), int(row.day)): row for (index, row) in df.iterrows()}

random_generator = random.randint(1,3)


if today in birthday_dict:
    person = birthday_dict.get(today)
    name = person["name"]
    with open(f"./letter_templates/letter_{random_generator}.txt") as letter:
        letter_text = letter.read()
        letter_text = letter_text.replace("[NAME]", name)
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=person["email"],
            msg=f"Subject: Boldog születésnapot\n\n{letter_text}",
        )
