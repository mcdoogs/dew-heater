import requests
import board
import digitalio
import adafruit_dht
import time
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
STATION = os.getenv("STATION")
USER_AGENT = os.getenv("USER_AGENT")

delay = 60
buffer = 7

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4)

# Set the pin leading to the transistor for the heating circuit
outpin = digitalio.DigitalInOut(board.D18)
outpin.direction = digitalio.Direction.OUTPUT


url = f"{BASE_URL}/stations/{STATION}/observations/latest"
headers = {'User-Agent': USER_AGENT}

def get_dewpoint():
    r = requests.get(url, headers=headers)
    observations = r.json()
    dewpoint = observations['properties']['dewpoint']['value']
    return dewpoint

while True:
    ct = datetime.datetime.now()
    print(f"Current time: {ct} / Current buffer: {buffer}")
    try:
        temperature_c = dhtDevice.temperature

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    dewpoint = get_dewpoint()
    print(f"Dewpoint is {dewpoint}, current temperature of dome is {temperature_c}")

    if (dewpoint + buffer) > temperature_c:
        print("Powering dew strip")
        outpin.value = True
    else:
        print("Not powering dew strip")
        outpin.value = False

    time.sleep(delay)

outpin.value = False