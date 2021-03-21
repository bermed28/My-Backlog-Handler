import requests, json
from igdb.wrapper import IGDBWrapper

wrapper = IGDBWrapper("2zu4l0leu7rrc9i8ysagqlxuu5rh89", "r2raogtcmwho8ja4fv6b8si2h7u7ag")

# query = input("Enter game name: ")
# byte_array = json.loads(wrapper.api_request(
#         'games',
#         f'fields name,cover,genres,artworks; search "{query}";')) #f in front mean I am putting a var in the string
#
# i=0
# for g in byte_array:
#     print(json.dumps(g,indent=2))
#     i+=1
#Query for getting covers------------------------------------

byte_array = json.loads(wrapper.api_request(
        'covers',
        'fields game,url,width, height; where id = 123355;')) #f in front mean I am putting a var in the string
i=0
for g in byte_array:
    print(json.dumps(g,indent=2))
    i+=1


#Query for getting artworks------------------------------------
# byte_array = json.loads(wrapper.api_request(
#         'artworks',
#         'fields game, url; where id = 7327;')) #f in front mean I am putting a var in the string
#
# i=0
# for g in byte_array:
#     print(json.dumps(g,indent=2))
#     i+=1
