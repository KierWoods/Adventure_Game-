# Text Adventure game with multiple choice.
# Good/evil counter could be added to inform which ending.
# Check Inventory at any time. 


# Import pyfiglet to convert text to ascii art. 
# Import cmd - cmd will allow the player to "play" the game.
# Import random for text choices so they don't all read the same boring sentence. 
import pyfiglet
import cmd
import random
import sys

# Declare variables
DESC = 'desc'
FORWARD = 'forward'
BACK = 'back'
RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'
GROUND = 'ground'
SHOP = 'shop'
WORLD_INFO = 'world-info'
NAME = 'name'
ITEM_DESC = 'item_info'
TAKEABLE = 'takeable'
EDIBLE = 'edible'
USER_CHOICE_WORDS = 'user_choice_words'
USEABLE = 'use'
JESTER = 'jester'
UNLOCK = 'unlock'
TALKABLE = 'talkable'

# Track location and inventory
location = 'Unknown Locale' # Game starts here.
inventory = []
display_exit = True

class adventureGameControls(cmd.Cmd):

    # Method where player enter an input that is not recognised.
    def default(self, arg):
        print("You cannot do that Adventurer!\n To request 'help', Simply type help.")

    # Move forward.
    def do_forward(self, arg):
        movement("forward")

    # Move back
    def do_back(self, arg):
        movement("back")

    # Move left
    def do_left(self, arg):
        movement("left")

    # Move right. 
    def do_right(self, arg):
        movement("right")

    # Climb up
    def do_climbup(self, arg):
        movement("up")

    # Climb down
    def do_climbdown(self, arg):
        movement("down")

    # Interact with jester.
    # After inteaction add jester to ground. 
    def do_jester(self, arg):
       talkJester()
       

    # Show players inventory to user. 
    def do_inventory(self, arg):
        if len(inventory) == 0:
            print("Adventurer your inventory is empty... But you knew that didn't you!")
            return

        # Count items in inventory. 
        itemCount = {}
        for item in inventory:
            if item in itemCount.keys():
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # Print inventory to player.
        print("Inventory")
        for item in set(inventory):
            if itemCount[item] > 1:
                print(" % (%s)" % (item, itemCount[item]))
            else:
                print(" " + item)

    # Function for player to collect items and add to inventory. 
    def do_collect(self, arg):
        loot = arg.lower()

        if loot == "":
            print("Adventuter you must be clear in which you wish to collect.\n Type 'view' to view the items in this location.")
        
        not_loot = False

        # Remove item from room and add to inventory. If lootable. 
        for item in getALLMatchingItemDescription(loot, world_map[location][GROUND]):
            if item_list[item].get(TAKEABLE, True) == False:
                not_loot = True
                continue
            print("%s added to inventory." % (item_list[item][NAME]))

            # Remove item from room. 
            world_map[location][GROUND].remove(item)

            # Add item to inventory. 
            inventory.append(item)
            return
        if not_loot:
            print("%s is not considered loot Adventurer, Please don't be greedy!" % (loot))
        else:
            print("Adventurer There is nothing to take...")
    
    # When players drop unwanted items. 
    def do_drop(self, arg):
        discarded_loot = arg.lower()
        player_inventory = getDescription(inventory)

        # Only allow drop of item if it is actually in inventory
        if discarded_loot not in player_inventory:
            print(" Adventurer, You cannot drop an item you do not have!")
            return

        # Search inventory for item and remove from inventory. 
        item = getMatchingItemDescription(discarded_loot, inventory)
        if item != None:
            drop_list = ["The item drops to the floor!", "You toss the item from your inventory without care!", "With purpose you place the item gently on the ground, you look at it one last time you will never forget this item...", "You drop the item"]
            print(random.choice(drop_list))
            inventory.remove(item)

            # Add item to ground.
            world_map[location][GROUND].append(item)

    # When players use an item. 
    def do_use(self, arg):
        item_use = arg.lower()
        if item_use == "":
            print("Adventurer, what are you trying to use?\n Type 'inventory' to check your ... inventory.")
            return
        not_use = False

        for item in getMatchingItemDescription(item_use, inventory):
            if item_list[item].get[USEABLE, False] == False:
                not_use = True
                continue
            print("Adventurer, You use the %s" % (item_list[item][NAME]))
            inventory.remove(item)
            return
        if not_use:
            print("Adventurer, you cannot use that")
        else:
            print("Adventurer, to use an item you must have the item in your inventory!")
    
    # View objects in the location player is in, or item in inventory. 
    def do_view(self, arg):
        player_view = arg.lower()
        
        # If player wants to reprint location and options.
        if player_view == "":
            locationViewer(location)
            return
      
        # If player wants to view item in location. 
        item = getMatchingItemDescription(player_view, world_map[location][GROUND])
        if item != None:
            print("".join(item_list[item][ITEM_DESC]))
            return

        item = getMatchingItemDescription(player_view, inventory)
        if item != None:
            print("".join(item_list[item][ITEM_DESC]))
            return
        else:
            print("Adventurer, You cannot see what is not infront of you!")

    def do_unlock(self, arg):
        # Check keycard is in inventory.
        use_item = arg.lower()
        if use_item == "":
            print("Adventurer, what are you trying to use?\n Type 'inventory' to check your ... inventory.") 
            return
        for item in getALLMatchingItemDescription(use_item, inventory):
            if item_list['keycard'].get(USEABLE, False) == False:
                print("You use the Keycard")
                print("\nAdventurer you open the door, It looks to be a holding cell, Detained within is a Jester.")
                inventory.remove('keycard')
                del world_map['locked door']
                world_map.update({'Holding Cell':{DESC: 'It is a small sad cell, A jester stands in the corner',
                                                    BACK: 'Corridor #2',
                                                    JESTER: 'Talk with Jester'}})





    # Help commands for user to understand controls and inputs. 
    def help_collect(self):
        print("collect - Add item to inventory")
    
    def help_view(self):
        print("view - view item in inventory or on the ground")

    def help_use(self):
        print("use - use item in inventory")

    def help_drop(self):
        print("drop - discard item from inventory")

    def help_jester(self):
        print("jester - Talk with the jester")

    def help_forward(self):
        print("forward - move forward")

    def help_back(self):
        print("back - move back")

    def help_climbdown(self):
        print("climbdown - move to lower part of room")

    def help_climbup(self):
        print("climbup - move to up in the room, you cannot fly so must wait for the command")

    def help_jester(self):
        print("jester - Talk with NPC Jester")

    def help_inventory(self):
        print("inventory - view items in your inventory") 

    def help_left(self):
        print("left - move left") 

    def help_right(self):
        print("left - move right")              
    
    
