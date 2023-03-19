# YouTube-Geo
YouTube Geo queries the YouTube Data v3 API for geotagged video content.

In order to use the script you will need to have obtained a Google API key at https://console.cloud.google.com/, enabled the YouTube Data v3 endpoint, and entered your API key in the script as the **apiKey** variable.


<img width="494" alt="Screenshot 2023-03-09 at 4 45 01 PM" src="https://user-images.githubusercontent.com/110642777/224043469-d20ab1be-0d75-458a-9291-954a4dc625d7.png">

Output data includes: timestamp, video title, video description, link to
video thumbnail, channel title, video ID, and video URL.

Usage: **python3 youtube_geo.py [OPTION]**

Options:

	--help: display this help menu
	
	--csv: output data as CSV file in reverse chronological order
	
	--json: output data as JSON file in reverse chronological order
