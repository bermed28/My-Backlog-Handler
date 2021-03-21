import requests, rawgpy, json

from igdb.wrapper import IGDBWrapper
wrapper = IGDBWrapper("2zu4l0leu7rrc9i8ysagqlxuu5rh89", "r2raogtcmwho8ja4fv6b8si2h7u7ag")

# f in front mean I am putting a var in the string
def getCoverUrl(id):
    byte_array = json.loads(wrapper.api_request(
        'covers',
        f'fields url; where id = {id};'))
    for g in byte_array:
        for key in g:
            if key == "url":
                return "https:" + g[key]

def getPlatforms(id):
    byte_array = json.loads(wrapper.api_request(
        'platforms',
        f'fields name; where id = {id};'))
    for g in byte_array:
        for key in g:
            if key == "name":
                return g[key]


def getGenres(id):
    byte_array = json.loads(wrapper.api_request(
        'genres',
        f'fields name; where id = {id};'))
    for g in byte_array:
        for key in g:
            if key == "name":
                return g[key]

def getInvolvedCompanies(id):

    def getCompany(id):
        byte_array = json.loads(wrapper.api_request(
            'companies',
            f'fields name; where id = {id};'))
        for g in byte_array:
            for key in g:
                if key == "name":
                    return g[key]


    byte_array = json.loads(wrapper.api_request(
        'involved_companies',
        f'fields company; where id = {id};'))
    for g in byte_array:
        for key in g:
            if key == "company":
                return getCompany(g[key])

byte_array = wrapper.api_request(
             'games',
             'fields name,genres,platforms,cover,involved_companies; where platforms = 48; limit 15;'
             )
#platform = 48 is PS4
games = json.loads(byte_array)
#g is a dictionary
print("Started Game Extraction")
gamesExtracted = 0
for g in games:
    gamesExtracted += 1

    for key in g:
        if key == "cover":
            g[key] = getCoverUrl(g[key])
        elif key == "platforms":
            for i in range(len(g[key])):    #g[key] is an array of platforms ids
                g[key][i] = getPlatforms(g[key][i]) #g[key][i] is a platform in the array
        elif key == "genres":
            for i in range(len(g[key])):
                g[key][i] = getGenres(g[key][i])
        elif key == "involved_companies":
            for i in range(len(g[key])):
                g[key][i] = getInvolvedCompanies(g[key][i])


print(f"Games Extracted: {gamesExtracted}")

with open('data.json', 'w') as outfile:
    json.dump(games, outfile, indent=2)

print("Finished, check your data.json")



