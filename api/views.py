from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
import json
from pprint import pprint
from models import Player, PuzzleData
from django.core import serializers

# Receive incoming json
def handle_post(request):
    if request.method == "POST":
        #Loads json received from POST
        received_json_data = json.loads(request.body)

        #Check if we got player data
        if 'player' in received_json_data or received_json_data['player']['social_id'] is not None or received_json_data['player']['email'] is not None or received_json_data['player']['puzzle_data'] is not None:
            inputid = received_json_data['player']['social_id']

            #See if player data already exist in database
            if len(Player.objects.filter(social_id=inputid))<1:

                #New Player
                p = Player()
                p.email = received_json_data['player']['email']
                p.social_id = received_json_data['player']['social_id']
                p.name = received_json_data['player']['name']
                p.save()

                playerPuzzleData = received_json_data['player']['puzzle_data']

                #Create puzzle data
                for i in range(len(playerPuzzleData['puzzles'])):

                    pdata = PuzzleData()
                    pdata.puzzles = playerPuzzleData['puzzles'][i]
                    pdata.scores=playerPuzzleData['scores'][i]
                    pdata.stars=playerPuzzleData['stars'][i]
                    pdata.save()
                    p.puzzle_data.add(pdata)

                p.save()
                data = serializers.serialize("python", p.puzzle_data.all())
                data = [d['fields'] for d in data]
                data = json.dumps(data)
                data = {'player': data}
                data = {'message': data}
                
                return render(request, "update.html", data)
            else:

                #Not a new player so have to see if we need to update scores and stars
                #I'll assume that players have unique social ids
                p = Player.objects.get(social_id=received_json_data['player']['social_id'])

                inputplayerPuzzleData = received_json_data['player']['puzzle_data']

                mylevels = {}
                #Create a list of levels and data pairs
                for currentlevel in p.puzzle_data.all():
                    mylevels[currentlevel.puzzles]=currentlevel

                #Check through each puzzle and update if needed
                for i in range(len(inputplayerPuzzleData['puzzles'])):
                    findlevel = inputplayerPuzzleData['puzzles'][i]

                    if findlevel not in mylevels:
                        #New puzzle level to add to puzzle data

                        pdata = PuzzleData()
                        pdata.puzzles = inputplayerPuzzleData['puzzles'][i]
                        pdata.scores=inputplayerPuzzleData['scores'][i]
                        pdata.stars=inputplayerPuzzleData['stars'][i]
                        pdata.save()
                        p.puzzle_data.add(pdata)

                    else:
                        #Puzzle data already exists, check if scores or stars is greater value

                        storedlevel = mylevels[findlevel]
                        if inputplayerPuzzleData['scores'][i] > storedlevel.scores:
                            storedlevel.scores = inputplayerPuzzleData['scores'][i]
                        if inputplayerPuzzleData['stars'][i] > storedlevel.stars:
                            storedlevel.stars = inputplayerPuzzleData['stars'][i]
                        storedlevel.save()

                p.save()

                #serialize puzzle data and return player's data in JSON

                data = serializers.serialize("python", p.puzzle_data.all())
                data = [d['fields'] for d in data]
                data = json.dumps(data)
                data = {'player': data}
                data = {'message': data}

                return render(request, "update.html", data)

        else:
            mymessage = {'message':"Did not find player data in JSON or badly formed JSON"}
            return render(request, "summary.html", mymessage)

    else:
        #Was not post request
        mymessage = {'message':"Did not make a POST request"}
        return render(request, "summary.html", mymessage)