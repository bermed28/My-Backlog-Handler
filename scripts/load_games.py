import json  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

import os
from index.models import Game_Model, Image_Model

def run():
    fileNumber = 7
    while fileNumber <= 7:
        with open(f'res/data_{fileNumber}.json', "r") as f:
            data = json.load(f)

        for i in data:
            # print("-------------------------------------------------------------------------")
            id, cover, genres, name, platforms, developers = None, None, None, None, None, None

            if 'id' in i:
                id = i['id']
            if 'cover' in i:
                cover = i['cover']
            if 'genres' in i:
                genres = i["genres"]
            if 'name' in i:
                name = i['name']
            if 'platforms' in i:
                platforms = i['platforms']
            if 'involved_companies' in i:
                developers = i['involved_companies']
            print("Game Uploaded: ", name, "- Platforms:", platforms)
            img, created = Image_Model.objects.get_or_create(img_id=id,img_url=cover)
            game = Game_Model(game_id=int(id), game_title=name,genres={"genres":genres},developers={"developers":developers},platforms ={"platforms":platforms}, img_id=img)
            game.save()

        fileNumber+=1


