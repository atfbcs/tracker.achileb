import cloudscraper
import json

# create a cloudscraper instance
scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
    },
)

# specify the target URL
url = "https://api.tracker.gg/api/v2/r6siege/standard/matches/ubi/achiIe.?sessionType=ranked"

# request the target website
response = scraper.get(url)

# get the response status code
print(f"The status code is {response.status_code}")

# print the content type to see the response format
print("Content-Type:", response.headers.get('Content-Type'))

# Check if the response is JSON and parse it
if response.headers.get('Content-Type') == 'application/json':
    data = response.json()  # Parse the JSON content
    print(json.dumps(data, indent=4))
else:
    # Print the actual response body if it's not JSON
    print("Response body:", response.text)
