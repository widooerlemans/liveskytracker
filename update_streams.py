import urllib.request
import xml.etree.ElementTree as ET
import json

CHANNELS = {
    "NASA": "UCWN3xxrcMIrgO45xP_b404w",
    "GreenlandWest": "UCJmO-p1e1LhC0l_O6Gj0i3A",
    "GreenlandEast": "UC2001oB2aA13K3lWd815Kpg",
    "GreenlandNorth": "UCXf9kG3wP3V41905jG7N6iQ",
    "GreenlandSouth": "UCoN5rA02q0_9v7l715g_vXA"
}

stream_data = {}

for name, channel_id in CHANNELS.items():
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        req = urllib.request.Request(
            rss_url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            ns = {'yt': 'http://www.youtube.com/xml/schemas/2015', 'atom': 'http://www.w3.org/2005/Atom'}
            video_id = None
            for entry in root.findall('atom:entry', ns):
                vid_elem = entry.find('yt:videoId', ns)
                if vid_elem is not None:
                    video_id = vid_elem.text
                    break
            if video_id:
                stream_data[name] = video_id
    except Exception as e:
        print(f"Error fetching {name}: {e}")

with open('streams.json', 'w') as f:
    json.dump(stream_data, f, indent=4)

print("Successfully updated streams.json:", stream_data)
