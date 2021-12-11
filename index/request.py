import json, os
from threading import Thread
from igdb.wrapper import IGDBWrapper
global wrapper #Global variable to reference wrapper so it can be used across all methods and getters

"""
Use formatted strings in getters

def example(str):
    return f'my {str} is formatted'
    
def example2(str):
    return 'my {0} is formatted'.format(str)

"""


"""
GETTERS FOR API INFORMATION
Main Idea:
    -> Given a certain reference ID, make a query extracting the name, url, etc specifed and return it in a string
    -> Said string will contain the information to be replaced in the main hastable that stores our game infromation
    -> We have to iterate through the transfromed byte array given from the query lookign for the key that is not the id associated
        -> Hence why we have a double for loop in each getter
    -> Every 'for key in endpoint[0]:' has a in index ([0]) because the api gives us an array of one element,
       the hashtable containing the requested url, name or array of items
"""
def getCoverUrl(id):
    covers = json.loads(wrapper.api_request('covers', f'fields url; where id = {id};'))
    for key in covers[0]:
        if key == "url":
            return ("https:" + covers[0]['url']).replace('thumb',"1080p")

def getPlatforms(id):

    platforms = json.loads(wrapper.api_request('platforms', f'fields name; where id = {id};'))
    for key in platforms[0]:
        if key == "name":
            if platforms[0][key] == "Xbox Series":
                return platforms[0][key] + " X"
            return platforms[0][key]


def getGenres(id):
    genres = json.loads(wrapper.api_request('genres', f'fields name; where id = {id};'))
    for key in genres[0]:
        if key == "name":
            return genres[0][key]

def getInvolvedCompanies(id):

    # We do this internal method to avoid over complicating the code and adding an external method to only call it here
    def getCompany(id):
        company = json.loads(wrapper.api_request('companies', f'fields name; where id = {id};'))
        for key in company[0]:
            if key == "name":
                return company[0][key]

    involved_companies = json.loads(wrapper.api_request('involved_companies', f'fields company; where id = {id};'))
    for key in involved_companies[0]:
        if key == "company":
            # Internal method is called and it's value is returned in the main method
            return getCompany(involved_companies[0][key])

def getSummary(id, wrapper):
    # This method is intended to be used externally, import it where needed
    # summary is a list of dictionaries that follows a json format
    summary = json.loads(wrapper.api_request('games', f'fields storyline, summary; where id = {id};'))

    # Since some games do not have a storyline description, we can use the summary of the game
    # or just simply put that it has no summary yet

    # summary[0] is the first dictionary that is in the list of json formatted dictionaries
    if "storyline" in summary[0]:
        return summary[0]['storyline']  # summary[0][key], since summary[0] is a dictionary
    elif "summary" in summary[0]:
        return summary[0]['summary']
    else:
        return "This game has no summary yet"



"""""""""""""""""""""""""""""""""""""""""MAIN METHOD FOR EXTRACTING GAMES"""""""""""""""""""""""""""""""""""""""""""""""


def extractAPIGames(endpoint: str, query: str, fileNumber:int):

    byte_array = wrapper.api_request(endpoint, query) #Byte array that stores the infromation given from the API with a given endpoint & query
    games = json.loads(byte_array) #Convert the byte array into a json-like hashtable for easy extraction and iteration

    print(f"Started Game Extraction for file {fileNumber}")
    gamesExtracted = 0

    """
    MAIN FOR LOOP TO EXTRACT DATA FROM API
    
    Main Idea:
        -> games is a hashtable that is modeled in a json format to extract data from API
        -> Every value from the hashtable is an id reference to the actual information from the API
            -> We iterate through each key and extract that information rlated to that key using a getter
            -> Some keys have values that are arrays of ID's, so we have to call the getter for each individual ID in 
                the array for that key
    """
    for game in games:
        gamesExtracted += 1
        print(f"Games: {gamesExtracted} - File: {fileNumber}")
        for key in game:
            if key == "cover":
                game[key] = getCoverUrl(game[key])
            elif key == "platforms":
                #game[key] is an array of platforms ids
                for i in range(len(game[key])):
                    #game[key][i] is a platform ID in the array that must be extracted with the getter
                    game[key][i] = getPlatforms(game[key][i])
            elif key == "genres":
                for i in range(len(game[key])):
                    game[key][i] = getGenres(game[key][i])
            elif key == "involved_companies":
                for i in range(len(game[key])):
                    game[key][i] = getInvolvedCompanies(game[key][i])

    #We parse the hashtable information to a .json file we deliver as output using json.dump()
    with open(f'../res/data_{fileNumber}.json', 'w') as outfile:
        json.dump(games, outfile, indent=4)

    print(f"Games Extracted: {gamesExtracted}")
    print(f"Finished, check your data_{fileNumber}.json")


#Command to initialize game extraction every time this file is ran
if __name__ == "__main__":
    """
    TO FIX UNAUTHORIZED URL FROM API:
    
    SEND POST REQUEST TO THIS ENDPOINT:
    
    https://id.twitch.tv/oauth2/token?client_id=yourClientID&client_secret=yourClientSecret&grant_type=client_credentials
    """
    wrapper = IGDBWrapper("2zu4l0leu7rrc9i8ysagqlxuu5rh89", "9tvwz8wnwyjuqvn5h4nmq8k413wzwt")

    # extractAPIGames('games', 'fields name,genres,platforms,cover,involved_companies; where platforms=48 & category=0; limit 200;',1) #PS4
    # extractAPIGames('games', 'fields name,genres,platforms,cover,involved_companies; where platforms=49 & category=0; limit 200;', 2) #XB1
    # extractAPIGames('games', 'fields name,genres,platforms,cover,involved_companies; where platforms=130 & category=0; limit 200;',3) #Switch
    # extractAPIGames('games', 'fields name,genres,platforms,cover,involved_companies; where platforms=6 & category=0; limit 200;', 4) #PC
    # extractAPIGames('games', 'fields name,genres,platforms,cover,involved_companies; where platforms=167; limit 200;', 5) #PS5
    # extractAPIGames('games', 'fields name,genres,platforms,cover,involved_companies; where platforms=169; limit 200;',6) #XB Series X



