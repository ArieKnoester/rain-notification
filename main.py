import requests
import smtplib

LATITUDE: float = 0.0   # Your latitude
LONGITUDE: float = 0.0  # Your longitude
OWM_API_KEY = ""  # Need an openweathermap.org account to get a key.
SMTP_HOST = ""  # Ex. smtp.gmail.com
FROM_ADDR = ""
FROM_ADDR_APP_PASSWORD = ""
TO_ADDR = ""
ENDPOINT = "https://api.openweathermap.org/data/2.8/onecall"
PARAMETERS = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": OWM_API_KEY,
    "exclude": "current,minutely,daily,alerts"
}


# Example api call to OpenWeather. The OneCall 3.0 endpoint requires that you save
# a payment method before it is authorized for your account.
# I did not want to provide credit card info for a small exercise like this.
# The 2.5 and 2.8 versions appear to work for now (2023-11-21)
# Docs: https://openweathermap.org/api/one-call-api

# To find a latitude and longitude:
# https://www.latlong.net/

response = requests.get(ENDPOINT, params=PARAMETERS)
response.raise_for_status()
hourly_forecast_48_hours = response.json()['hourly']

# New list from the hourly_forecast_48_hours of the status_codes for the next 12 hours.
# Status codes are found at: https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
hourly_status_code_next_12 = [hour['weather'][0]['id'] for hour in hourly_forecast_48_hours[:12]]
print(hourly_status_code_next_12)

for status_code in hourly_status_code_next_12:
    if status_code < 600:
        # print("Bring an umbrella.")
        with smtplib.SMTP(SMTP_HOST) as connection:
            connection.starttls()
            connection.login(user=FROM_ADDR, password=FROM_ADDR_APP_PASSWORD)
            connection.sendmail(
                from_addr=FROM_ADDR,
                to_addrs=TO_ADDR,
                # 'To' line is needed in msg, else it will use 'to_addrs' above to populate bcc
                # which may cause the recipient's email server to mark it as spam. This may
                # not be the case if sending to a list of recipients. I have not tested it.
                msg=f"To: {TO_ADDR}\r\n"
                    "Subject: Rain Today.\r\n"
                    "Chance of rain in the next 12 hours. Bring an umbrella."
            )
        break
