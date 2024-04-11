import requests

api_key = 'AIzaSyAyKGLUMzqBQJEkkFofZyQRGc6_2w8T-Uc'

def get_channel_data(channel_id):
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx status codes)
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            channel_data = data['items'][0]['snippet']
            return channel_data
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    return None

# Example channel ID (replace this with the actual channel ID you want to fetch)
channel_id = "NarendraModi"

# Call the function to get the channel data
channel_data = get_channel_data(channel_id)

# Check if the channel data is retrieved successfully
if channel_data:
    print("Channel data retrieved successfully:")
    print(channel_data)
else:
    print("Failed to fetch channel data. Channel may not exist or API request failed.")
