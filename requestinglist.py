import json
import random
import requests
import string

runescape_id_api = "https://secure.runescape.com/m=itemdb_rs/bestiary/beastData.json?beastid={}"
runescape_beast_name = "https://secure.runescape.com/m=itemdb_rs/bestiary/bestiaryNames.json?letter={}"

try:
    #Check if the monsters file already exists and loads it#
    inFile = open('monsters.json')
    #print("Found Monsters File")
    monsters_list = json.load(inFile)
    #print("Loaded {} monsters from file.".format(len(monsters_list)))

except:
    #If the programme cannot find the monsters file then get the information from api#
    print("No Monsters file found. Getting from API.")
    monsters_list = []

    for letter in string.ascii_uppercase:
        print("Getting Monsters for " + letter)
        response = requests.get(runescape_beast_name.format(letter))
        if response.status_code == 200:
            #print("Found {} monsters.".format(len(response.json())))
            monsters_list.extend(response.json())

print()
#print ("Got {} monsters total.".format(len(monsters_list)))

with open("monsters.json", "w") as monster_file:
    json.dump(monsters_list, monster_file)


def get_random_monster():
    random_monster = random.choice(monsters_list)
    if "dupe" in random_monster:
        #print("Multiple options available for {}. Choosing...".format(random_monster["dupe"]))
        random_monster = random.choice(random_monster["npcs"])
    return random_monster


def get_monster_stats(monster_id):
    response = requests.get(runescape_id_api.format(monster_id))
    if response.status_code == 200:
        return response.json()

def get_attack_options(monster_attacks):
    response = []
    if "magic" in monster_attacks and monster_attacks["magic"] > 0:
        response.append("magic")
    if "attack" in monster_attacks and monster_attacks["attack"] > 0:
        response.append("attack")
    if "ranged" in monster_attacks and monster_attacks["ranged"] > 0:
        response.append("ranged")
    return response


def run():
    your_attack_options = []
    while len(your_attack_options) == 0:
        your_monster = get_random_monster()
        #print(your_monster)
        your_monster_stats = get_monster_stats(your_monster['value'])
        your_attack_options = get_attack_options(your_monster_stats)
    your_life_points = your_monster_stats["lifepoints"]

    #print(your_attack_options)


    print('You were given {}'.format(your_monster['label']) + " it has {} lifepoints".format(your_life_points))
    #print("Monsters Stats {}".format(your_monster_stats))

    opponent_attack_options = []
    while len(opponent_attack_options) == 0:
        opponent_monster = get_random_monster()
        # print(opponent_monster)
        opponent_monster_stats = get_monster_stats(opponent_monster['value'])
        opponent_attack_options = get_attack_options(opponent_monster_stats)
    opponent_life_points = opponent_monster_stats["lifepoints"]
    # print(opponent_attack_options)

    print('Your opponent was given {}'.format(opponent_monster['label']) + " it has {} lifepoints".format(
        opponent_life_points))

    while your_life_points > 0 and opponent_life_points > 0:
        stat_choice = input('Which attack do you want to use? ' + ", ".join(your_attack_options) + ": ")
        opponent_attack_choice = random.choice(opponent_attack_options)
        print('The opponent chose to fight back with {}'.format(opponent_attack_choice))
        opponent_monster_stats = get_monster_stats(opponent_monster["value"])
        my_stat = your_monster_stats[stat_choice]
        opponent_stat = opponent_monster_stats[opponent_attack_choice]

        opponent_life_points -= my_stat
        print("You hit the enemy for {} points. It's new life points are {}".format(my_stat, opponent_life_points))

        your_life_points -= opponent_stat
        print("Enemy hits you for {} points. Your new life points are {} ".format(opponent_stat, your_life_points))

    if opponent_life_points <= 0:
        print("You have defeated a great enemy!")
    elif your_life_points <= 0:
        print("Your quest has come to an end cause you deaded")




    # if my_stat > opponent_stat:
    #     print('You Win!')
    # elif my_stat < opponent_stat:
    #     print('You Lose!')
    # else:
    #     print('Draw!')
run()
