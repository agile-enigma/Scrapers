#Import all needed libraries
import json, csv, requests, getopt, sys, re
from datetime import datetime

#Set variables
#Please enter your Google API key as apiKey
base = "https://www.googleapis.com/youtube/v3/search?"
snippet = "part=snippet"
apiKey = "[GOOGLE API KEY HERE NO BRACKETS]"
api_field = "&key=" + apiKey
order = "&order=date"
#channel_id = ""
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#construct API query URL
def construct_url():
    #apiKey = input('Please enter your Google API key: ')
    latitude = input('Please enter the latitude of your desired location: ')
    longitude = input('Please enter the longitude of your desired location: ')
    locationRadius = input('Please enter your desired radius in kilometers (number only): ')
    #maxResults = input('Please enter the maximum number of results desired: ')
    while True:
        global publishedAfter
        publishedAfter = input("Please enter the date at which scraping should begin\
(yyyy-mm-dd; time will be in UTC): ")
        if not re.match("\d\d\d\d-\d\d-\d\d", publishedAfter):
            print("Error: Date entered in incorrect format.")
        else:
            break

    while True:
        base_url = base + snippet + "&type=video" + "&location=" + latitude + "," + \
            longitude + "&locationRadius=" + locationRadius + "km" + api_field + \
            "&publishedAfter=" + publishedAfter + "T00:00:00Z"
        response = input('Would you like to query for a specific search term?(y/n): ')
        if response == 'y':
            searchTerm = input('Please enter your search term: ')
            global api_url
            api_url = base_url + "&q=" + searchTerm + order
            break
        if response == 'n':
            api_url = base_url + order
            break
        else:
            print('Response not valid')
            continue

#Set arguments
argumentList = sys.argv[1:]
options = "cjh"
long_options = ["csv", "json", "help"]
arguments, values = getopt.getopt(argumentList, options, long_options)

#Check for undeclared 'apiKey' variable and absence of option
if apiKey == "":
    print("No value entered for variable 'apiKey' in script code."); quit()
if len(sys.argv) <= 1:
    print('No option entered. Options:\n\t--help: display help menu;\n\t--csv: \
output data as .csv file;\n\t--json: output data as json file.')

#--csv: output data to .csv
for currentArgument, currentValue in arguments:
    if currentArgument in ('--csv'):
    #Construct API query
        construct_url()
    #Query API and convert JSON data to Python dictionary object
        api_response = requests.get(api_url)
        print('...acquiring data...')
        videos = json.loads(api_response.text)
    #Convert Python dictionary object into a .csv file
        with open("youtube_geo" + now + ".csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["publishedAt",
                                 "title",
                                 "description",
                                 "thumbnailurl",
                                 "channelTitle",
                                 "videoId",
                                 "videoURL"])
            has_another_page = True
            while has_another_page:
                if videos.get("items") is not None:
                    for video in videos.get("items"):
                        video_data_row  = [
                            video["snippet"]["publishedAt"],
                            video["snippet"]["title"],
                            video["snippet"]["description"],
                            video["snippet"]["thumbnails"]["default"]["url"],
                            video["snippet"]["channelTitle"],
                            video["id"]["videoId"],
                            'youtube.com/watch?v=' + video["id"]["videoId"]
                            ]
                        csv_writer.writerow(video_data_row)
                if "nextPageToken" in videos.keys():
                    next_page_url = api_url + '&pageToken=' + videos['nextPageToken']
                    next_page_posts = requests.get(next_page_url)
                    videos = json.loads(next_page_posts.text)
                else:
                    print("Done")
                    has_another_page = False

#--json: output data to .json
    elif currentArgument in ('--json'):
        construct_url()
    #Query API and convert output data to JSON file & write output to .json file
        api_response = requests.get(api_url)
        print('...acquiring data...')
        json_loads = json.loads(api_response.text)
        with open("youtube_geo" + now + ".json", "w") as json_file:
            json.dump(json_loads, json_file, indent=2, sort_keys=True)
            #json_file.write(api_response.text)
#Print help menu
    elif currentArgument in ('--help'):
        print('\nYouTube Geo queries the YouTube v3 Data API for geotagged video content. \
\n\nUsage: python3 youtube_geo.py [OPTION]\
\n\nOptions:\n\t--help: display this help menu\n\t--csv: output data as CSV file in reverse chronological order\
\n\t--json: output data as JSON file in reverse chronological order\n')
