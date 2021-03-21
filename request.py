import requests, rawgpy, json

from igdb.wrapper import IGDBWrapper
wrapper = IGDBWrapper("2zu4l0leu7rrc9i8ysagqlxuu5rh89", "r2raogtcmwho8ja4fv6b8si2h7u7ag")

'''With a wrapper instance already created'''
# JSON API request
# parse into JSON however you like...
def getCoverUrl(id):
    byte_array = json.loads(wrapper.api_request(
        'covers',
        f'fields url; where id = {id};'))  # f in front mean I am putting a var in the string
    for g in byte_array:
        for key in g:
            if key == "url":
                return "https:" + g[key]

def getPlatforms(id):
    byte_array = json.loads(wrapper.api_request(
        'platforms',
        f'fields name; where id = {id};'))  # f in front mean I am putting a var in the string
    for g in byte_array:
        for key in g:
            if key == "name":
                return g[key]


def getGenres(id):
    byte_array = json.loads(wrapper.api_request(
        'genres',
        f'fields name; where id = {id};'))  # f in front mean I am putting a var in the string
    for g in byte_array:
        for key in g:
            if key == "name":
                return g[key]

def getCompanies(id):
    byte_array = json.loads(wrapper.api_request(
        'involved_companies',
        f'fields name; where id = {id};'))  # f in front mean I am putting a var in the string
    for g in byte_array:
        for key in g:
            if key == "name":
                return g[key]
# Protobuf API request
from igdb.igdbapi_pb2 import GameResult
byte_array = wrapper.api_request(
             'games', # Note the '.pb' suffix at the endpoint
             'fields name,genres,platforms,cover,involved_companies;where platforms = 48;limit 15;'
             )
#platform = 48 is PS4
games = json.loads(byte_array)
#g is a dictionary
for g in games:
    for key in g:
        if key == "cover":
            g[key] = getCoverUrl(g[key])
        if key == "platforms":
            for i in range(len(g[key])):    #g[key] is an array of platforms ids
                g[key][i] = getPlatforms(g[key][i]) #g[key][i] is a platform in the array
        if key == "genres":
            for i in range(len(g[key])):    #g[key] is an array of platforms ids
                g[key][i] = getGenres(g[key][i]) #g[key][i] is a platform in the array
        if key == "involved_companies":
            for i in range(len(g[key])):    #g[key] is an array of platforms ids
                g[key][i] = getCompanies(g[key][i]) #g[key][i] is a platform in the array



with open('data.json', 'w') as outfile:
    json.dump(games, outfile, indent=2)
