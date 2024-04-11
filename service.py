import requests
import json

api_key = 'AIzaSyAVsEn2fmgOHxOth843XugWgOZMi7sMaQY'

def get_channel_data(channel_id):
    try:
        url = f"https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key={api_key}&part=snippet,statistics&fields=items(id,snippet,statistics)"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx status codes)
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            channel_data = data['items'][0]
            return channel_data
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    return None

# Example channel ID (replace this with the actual channel ID you want to fetch)
channel_id = "7lCDEYXw3mM"

# Call the function to get the channel data
channel_data = get_channel_data(channel_id)

# Check if the channel data is retrieved successfully
if channel_data:
    print("Channel data retrieved successfully:")
    print(channel_data)
else:
    print("Failed to fetch channel data. Channel may not exist or API request failed.")




'''def get_channel_data(channel_id):
    try:
        # Load channel data from JSON file
        with open('channel_data.json', 'r') as file:
            channel_data_list = json.load(file)

        # Find the channel data for the given channel ID
        for channel_data in channel_data_list:
            if channel_data['channel_id'] == channel_id:
                return channel_data
            print(channel_data)
    except FileNotFoundError:
        print("Channel data JSON file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None'''


