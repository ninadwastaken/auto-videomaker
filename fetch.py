"""
./fetch <url> <outFileName>

Outputs:
    - post.json
"""

import sys
import requests
import os

# post_link = sys.argv[1][:-1] + '.json'
headers = {'user-agent': 'MyAPI/0.0.1'}
post_link = "https://www.reddit.com/r/AskReddit/comments/18tki3r/what_is_the_most_overrated_travel_destination.json"
json_data = requests.get(post_link).json()
print(json_data)
