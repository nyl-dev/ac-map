import json
import re

# Read the JSON file
with open('input.json', 'r') as file:
    json_data = json.load(file)

# Initialize list to store extracted data
data_list = []

# Define regular expressions for extracting artist, timestamp, and institution
artist_pattern = re.compile(r'by @([^—\u00e2\u0080\u0094]+)(?: - | \u00e2\u0080\u0094 )')
timestamp_pattern = re.compile(r'(?:-|\u00e2\u0080\u0094) \s*(.+?)(?:\s+at @|$)')
institution_pattern = re.compile(r'at @([^—]+)')

# Iterate over each item
for item in json_data:
    # Check if 'media' key exists and if it's not empty
    if 'media' in item and item['media']:
        # Access the first element of the 'media' list
        media_item = item['media'][0]
        
        # Initialize dictionary to store data for this item
        item_data = {}

        # Check if 'media_metadata' and 'video_metadata' keys exist
        if 'media_metadata' in media_item and 'video_metadata' in media_item['media_metadata']:
            # Extract exif_data
            exif_data = media_item['media_metadata']['video_metadata'].get('exif_data', [])
            # Filter out null values and keep only latitude and longitude
            exif_trimmed = [{"latitude": data.get("latitude"), "longitude": data.get("longitude")} for data in exif_data if data.get("latitude") is not None and data.get("longitude") is not None]
            if exif_trimmed:
                item_data['exif_data'] = exif_trimmed
        
        # Check if 'title' key exists
        title = media_item.get('title')
        if title:
            # Extract artist
            artist_match = artist_pattern.search(title)
            if artist_match:
                artist = artist_match.group(1)
                item_data['artist'] = artist
                
            # Extract timestamp
            timestamp_match = timestamp_pattern.search(title)
            if timestamp_match:
                timestamp = timestamp_match.group(1).strip()
                item_data['timestamp'] = timestamp
                
            # Extract institution
            institution_match = institution_pattern.search(title)
            if institution_match:
                institution = institution_match.group(1).strip()
                item_data['institution'] = institution

        # Append item_data to data_list
        if item_data:
            data_list.append(item_data)

# Export extracted data to a single JSON file
with open('exported_data.json', 'w') as export_file:
    json.dump(data_list, export_file, indent=4)

print("Exif data and titles exported successfully to 'exported_data.json'.")