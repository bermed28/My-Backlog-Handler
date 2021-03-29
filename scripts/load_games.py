import json  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

import os
from index.models import Game_Model, Image_Model

def run():
    with open('res/data.json', "r") as f:
        data = json.load(f)

    Game_Model.objects.all().delete()
    Image_Model.objects.all().delete()

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

        print("id", id)
        print("cover", cover)
        print("genres", genres)
        print("name", name)
        print("platforms", platforms)
        print("developers", developers)

        img, created = Image_Model.objects.get_or_create(img_id=id,img_url=cover)

        print(img)
        print(created)

        game = Game_Model(game_id=int(id), game_title=name,genres={"genres":genres},developers={"developers":developers},platforms ={"platforms":platforms}, img_id=img)
        game.save()


        # Format
    # email,role,course
    # jane@tsugi.org,I,Python
    # ed@tsugi.org,L,Python

    # for row in reader:
    #     print(row)
    #
    #     p, created = Person.objects.get_or_create(email=row[0])
    #     c, created = Course.objects.get_or_create(title=row[2])
    #
    #     r = Membership.LEARNER
    #     if row[1] == 'I':
    #         r = Membership.INSTRUCTOR
    #     m = Membership(role=r, person=p, course=c)
    #     m.save()

