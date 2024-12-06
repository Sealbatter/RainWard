import requests
import pprint

url = "https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast"

response = requests.get(url)

pprint.pp(response.json())