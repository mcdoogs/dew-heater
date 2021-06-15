import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
STATION = os.getenv("STATION")
USER_AGENT = os.getenv("USER_AGENT")

delay = 60

url = f"{BASE_URL}/stations/{STATION}/observations/latest"
headers = {'User-Agent': USER_AGENT}

while True:
	print("Querying NWS...")
	r = requests.get(url, headers=headers)
	observations = r.json()
	dewpoint = observations['properties']['dewpoint']['value']
	print(f"Current dewpoint is {dewpoint} degrees celsius")
	time.sleep(delay)