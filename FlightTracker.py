from gpiozero import LED, LEDBarGraph, Button, OutputDevice
from time import sleep
from RPLCD.i2c import CharLCD 
import requests # Import the requests library to make HTTP requests to the OpenSky API

URL = "https://opensky-network.org/api/states/all" # OpenSky API URL
params = { # API parameters 
    "icao24": "",  # ICAO24 address of the aircraft (optional)
    "lamin": 51.19, "lomin": -1.17,
    "lamax": 51.48, "lomax": -0.77
}
r = requests.get(URL, params=params) # Make a GET request to the OpenSky API with the specified parameters
data = r.json() # Parse the JSON response from the OpenSky API
POLL_SECONDS = 5 # Polling interval in seconds

led = LED(17)
btn_a = Button(26) 


lcd = CharLCD(
    i2c_expander='PCF8574', 
    address=0x27, 
    port=1,
    cols=16,
    rows=2,
    charmap='A00',
    auto_linebreaks=True
)

def track_flights():
    print("Tracking flights...")
    print("---------------------------------")
    lcd.write_string("Tracking Flights")
    print("Polling OpenSky API every {} seconds...".format(POLL_SECONDS))
    if data['states'] is None:
        print("No flights found in the specified area.")
        lcd.clear()
        lcd.write_string("No flights found")
        sleep(5)
        return
    else:
        for flight in data['states']: # Loop through each flight in the 'states' list of the API response
            icao24 = flight[0] 
            callsign = flight[1]
            origin_country = flight[2]
            time_position = flight[3]
            last_contact = flight[4]
            longitude = flight[5]
            latitude = flight[6]
            baro_altitude = flight[7]
            on_ground = flight[8]
            velocity = flight[9]
            heading = flight[10]
            vertical_rate = flight[11]
            category = flight[12]

            print("Flight: {} | Callsign: {} | Country: {} | Altitude: {} | Velocity: {} | Category: {}".format ( 
                icao24, callsign, origin_country, baro_altitude, velocity, category))
            
            lcd.clear()
            lcd.write_string("CS: {}".format(callsign))
            lcd.cursor_pos = (1, 0)
            lcd.write_string("CON: {}".format(origin_country))
            sleep(5) # Wait for 5 seconds before polling the API again
            lcd.clear()
            lcd.write_string("PL: {}".format(icao24))
            lcd.cursor_pos = (1, 0)
            lcd.write_string("Cat: {}".format(category))
            sleep(5) # Wait for 5 seconds before polling the API again
            lcd.clear()
            lcd.write_string("Alt: {}".format(baro_altitude))
            lcd.cursor_pos = (1, 0)
            lcd.write_string("Vel: {}".format(velocity))
            sleep(POLL_SECONDS)

def main():
    print("Flight Tracker Initialized")
    print("---------------------------------")
    # Initialize the LCD display
    print("1: Press the button to start tracking flights.")
    while True:
        if btn_a.is_pressed:
            track_flights()
            print("Tracking flights...")

main()