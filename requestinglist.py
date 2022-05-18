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

#picks a monster from the list and if there are any dupes then it selects just one of them
def get_random_monster():
    random_monster = random.choice(monsters_list)
    if "dupe" in random_monster:
        #print("Multiple options available for {}. Choosing...".format(random_monster["dupe"]))
        random_monster = random.choice(random_monster["npcs"])
    return random_monster

#gets the monsters stats that we will use for attacking etc from the API
def get_monster_stats(monster_id):
    response = requests.get(runescape_id_api.format(monster_id))
    if response.status_code == 200:
        return response.json()


#check what attack options your character will have#
def get_attack_options(monster_attacks):
    response = []
    if "magic" in monster_attacks and monster_attacks["magic"] > 0:
        response.append("magic")
    if "attack" in monster_attacks and monster_attacks["attack"] > 0:
        response.append("attack")
    if "ranged" in monster_attacks and monster_attacks["ranged"] > 0:
        response.append("ranged")
    return response

#checking that the monster is capable of attacking, that it has more than 0 attack options#
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

#the actual game portion#

    while your_life_points > 0 and opponent_life_points > 0:

#for each attack option, gets the level of the attack and the number when printed#
        attack_damage_list = []
        for i in range(0, len(your_attack_options)):
            option = your_attack_options[i]
            value = your_monster_stats[option]
            attack_damage_list.append("{} ({})".format(option, value))
        stat_choice = input('Which attack do you want to use? ' + ", ".join(attack_damage_list) + ": ")
        if stat_choice not in your_attack_options:
            print("Please select from available options")
            continue

            #picking a random attack choice for opponent#
        opponent_attack_choice = random.choice(opponent_attack_options)
        print('The opponent chose to fight back with {}'.format(opponent_attack_choice))
        opponent_monster_stats = get_monster_stats(opponent_monster["value"])
        my_stat = your_monster_stats[stat_choice]
        opponent_stat = opponent_monster_stats[opponent_attack_choice]

        #keeping the starter lifepoints so damage percentage is based off of that and not a smaller amount#

        starter_opponent_life_points = opponent_monster_stats["lifepoints"]
        starter_your_life_points = your_monster_stats["lifepoints"]

        #picking a random percent of damage to do depending on your attack stat#

        my_percentage_damage = random.randint(0, my_stat)
        opponent_percentage_damage = random.randint(0, opponent_stat)

        #calculating and then subtractinng the percentage, + 10 so lower characters do some damage#

        my_damage_done = (starter_opponent_life_points * my_percentage_damage / 100) + 10
        my_damage_done = min(my_damage_done, opponent_life_points)
        opponent_damage_done = (starter_your_life_points * opponent_percentage_damage / 100) + 10
        opponent_damage_done = min(opponent_damage_done, your_life_points)

        #part of the game letting you know how powerful your hit was and the opponents#
        opponent_life_points -= my_damage_done
        print("You hit the enemy for {} points. It's new life points are {}".format(int(my_damage_done), int(opponent_life_points)))

        your_life_points -= opponent_damage_done
        print("Enemy hits you for {} points. Your new life points are {} ".format(int(opponent_damage_done), int(your_life_points)))
        #finished game, if
    if opponent_life_points <= 0:
        print("You have defeated a great enemy!")
    elif your_life_points <= 0:
        print("Your quest has come to an end cause you deaded")

run()
