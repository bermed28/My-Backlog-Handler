import requests


headers = {
    'User-Agent': 'StackOverflowers UPRM College Project'
}
search = input("Enter game name: ")
payload = {'search': search}
url = "https://api.rawg.io/api/games"
r = requests.get(url, headers=headers, params=payload)

print(r.text)