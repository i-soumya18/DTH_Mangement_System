import requests
from api import value

api_key = value

def get_channel_data(channel_name):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&q={channel_name}&part=snippet,id&maxResults=1&type=channel"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx status codes)
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            channel_id = item['id']['channelId']
            channel_name = item['snippet']['channelTitle'] if 'snippet' in item else "Unknown"


            # Construct the search query URL using the channel name
            search_query = channel_name.replace(" ", "+")
            search_url = f"https://www.youtube.com/results?search_query={search_query}"

            return {
                "channel_id": channel_id,
                "channel_name": channel_name,
                "channel_url": search_url,
                "channel_price": 0  # You can set the price here or fetch it from another source
            }
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

    return None
