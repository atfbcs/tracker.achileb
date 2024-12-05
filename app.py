from flask import Flask, request, jsonify, render_template
import cloudscraper
import json
import random
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)


# List of User-Agent strings to rotate
USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17",
    "Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
    "Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16",
    "Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.6 Safari/600.7.12"
]

# Function to create the scraper with random User-Agent rotation
def get_scraper():
    # Random headers
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": random.choice(["en-US,en;q=0.9", "fr-FR,fr;q=0.9", "de-DE,de;q=0.9"]),
        "Accept-Encoding": random.choice(["gzip, deflate", "br", "gzip"]),
        "Referer": random.choice(["https://google.com", "https://example.com", "https://tracker.gg"]),
        "Connection": random.choice(["keep-alive", "close"]),
        "Accept": random.choice(["application/json", "text/html"]),
    }

    # Random cookies
    cookies = {
        "session_id": str(random.randint(1000000, 9999999)),  # Random session ID
        "tracking": str(random.random()),  # Random tracking value
    }

    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows"}
    )

    scraper.headers.update(headers)  # Set the selected User-Agent
    scraper.cookies.update(cookies)
    return scraper

# Endpoint to render index.html
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to fetch ranked data based on username and platform
@app.route('/getrankeddata')
def get_ranked_data():
    # Get the username and platform from query parameters
    username = request.args.get('username')
    platform = request.args.get('platform')

    # Log the username and platform to debug
    app.logger.info(f"Received request with username={username}, platform={platform}")

    # Check if username or platform is missing
    if not username or not platform:
        app.logger.error("Missing 'username' or 'platform' parameter")
        return jsonify({"error": "Missing 'username' or 'platform' parameter"}), 400

    # Initialize the scraper
    scraper = get_scraper()

    # Initialize the rank tracking dictionary
    rank_progression = {}

    # Start with the first page
    next_page = 1

    while True:
        # Build the URL for the current page
        if next_page == 1:
            url = f"https://api.tracker.gg/api/v2/r6siege/standard/matches/{platform}/{username}?sessionType=ranked"
        else:
            url = f"https://api.tracker.gg/api/v2/r6siege/standard/matches/{platform}/{username}?sessionType=ranked&next={next_page}"

        # Log the request URL for debugging
        app.logger.info(f"Requesting URL: {url}")

        # Request the data using cloudscraper
        response = scraper.get(url)

        # Check if the response is valid
        if response.status_code != 200:
            app.logger.error(f"Failed to fetch data: {response.status_code}")
            return jsonify({"error": "Failed to fetch data from Tracker API"}), 400

        data = response.json()
        matches = data.get('data', {}).get('matches', [])

        # If no matches are found, stop fetching
        if not matches:
            break

        # Process each match
        for match in matches:
            rank_points = match['segments'][0]['stats']['rankPoints']['displayValue']
            rank_name = match['segments'][0]['stats']['rankPoints']['metadata'].get('name', 'Unknown')

            # Skip if rankPoints is None or not a valid string
            if not rank_points:
                continue

            # Convert rankPoints to integer after removing commas
            rank_points_int = int(rank_points.replace(",", ""))

            # Store rank progression
            if rank_name not in rank_progression:
                rank_progression[rank_name] = {'games': 0, 'rp': 0}
            
            # Increment the game count and accumulate RP for that rank
            rank_progression[rank_name]['games'] += 1
            rank_progression[rank_name]['rp'] += rank_points_int

        # Move to the next page
        next_page += 1

    # Prepare the response data for graphing
    progression_data = []
    for rank, data in rank_progression.items():
        progression_data.append({
            "rank": rank,
            "games": data['games'],
            "average_rp": data['rp'] / data['games'] if data['games'] > 0 else 0,
        })

    return jsonify({"rank_progression": progression_data})

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