# Function for game over and player dies or cannot continue. 
def gameOver():
    game_over = "Game Over!"
    gameover_ascii = pyfiglet.figlet_format(game_over, font='bulbhead')
    print(gameover_ascii)
    exit()
            

    

# Show location and potential moves for the player character. 
def locationViewer(locale):
    print(locale)
    print('=' * len(locale))
    print(''.join(world_map[locale][DESC]))

    # Show player all items. 
    if len(world_map[locale][GROUND]) > 0:
        for item in world_map[location][GROUND]:
            print(item_list[item][WORLD_INFO])

    # Show all possible movements.
    moves = []
    for direction in (FORWARD, BACK, LEFT, RIGHT, UP, DOWN, UNLOCK, JESTER):
        if direction in world_map[locale].keys():
            moves.append(direction.title())
    print()
    if display_exit:
        for direction in  (FORWARD, BACK, LEFT, RIGHT, UP, DOWN, UNLOCK, JESTER):
            if direction in world_map[location]:
                print("%s: %s" % (direction.title(), world_map[location][direction]))
    else:
        print("Moves Available: %s" % " ".join(moves))

def movement(direction):
    global location
    if direction in world_map[location]:
        print("You enter %s. " % direction)
        location = world_map[location][direction]
        locationViewer(location)
    else:
        print("Adventurer that is not possible!")
    while True:
        locationViewer(location)
        user_choice = input()
        if user_choice == "quit":
            break
        if user_choice in (FORWARD, BACK, LEFT, RIGHT, UP, DOWN):
            movement(user_choice)

def getDescription(items):
    items = list(set(items))
    item_descriptions = []
    for item in items:
        item_descriptions.extend(item_list[item][USER_CHOICE_WORDS])
    return list(set(item_descriptions))

def getFirstDescription(items):
    items = list(set(items))
    descriptions = []
    for item in items:
        descriptions.append(item_list[item][USER_CHOICE_WORDS][0])
    return list(set(descriptions))

def getMatchingItemDescription(description, items):
    items = list(set(items))
    for item in items:
        if description in item_list[item][USER_CHOICE_WORDS]:
            return item
    return None

def getALLMatchingItemDescription(description, items):
    items = list(set(items))
    matching_items = []
    for item in items:
        if description in item_list[item][USER_CHOICE_WORDS]:
            matching_items.append(item)
    return matching_items
 
