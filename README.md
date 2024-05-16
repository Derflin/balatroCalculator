## Introduction

The project is about implementing score calculator for game called "Balatro" using Python. Its goal is to let user simulate different game states from the game, edit them and calculate score based on them. The app provides functionality such as:
* Display information about current game state
* Add/Remove joker card or playing card to hand
* Edit parameters of game state, poker hand, existing joker card or playing card in hand
* Change position of an existing joker card or playing card in hand
* Trigger card selection for a playing card in hand
* Calculate expected result score based on current game state
* Save and load game states from JSON file

Currently the project only supports interaction through command line interface (CLI), but in the future I would like to also add a graphical user interface (GUI) to it. Apart from that, I also intend to add some other features mentioned in the TODO section, but since I am working on this project alone and only in my free time, I am not sure when exactly I will be able to implement them.

## Usage

The calculator app should be started by running Python script from "app.py" file, which contains the implementation for the main app loop and user interface.

```bash
python app.py
```

App itself contains a "help" feature which should explain all the details regarding what's available for the user and how to use the app. 

```
Type command: help
----------------------------------------
This app is meant to be used as a score calculator for game "Balatro"
-----
Command structure: [command_name] [command_target] [command_args]
-> "[command_name]" is used to determine which command should be executed and can be one of the following:
    -- "show" or "sh" -> Display information about current game state
    -- "calc" or "c" -> Calculate expected result score based on current game state
    -- "select" or "sl" -> Trigger card selection for a playing card in hand
    -- "add" or "a" -> Modify current game state by adding new joker card or playing card to hand
    -- "remove" or "r" -> Modify current game state by removing an existing joker card or playing card from hand
    -- "move" or "m" -> Modify current game state by changing position of an existing joker card or playing card in hand
    -- "swap" or "sw" -> Modify current game state by swaping position of two existing joker cards or playing cards in hands
    -- "edit" or "e" -> Modify current game state by editing parameters of itself, poker hand, existing joker card or playing card in hand
    -- "save" -> Save game state to file
    -- "load" -> Load game state from file
    -- "help" or "h" -> Display app manual
    -- "quit" or "q" -> Close the app
-> "[command_target]" is used to specify what game objects exactly should be affected by the command and these might be one of the following:
    -- "state" or "st" -> State
    -- "poker_hand" or "ph" -> Poker Hand
    -- "joker" or "j" -> Joker
    -- "playing_card" or "pc" -> Playing Card
-> "[command_args]" is used to specify additional parameters that can be passed along with the command
    -- Syntax for the additional command arguments is: "-[arg_name]=[arg_value]"
    -- If there is more than one additional argument passed, every additional argument should be seperated from previous one by blank space
-----
You can also type "help [command_name]" in order to learn more about specific command and what [command_target] and [command_args] it supports
```

```
Type command: help add
----------------------------------------
-> Desc: Modify current game state by adding new joker card or playing card to hand
-> [REQUIRED] Command Targets:
    -- Joker (joker / j)
    -- Playing Card (playing_card / pc)
-> Command Args:
    -- [All][OPTIONAL] "index" -> Index of owned joker or playing card in hand
    -- [All][REQUIRED] "id" -> ID of a joker or playing card to be used as base for a joker or playing card
    -- [Joker][OPTIONAL] "edition_id" -> ID of edition to be set for a joker
    -- [Joker][OPTIONAL] "level" -> Joker level
    -- [Joker][OPTIONAL] "add_sell_value" -> Joker additional sell value
    -- [Playing Card][OPTIONAL] "suit_id" -> ID of suit to be set for a playing card
    -- [Playing Card][OPTIONAL] "enhancment_id" -> ID of enhancment to be set for a playing card
    -- [Playing Card][OPTIONAL] "edition_id" -> ID of edition to be set for a playing card
    -- [Playing Card][OPTIONAL] "seal_id" -> ID of seal to be set for a playing card
    -- [Playing Card][OPTIONAL] "add_chip" -> Playing card additional chips
---------------------------------------
```

## Example

```
Type command: show joker
----------------------------------------
    Jokers: None
----------------------------------------

Type command: add joker -id=100
----------------------------------------
Added new joker card
----------------------------------------

Type command: show joker
----------------------------------------
    Jokers:
    1) Walkie Talkie | Common
        -> Status: ACTIVE
        -> Effect Active: {'b_add_chip': 10, 'b_add_mult': 4}
        -> Effect Passive: None
        -> Condition: {'card_rank': [2, 8]}
        -> Sell Value: 2
        -> Edition: Base
----------------------------------------
```

## Requirements

I created this project using Python 3.10. I didn't check it's compatibility with any other Python version.

## License

Project is licensed under the [MIT](LICENSE) license.

## TODO

- [] Add type validation for args provided by user
- [] Add option to trigger more than one card at once
- [] Automation tests
- [] Adjust displayed card_rank or card_suit in conditions, to include names apart from IDs (maybe add some kind of tags to message sent to logger and then detect them in logger and replace "object_tag{ID}object_tag" with something like "object_type_name (ID: {id})")
- [] Implement adding jokers/playing cards or changing editions/seals/enhancments/suits/rank based on their names, rather than ID from configuration file
- [] Implement feature for optimizing joker/playing cards placement to maximize score 
- [] Add GUI
- [] Add support for consumables and vouchers