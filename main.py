import requests
import time
from datetime import datetime
from password import password
import smtplib

# define my local latitude an longitude
MY_LAT = 19.404430 # Your latitude
MY_LONG = -99.168870 # Your longitude
# function to detect if the iss is over my location
def is_iss_overhead():
    # call the api from the iss
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    # checking if there was any problem
    response.raise_for_status()
    # reading my json response
    data = response.json()
    # taken the latitude and longitude of the iss
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    #Your position is within +5 or -5 degrees of the ISS position.
    if  MY_LAT + 5 >= iss_latitude >= MY_LAT - 5 and MY_LONG + 5 >= iss_longitude >= MY_LONG - 5:
        return True
    else:
        return False

def is_night():
    # generating the parameters to send on to the api
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    # call the api to get the sunset and sunrise hour
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    # checking is was any problem
    response.raise_for_status()
    # reading my json file response
    data = response.json()
    # formating the response
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunrise -= 6
    if sunrise <= 0:
        sunrise += 24
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    sunset -= 6
    if sunset <= 0:
        sunset += 24
    # get the current time now
    time_now = datetime.now().hour
    print(time_now)
    # checking if it dark and i can see at this hour the space
    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False
while True:
    time.sleep(60)
    # check if the iss is over and is dark
    if is_iss_overhead() and is_night():
        my_email = "davidraskovskypython@gmail.com"
        to_addrs = "davidraskovskypython@yahoo.com"
        # the connection with the server with i am sending the mails
        with smtplib.SMTP("smtp.gmail.com") as connection:
            # the starttls is the security method to connection with encyptions
            # make the connection more secure
            connection.starttls()
            # Establish the user to connection and password
            connection.login(user=my_email, password=password)
            # writing the email and sending
            connection.sendmail(from_addr=my_email,
                                to_addrs=to_addrs,
                                msg=f"Subject:lOOK uP\n\nThe ISS is over you on the sky"
                                )
    else:
        print(f"ISS is over you: {is_iss_overhead()},and is dark now {is_night()}")




