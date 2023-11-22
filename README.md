# rain-notifications

A small Python course exercise. It requests weather data from 
OpenWeatherMap.org and filters the response to find if it will
rain within the next twelve hours. If so, an email is sent.
Originally this was meant to send an SMS message, but I did not
want to provide payment information to Twilio for such a small
project.

- Some constant variables will need to be assigned for this code
to work.
- The sending email address must be set up to use an app password
which is less secure. It is recommended to set up a separate email
account for this.