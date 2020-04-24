# Classes of game mechanics

import sys
import time
import threading
from collections import (Counter,
                         deque)
from src.data.constant import (HELP,
                               WELCOME_MESSAGE,
                               SeedCatalog)


class GameMechanics:

    def __init__(self):

        self.GAME_COMMANDS = {'help': self.help,
                              'quit': self.quit}
        self.playerMechanics = PlayerMechanics()
        self.inventoryMechancis = InventoryMechanics()
        self.rCommand = None            # user's raw command(s)
        self.command = None
        self.argument = None
        self.task = None                # function to execute
        self.isMultiple = bool          # multiple commands or single

        self._combine_commands()

    def help(self):

        print(HELP)

    def quit(self):

        print('Leaf closing. See you soon!')
        sys.exit()

    def start_game(self):

        self.welcome_message()
        while True:
            self.get_commands()
            self.parse_commands()
            self.get_command_type()
            self.process_commands()

    def welcome_message(self):

        print(WELCOME_MESSAGE)

    def get_commands(self):

        self.rCommand = str(input('\nLEAF > ')).split(maxsplit=1)

    def parse_commands(self):

        input_count = len(self.rCommand)
        if input_count == 1:
            self.isMultiple = False
            self.command = self.rCommand[0]
        else:
            self.command, self.argument = self.rCommand
            self.isMultiple = True

    # [] TODO: test next
    def get_command_type(self):

        self.task = self.GAME_COMMANDS.get(self.command,
                                           self._unrecognized_command)

    def process_commands(self):

        if self.isMultiple:
            self.task(self.argument)
        else:
            # [] TODO: test if the user add an extra argument which should not be
            self.task()

    def _combine_commands(self):

        self.GAME_COMMANDS.update(self.playerMechanics.PLAYER_COMMANDS)
        self.GAME_COMMANDS.update(self.inventoryMechancis.INVENTORY_COMMANDS)

    # GameMechanics command errors
    # [] TODO: create custom error types, i.e. GameCommandError, PlayerCommandError, etc.
    def _unrecognized_command(self):

        print(f'\'{self.command}\' is not a valid command.\nSee \'help\' command.')

    def _incomplete_command(self):

        print(f'{self.command} needs a value to work.')


class PlayerMechanics:

    def __init__(self):

        self.PLAYER_COMMANDS = {'till': self.till,
                                'plant': self.plant,
                                'check': self.check,
                                'harvest': self.harvest}

        self.playerInventoryMechanics = InventoryMechanics()
        self.plantGrowthMechanics = None
        self.growing_plants = deque()        # list of active and non-active threads

    def till(self):

        # [] TODO: add a mechanics that will prevent other commands from executing if this is not executed first
        print('tilling the soil...')
        time.sleep(5)
        print('soil tilled!')

    def plant(self, seed=None):

        if seed:
            print(f'plant: {self.playerInventoryMechanics.inventoryDeque=}')
            if seed in self.playerInventoryMechanics.inventoryDeque:
                # Seed information
                seed_details = SeedCatalog(seed)

                # [] TODO: deduct 1 seed to player's inventory
                # print(seed)
                self.playerInventoryMechanics.remove_item(seed)

                print(f'planting {seed}...')
                time.sleep(3)

                # start growing plant
                self.plantGrowthMechanics = GrowthMechanics(seed, duration=seed_details.duration)
                self.growing_plants.append(self.plantGrowthMechanics)
                self.plantGrowthMechanics.start()
                print(f'{seed} planted!')
            else:
                print(f'You don\'t have a \'{seed}\' in your inventory.')
        else:
            print('Incomplete command, should be plant [seed], i.e. plant tomato')

    def check(self):

        # [] TODO: display growth percentage of planted crop
        for index, plant in enumerate(self.growing_plants):
            print(index, plant.name, plant.is_alive())

    def harvest(self):

        # [] TODO: display harvestable (100% growth) crops
        # [] TODO: you can only harvest thread that completed its task
        if self.growing_plants:
            print(f'Harvesting \'{self.growing_plants.popleft().name}\'...')
            time.sleep(4)
            print('Done!')


class InventoryMechanics:

    def __init__(self):

        self.INVENTORY_COMMANDS = {'inventory': self.inventory,
                                   'add_item': self.add_item}

        # seed, duration (seconds)
        # self.seeds = {'tomato': 15,
        #               'lettuce': 16,
        #               'watermelon': 34}
        #
        # self.quantityCounter = Counter(self.seeds.keys())

        # self.inventoryDeque = deque(['tomato',
        #                              'lettuce',
        #                              'watermelon',
        #                              'tomato'])
        self.inventoryDeque = deque()
        self.inventoryCounter = Counter(self.inventoryDeque)

    def inventory(self):

        # print(f'{"Item":<16}{"Quantity":<16}{"Duration (seconds)"}')
        # for name, duration in self.seedsDeque:
        #     print(f'{name:<16}{self.quantityCounter[name]:<16}{duration}')

        # print(f'{"Item":<16}{"Quantity":<16}')
        # for item in set(self.inventoryDeque):
        #     print(f'{item:<16}{self.inventoryCounter[item]:<16}')

        # [] TODO: Logic error: you are still getting the original result after updating your inventory, why?
        print(f'inventory:\n{self.inventoryDeque=}\n{self.inventoryCounter=}')
        print(f'{len(self.inventoryDeque)=}')

    def add_item(self, item):

        # [] TODO: implement adding new item(s) to inventory
        self.inventoryDeque.append(item)

        # update inventoryCounter
        self.inventoryCounter = Counter(self.inventoryDeque)

    def remove_item(self, item):

        # [] TODO: implement removing item(s) to inventory
        # print(item)
        # print(self.inventoryDeque.remove(item))
        self.inventoryDeque.remove(item)

        # update inventoryCounter
        self.inventoryCounter = Counter(self.inventoryDeque)

        print(f'remove_item: {self.inventoryDeque=}')


class GrowthMechanics(threading.Thread):

    def __init__(self, seed, duration):

        super().__init__()
        self.name = seed
        self.duration = duration

    def run(self):

        time.sleep(self.duration)
