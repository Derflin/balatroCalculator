## Introduction

The project is about implementing score calculator for game called "Balatro" using Python. Its goal is to let user simulate different game states from the game, edit them and calculate score based on them. The app provides to the user functionality such as:
* Display information about current game state
* Add/Remove joker card or playing card to hand
* Edit parameters of game state, poker hand, existing joker card or playing card in hand
* Change position of an existing joker card or playing card in hand
* Trigger card selection for a playing card in hand
* Calculate expected result score based on current game state

Currently the project only support interaction through command line interface (CLI), but in the future I would like to also add a graphical user interface (GUI) to it. Apart from that, I also intend to add some other features to this project(some of which are also mentioned in the TODO section on the bottom of README), but since I am working on this project alone and only in my free time, I am not sure when I will be able to implement them.

## Requirements

I created this project using Python 3.10, so it should work with it. I didn't check it's compatibility with any Python version prior to it.

## Usage

The calculator app should be started by running Python script from "app.py" file, which contains the implementation for the main game loop and user interface.

App itself contains a "help" feature which should explain all the details regarding what's available for the user and how to use the app. 

## TODO

- [] Add print/input logger so that it would be easier to print separators | also fix the issue with status return, so that it only breaks execution when actual error occurs
- [] Add option to adjust joker condition varieties
- [] Refactor project - Breakdown long functions in files into smaller functions to improve code readability
- [] Implement save/load feature - maybe by implementing _repr__ functon in objects
- [] Implement condition_variety in jokers - display them in joker __str__ and add them to the "edit" command 
- [] Implement adding jokers/playing cards based on their names, rather than ID from configuration file
- [] Implement feature for optimizing joker/playing cards placement to maximize score 
- [] Add option to load game state based on state in actual game
- [] Add GUI