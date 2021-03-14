import requests, rawgpy, json, time


from requests.auth import HTTPBasicAuth
from igdb.wrapper import IGDBWrapper
from igdb.igdbapi_pb2 import GameResult

wrapper = IGDBWrapper("2zu4l0leu7rrc9i8ysagqlxuu5rh89", "r2raogtcmwho8ja4fv6b8si2h7u7ag")
byte_array = json.loads(wrapper.api_request('games', 'fields *; where id=142;'))

i=0
for g in byte_array:
    print(json.dumps(g,indent=2))
    i+=1

print(i)