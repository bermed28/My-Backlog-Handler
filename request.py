import requests, rawgpy, json
from requests.auth import HTTPBasicAuth
from igdb.wrapper import IGDBWrapper
wrapper = IGDBWrapper("2zu4l0leu7rrc9i8ysagqlxuu5rh89", "r2raogtcmwho8ja4fv6b8si2h7u7ag")

'''With a wrapper instance already created'''
# JSON API request
# parse into JSON however you like...

# Protobuf API request
from igdb.igdbapi_pb2 import GameResult
byte_array = wrapper.api_request(
            'games', # Note the '.pb' suffix at the endpoint
            'fields name,category,platforms;where platforms = 48;limit 500;'
            )

games = json.loads(byte_array)
i=0
for g in games:
    print(json.dumps(g,indent=2))
    i+=1

print(i)
# games_message = GameResult()
# games_message.ParseFromString(byte_array) # Fills the protobuf message object with the response
# print(games_message)














# r = requests.post("https://id.twitch.tv/oauth2/token?client_id=2zu4l0leu7rrc9i8ysagqlxuu5rh89&client_secret=2ul2ra2mfjyioilxrbawoi0b5tpf0p&grant_type=client_credentials")
# print(r.text)
# headers = {
#     'Client-ID': "2zu4l0leu7rrc9i8ysagqlxuu5rh89",
#     'Authorization': "Bearer r2raogtcmwho8ja4fv6b8si2h7u7ag",
#
# }
# r = requests.post("https://api.igdb.com/v4/games", data=headers)
#
# # payload = {'cover': 'grand theft auto'}
# # url = "https://api.igdb.com/v4/games"
# #
# # r = requests.get(url, headers=headers)
#
# print(r.text)







# rawg = rawgpy.RAWG("User-Agent, My Backlog Handler, S.O. Studios")
# rawg.login("bermedDev@gmail.com", "Fer28nan")
# search = rawg.search("call-of-duty",num_results=100)
#
#
# gtaDict = {}
#
#
# for game in search:
#
#     game.populate()
#
#     p = game.platforms
#
#     for plat in p:
#             if "PC" not in plat.name and "Call of Duty" in game.name:
#                 if game.name not in gtaDict:
#                     gtaDict[game.name] = [plat.name]
#                 else:
#                     gtaDict[game.name] += [plat.name]


#
# for game, platforms in gtaDict.items():
#     print(game, "-", platforms)