def talkJester():
    print("...but... Jester is our friend?")
    kill_choice = int(input("""Are you sure you want to kill the jester..? She may provide helpful hints and tips?!
             1 - KILL JESTER
             2- Spare Jester"""))
    if kill_choice == 1:
        print("""You strangle the jester with your bare hands, she falls to the gorund lifeless and limp.
                    and for you adventurer, the game is over.""")
    elif kill_choice == 2:
        print("""JESTER: Sometimes to get inside a door, All you need to do is knock,
                Other times you will need this thing So the door you can unlock.""")
        print("\nYou take note of the riddle and wish you had in fact killed the jester.")
        gameOver()
        
# World Map stored in dictionary. Each location will be a dictionary.
# The keys will be the direction a player cant travel or an action for the player.

world_map = {
    'Unknown Locale': {
        DESC: ' You awaken within a strange dark room, the door is locked. There are no windows',
        FORWARD: 'Corridor #1',
        JESTER: 'Jester',
        GROUND: ['torch', 'blueprints', 'batteries', 'keycard']},
    'Corridor #1': {
        DESC: 'The corridor is dimly lit, lights flickering, where should you go?',
        LEFT: 'Corridor #2',
        RIGHT: 'Engine Room',
        BACK: 'Unknown Locale',
        GROUND: ['sign'],
        },
    'Engine Room': {
        DESC: 'You enter a room full of machines, you can barely hear yourself think! Gears crunch and buttons flash red and green. You wonder what is this powering? and where is the operator...',
        FORWARD: 'Corridor #1',
        DOWN: 'Engine',
        GROUND: ['keycard',"Engine Control Panel"]},
    'Corridor #2': {
        DESC: 'The corridor continues on, the flickering light seem to settle. Your eyes adjust...',
        FORWARD: 'Holding Cell',
        LEFT: 'Dark Corner',
        RIGHT: 'Corridor #3',
        BACK: 'Corridor #1',
        GROUND: [],
        },
    'Holding Cell': {
        DESC: '"Adventurer you open the door, It looks to be a holding cell, Detained within is a Jester."',
        BACK: 'Corridor #2',
        JESTER: 'Talk with Jester',
        GROUND: ['jester'],
        },
    }
item_list = {
    'keycard': {
        WORLD_INFO: 'A Keycard lays on the ground. I wonder what it can be used for.',
        NAME: 'Keycard',
        ITEM_DESC: 'Could this be used to open doors?',
        USEABLE: True,
        TAKEABLE: True, 
        USER_CHOICE_WORDS: ['keycard']},
    'blueprints': {
        WORLD_INFO: 'These appear to be plans for a building',
        NAME: 'blueprints',
        ITEM_DESC: 'MAKE THIS AN ASCII MAP? PERHAPS', # make this a map display(?)
        TAKEABLE: True,
        USER_CHOICE_WORDS: ['blueprints', 'map']},
    'Engine Control Panel': {
        WORLD_INFO: 'There is a control panel, Lights flicker, there are numerous buttons and switches',
        NAME: 'Engine Controls',
        ITEM_DESC: 'You wonder what the this is powering, where is the operator, you do not \
touch the controls as not to alert anyone to your prescence.',
        TAKEABLE: False,
        USER_CHOICE_WORDS: ['Engine', 'controls', 'panel', 'control panel','engine controls']},
    'torch': {
        WORLD_INFO: 'A torch sits on the ground.',
        NAME: 'a torch',
        ITEM_DESC: 'A torch, how enlightening',
        USER_CHOICE_WORDS: ['torch','light']},
    'batteries': {
        WORLD_INFO: 'A couple of batteries are on the ground',
        NAME: 'batteries',
        ITEM_DESC: 'Perhaps these could be used to power something',
        USER_CHOICE_WORDS: ['batteries', 'power']},
    'sign': {
        WORLD_INFO: 'A sign is present on the wall',
        NAME: 'sign',
        ITEM_DESC: '< Main Deck || Engine Room > ',
        USER_CHOICE_WORDS: ['sign']},
    'jester': {
        WORLD_INFO: 'Jingle the Jester stands in the corner, she is delighted to see a friendly face',
        NAME: 'jester',
        ITEM_DESC: 'Jingle the Jester, speaks in rythmn and ryhme, do you have the time?',
        TALKABLE: True,
        USER_CHOICE_WORDS: ['jester']},
    }




# Print title of game. 
title = "Adventure Game"
title_ascii = pyfiglet.figlet_format(title, font='bulbhead')
print(title_ascii)

print("Type 'help' for gameplay")

locationViewer(location)
adventureGameControls().cmdloop()


                              

      
