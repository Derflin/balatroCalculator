DEFAULT_SAVE_DIRECTORY = "saves/"

INDENT_SIZE = 4
INDENT = " " * INDENT_SIZE
SEPARATOR_SIZE = 40
SEPARATOR = "-" * SEPARATOR_SIZE

TARGETS = {
    "state": {
        "name": "State",
        "command_target": ["state", "st"]
    },
    "poker_hand": {
        "name": "Poker Hand",
        "command_target": ["poker_hand", "ph"]
    },
    "joker": {
        "name": "Joker",
        "command_target": ["joker", "j"]
    },
    "playing_card": {
        "name": "Playing Card",
        "command_target": ["playing_card", "pc"]
    }
}

STATE_TARGET = TARGETS["state"]["command_target"]
POKER_HAND_TARGET = TARGETS["poker_hand"]["command_target"]
JOKER_TARGET = TARGETS["joker"]["command_target"]
PLAYING_CARD_TARGET = TARGETS["playing_card"]["command_target"]

COMMANDS = {
    "show": {
        "desc": "Display information about current game state",
        "command_name": ["show", "sh"],
        "command_target": [None, TARGETS["state"]["name"], TARGETS["poker_hand"]["name"], TARGETS["joker"]["name"], TARGETS["playing_card"]["name"]],
        "command_args": []
    },
    "calc": {
        "desc": "Calculate expected result score based on current game state",
        "command_name": ["calc", "c"],
        "command_target": [None],
        "command_args": []
    },
    "select": {
        "desc": "Trigger card selection for a playing card in hand",
        "command_name": ["select", "sl"],
        "command_target": [None, TARGETS["playing_card"]["name"]],
        "command_args": [
            {
                "name": "index",
                "desc": "Index of owned playing card in hand",
                "required": True,
                "target": None
            }
        ]
    },
    "add": {
        "desc": "Modify current game state by adding new joker card or playing card to hand",
        "command_name": ["add", "a"],
        "command_target": [TARGETS["joker"]["name"], TARGETS["playing_card"]["name"]],
        "command_args": [
            {
                "name": "index",
                "desc": "Index of owned joker or playing card in hand",
                "required": False,
                "target": None
            },
            {
                "name": "id",
                "desc": "ID of a joker or playing card to be used as base for a joker or playing card",
                "required": True,
                "target": None
            },
            {
                "name": "edition_id",
                "desc": "ID of edition to be set for a joker",
                "required": False,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "level",
                "desc": "Joker level",
                "required": False,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "add_sell_value",
                "desc": "Joker additional sell value",
                "required": False,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "suit_id",
                "desc": "ID of suit to be set for a playing card",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "enhancment_id",
                "desc": "ID of enhancment to be set for a playing card",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "edition_id",
                "desc": "ID of edition to be set for a playing card",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "seal_id",
                "desc": "ID of seal to be set for a playing card",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "add_chip",
                "desc": "Playing card additional chips",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            }
        ]
    },
    "remove": {
        "desc": "Modify current game state by removing an existing joker card or playing card from hand",
        "command_name": ["remove", "r"],
        "command_target": [TARGETS["joker"]["name"], TARGETS["playing_card"]["name"]],
        "command_args": [
            {
                "name": "index",
                "desc": "Index of owned joker or playing card in hand",
                "required": True,
                "target": None
            }
        ]
    },
    "move": {
        "desc": "Modify current game state by changing position of an existing joker card or playing card in hand",
        "command_name": ["move", "m"],
        "command_target": [TARGETS["joker"]["name"], TARGETS["playing_card"]["name"]],
        "command_args": [
            {
                "name": "index1",
                "desc": "Index of owned joker or playing card in hand to be moved",
                "required": True,
                "target": None
            },
            {
                "name": "index2",
                "desc": "Index of a new position where to move owned joker or playing card in hand",
                "required": True,
                "target": None
            }
        ]
    },
    "swap": {
        "desc": "Modify current game state by swaping position of two existing joker cards or playing cards in hands",
        "command_name": ["swap", "sw"],
        "command_target": [TARGETS["joker"]["name"], TARGETS["playing_card"]["name"]],
        "command_args": [
            {
                "name": "index1",
                "desc": "Index of owned joker or playing card in hand to be swapped",
                "required": True,
                "target": None
            },
            {
                "name": "index2",
                "desc": "Index of owned joker or playing card in hand to be swapped",
                "required": True,
                "target": None
            }
        ]
    },
    "edit": {
        "desc": "Modify current game state by editing parameters of itself, poker hand, existing joker card or playing card in hand",
        "command_name": ["edit", "e"],
        "command_target": [TARGETS["state"]["name"], TARGETS["poker_hand"]["name"], TARGETS["joker"]["name"], TARGETS["playing_card"]["name"]],
        "command_args": [
            {
                "name": "skipped_blinds",
                "desc": "Skipped blinds in the current run",
                "required": False,
                "target": TARGETS["state"]["name"]
            },
            {
                "name": "dollar_count",
                "desc": "Owned dollars",
                "required": False,
                "target": TARGETS["state"]["name"]
            },
            {
                "name": "joker_count_max",
                "desc": "Max number of jokers",
                "required": False,
                "target": TARGETS["state"]["name"]
            },
            {
                "name": "card_deck_size",
                "desc": "Number of cards in the deck",
                "required": False,
                "target": TARGETS["state"]["name"]
            },
            {
                "name": "stone_card_deck_count",
                "desc": "Number of stone cards in the deck",
                "required": False,
                "target": TARGETS["state"]["name"]
            },
            {
                "name": "steel_card_deck_count",
                "desc": "Number of steel cards in the deck",
                "required": False,
                "target": TARGETS["state"]["name"]
            },
            {
                "name": "discard_remain",
                "desc": "Remaining discards",
                "required": False,
                "target": TARGETS["state"]["name"]
            },
            {
                "name": "card_deck_remain",
                "desc": "Remaining cards in the deck",
                "required": False,
                "target": TARGETS["state"]["name"]
            },
            {
                "name": "index",
                "desc": "Index of poker hand",
                "required": True,
                "target": TARGETS["poker_hand"]["name"]
            },
            {
                "name": "played_count",
                "desc": "Poker hand played count",
                "required": False,
                "target": TARGETS["poker_hand"]["name"]
            },
            {
                "name": "level",
                "desc": "Poker hand level",
                "required": False,
                "target": TARGETS["poker_hand"]["name"]
            },
            {
                "name": "index",
                "desc": "Index of owned joker",
                "required": True,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "edition_id",
                "desc": "ID of edition to be set for a joker",
                "required": False,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "level",
                "desc": "Joker level",
                "required": False,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "add_sell_value",
                "desc": "Joker additional sell value",
                "required": False,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "active",
                "desc": "Joker active status",
                "required": False,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "cond_card_suit",
                "desc": "ID of card suit to be set in joker conditions (applicable only to jokers with \"card_suit\" condition variety assigned to them)",
                "required": False,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "cond_card_rank",
                "desc": "ID of card rank to be set in joker conditions (applicable only to jokers with \"card_rank\" condition variety assigned to them)",
                "required": False,
                "target": TARGETS["joker"]["name"]
            },
            {
                "name": "index",
                "desc": "Index of owned playing card in hand",
                "required": True,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "suit_id",
                "desc": "ID of suit to be set for a playing card",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "enhancment_id",
                "desc": "ID of enhancment to be set for a playing card",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "edition_id",
                "desc": "ID of edition to be set for a playing card",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "seal_id",
                "desc": "ID of seal to be set for a playing card",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "add_chip",
                "desc": "Playing card additional chips",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            },
            {
                "name": "active",
                "desc": "Playing card active status",
                "required": False,
                "target": TARGETS["playing_card"]["name"]
            }
        ]
    },
    "save": {
        "desc": "Save game state to file",
        "command_name": ["save"],
        "command_target": [None],
        "command_args": [
            {
                "name": "file",
                "desc": F"Name of file to be created in \"{DEFAULT_SAVE_DIRECTORY}\" directory, to which the game state will be saved",
                "required": False,
                "target": None
            }
        ]
    },
    "load": {
        "desc": "Load game state from file",
        "command_name": ["load"],
        "command_target": [None],
        "command_args": [
            {
                "name": "file",
                "desc": F"Name of file located in \"{DEFAULT_SAVE_DIRECTORY}\" directory, from which the game state will be loaded",
                "required": True,
                "target": None
            }
        ]
    },
    "help": {
        "desc": "Display app manual",
        "command_name": ["help", "h"],
        "command_target": [None],
        "command_args": []
    },
    "quit": {
        "desc": "Close the app",
        "command_name": ["quit", "q"],
        "command_target": [None],
        "command_args": []
    }
}

COMMANDS["help"]["command_target"] += [key for key in COMMANDS.keys()]