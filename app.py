import logging
import sys

from config import COMMANDS, TARGETS, STATE_TARGET, POKER_HAND_TARGET, JOKER_TARGET, PLAYING_CARD_TARGET, SEPARATOR, INDENT
from game.logger import AppFormatter
from game.simulation import Simulation

class AppCommandLine:
    def __init__(self):
        self.__setLoggers__()
        self.sim = Simulation()
        self.commands_map = [
            {"name": COMMANDS["show"]["command_name"], "func": lambda target, args: self.commandShow(target, args)},
            {"name": COMMANDS["calc"]["command_name"], "func": lambda target, args: self.commandCalc(target, args)},
            {"name": COMMANDS["select"]["command_name"], "func": lambda target, args: self.commandSelect(target, args)},
            {"name": COMMANDS["add"]["command_name"], "func": lambda target, args: self.commandAdd(target, args)},
            {"name": COMMANDS["remove"]["command_name"], "func": lambda target, args: self.commandRemove(target, args)},
            {"name": COMMANDS["move"]["command_name"], "func": lambda target, args: self.commandMove(target, args)},
            {"name": COMMANDS["swap"]["command_name"], "func": lambda target, args: self.commandSwap(target, args)},
            {"name": COMMANDS["edit"]["command_name"], "func": lambda target, args: self.commandEdit(target, args)},
            {"name": COMMANDS["save"]["command_name"], "func": lambda target, args: self.commandSave(target, args)},
            {"name": COMMANDS["load"]["command_name"], "func": lambda target, args: self.commandLoad(target, args)},
            {"name": COMMANDS["help"]["command_name"], "func": lambda target, args: self.commandHelp(target, args)},
            {"name": COMMANDS["quit"]["command_name"], "func": lambda target, args: self.commandQuit(target, args)},
        ]
        self.help_command_string = " or ".join(["\"" + name + "\"" for name in COMMANDS["help"]["command_name"]])

    def __setLoggers__(self):
        # Set logger for current object
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(AppFormatter('%(message)s'))
        self.logger.addHandler(stdout_handler)

        # Set logger for game objects
        game_logger = logging.getLogger("game")
        game_logger.setLevel(logging.INFO)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(AppFormatter('%(message)s'))
        game_logger.addHandler(stdout_handler)

    def start(self):
        self.logger.info("Welcome to calculator for Balatro")
        self.logger.info(F'Please type {self.help_command_string} to check possible commands')
        self.logger.info(SEPARATOR)

        # Prepare main app loop
        self.running = True
        while self.running:
            user_input = input('Type command: ')
            self.logger.info(SEPARATOR)

            commands = user_input.split(";")
            for command in commands:
                command_inputs = command.strip().split(" ")

                command_name = command_inputs.pop(0)
                command_target = None if len(command_inputs) == 0 or command_inputs[0][0] == "-" else command_inputs.pop(0)
                command_args = {}
                for elem in command_inputs:
                    args = elem.lstrip("-").split("=")
                    arg_name = args[0]
                    arg_value = int(args[1])
                    if "index" in arg_name:
                        arg_value -= 1
                    command_args[arg_name] = arg_value

                status = self.parseCommand(command_name, command_target, command_args)
                self.logger.info(SEPARATOR)

                if not status:
                    break

    def parseCommand(self, command_name, command_target, command_args):
        status = True
        found = False
        for command in self.commands_map:
            if command_name in command["name"]:
                found = True
                status = command["func"](command_target, command_args)
                break

        if not found:
            status = False
            self.logger.info(F"Couldn't find a command called \"{command_name}\"")
            self.logger.info(F'Please type {self.help_command_string} to check possible commands')

        return status and found

    def commandHelp(self, command_target=None, command_args=None):
        if command_target is not None:
            found = False
            for command_details in COMMANDS.values():
                if command_target in command_details["command_name"]:
                    found = True

                    self.logger.info(F'-> Desc: {command_details["desc"]}')
                    
                    required = "[REQUIRED]" if None not in command_details["command_target"] else "[OPTIONAL]"
                    self.logger.info(F'-> {required} Command Targets: {"Not Supported" if len(command_details["command_target"]) == 0 else ""}')
                    for target_name in command_details["command_target"]:
                        if target_name is not None:
                            command_target_name = target_name if target_name is not None else "None" 
                            self.logger.info(INDENT + F'-- {command_target_name}')
                    
                    self.logger.info(F'-> Command Args: {"Not Supported" if len(command_details["command_args"]) == 0 else ""}')
                    for arg in command_details["command_args"]:
                        target = ("[" + arg["target"] + "]") if arg["target"] is not None else "[All]"
                        required = "[REQUIRED]" if arg["required"] else "[OPTIONAL]"
                        command_arg_name = "\"" + arg["name"] + "\""
                        self.logger.info(INDENT + F'-- {target}{required} {command_arg_name} -> {arg["desc"]}')

                    break

            if not found:
                self.logger.info(F"Couldn't find a command called \"{command_target}\"")
                self.logger.info(F'Please type {self.help_command_string} to check possible commands')

        else:
            self.logger.info("This app is meant to be used as a score calculator for game \"Balatro\"")
            self.logger.info("-----")
            self.logger.info("Command structure: [command_name] [command_target] [command_args]")

            self.logger.info("-> \"[command_name]\" is used to determine which command should be executed and can be one of the following:")
            for command_details in COMMANDS.values():
                command_name = " or ".join(["\"" + name + "\"" for name in command_details["command_name"]])
                self.logger.info(INDENT + F'-- {command_name} -> {command_details["desc"]}')
            
            self.logger.info("-> \"[command_target]\" is used to specify what game objects exactly should be affected by the command and these might be one of the following:")
            for target_details in TARGETS.values():
                command_target = " or ".join(["\"" + name + "\"" for name in target_details["command_target"]])
                self.logger.info(INDENT + F'-- {command_target} -> {target_details["name"]}')
            
            self.logger.info("-> \"[command_args]\" is used to specify additional parameters that can be passed along with the command")
            self.logger.info(INDENT + "-- Syntax for the additional command arguments is: \"-[arg_name]=[arg_value]\"")
            self.logger.info(INDENT + "-- If there is more than one additional argument passed, every additional argument should be seperated from previous one by blank space")
            
            self.logger.info("-----")
            self.logger.info("You can also type \"help [command_name]\" in order to learn more about specific command and what [command_target] and [command_args] it supports")
        
        return True

    def commandShow(self, command_target=None, command_args=None):
        if command_target is None:
            self.sim.printState()
            self.logger.info(SEPARATOR)
            self.sim.printPokerHands()
            self.logger.info(SEPARATOR)
            self.sim.printJokers()
            self.logger.info(SEPARATOR)
            self.sim.printHand()
        elif command_target in STATE_TARGET:
            self.sim.printState()
        elif command_target in POKER_HAND_TARGET:
            self.sim.printPokerHands()
        elif command_target in JOKER_TARGET:
            self.sim.printJokers()
        elif command_target in PLAYING_CARD_TARGET:
            self.sim.printHand()
        else:
            self.logger.info("Stopped command processing")
            self.logger.error("Unsupported command target")
            return False
        
        return True

    def commandCalc(self, command_target=None, command_args=None):
        self.sim.printCalculatedScore()
        return True

    def commandSelect(self, command_target=None, command_args=None):
        index = None if "index" not in command_args else command_args["index"]
        if index is None:
            self.logger.info("Stopped command processing")
            self.logger.error("Missing required information about \"index\"")
            return False

        status = True
        if command_target is None or command_target in PLAYING_CARD_TARGET:
            status = self.sim.triggerSelectPlayingCard(index)

        if status:
            self.logger.info(F"Triggered card selection for card with index {index + 1}")
        else:
            self.logger.error("Issue occured while processing the command")
        
        return status

    def commandAdd(self, command_target=None, command_args=None):
        index = None if "index" not in command_args else command_args["index"]
        id = None if "id" not in command_args else command_args["id"]
        if id is None:
            self.logger.info("Stopped command processing")
            self.logger.error("Missing required information about \"id\"")
            return False

        status = True
        if command_target is None or command_target in JOKER_TARGET:
            edition_id = None if "edition_id" not in command_args else command_args["edition_id"]
            level = None if "level" not in command_args else command_args["level"]
            add_sell_value = None if "add_sell_value" not in command_args else command_args["add_sell_value"]

            status = self.sim.addJoker(id=id, index=index, edition_id=edition_id, level=level, add_sell_value=add_sell_value)
            if status:
                self.logger.info("Added new joker card")

        elif command_target is None or command_target in PLAYING_CARD_TARGET:
            suit_id = None if "suit_id" not in command_args else command_args["suit_id"]
            enhancment_id = None if "enhancment_id" not in command_args else command_args["enhacment_id"]
            edition_id = None if "edition_id" not in command_args else command_args["edition_id"]
            seal_id = None if "seal_id" not in command_args else command_args["seal_id"]
            add_chip = None if "add_chip" not in command_args else command_args["add_chip"]

            status = self.sim.addPlayingCard(id=id, suit_id=suit_id, index=index, enhancment_id=enhancment_id, edition_id=edition_id, seal_id=seal_id, add_chip=add_chip)
            if status:
                self.logger.info("Added new playing card to hand")

        else:
            self.logger.info("Stopped command processing")
            self.logger.error("Unsupported command target")
            return False
        
        if not status:
            self.logger.error("Issue occured while processing the command")
        
        return True

    def commandRemove(self, command_target=None, command_args=None):
        index = None if "index" not in command_args else command_args["index"]

        status = True
        if command_target in JOKER_TARGET:
            status = self.sim.removeJoker(index)
            if status:
                self.logger.info("Removed joker card")
        elif command_target in PLAYING_CARD_TARGET:
            status = self.sim.removePlayingCard(index)
            if status:
                self.logger.info("Removed playing card from hand")
        else:
            self.logger.info("Stopped command processing")
            self.logger.error("Unsupported command target")
            return False
        
        if not status:
            self.logger.error("Issue occured while processing the command")

        return status

    def commandMove(self, command_target=None, command_args=None):
        index1 = None if "index1" not in command_args else command_args["index1"]
        index2 = None if "index2" not in command_args else command_args["index2"]
        if index1 is None or index2 is None:
            self.logger.info("Stopped command processing")
            self.logger.error("Missing required information about \"index1\" or \"index2\"")
            return False

        status = True
        if command_target in JOKER_TARGET:
            status = self.sim.movePositionJoker(index1, index2)
            if status:
                self.logger.info(F"Changed joker card position from {index1} to {index2}")
        elif command_target in PLAYING_CARD_TARGET:
            status = self.sim.movePositionPlayingCard(index1, index2)
            if status:
                self.logger.info(F"Changed playing card position in hand from {index1} to {index2}")
        else:
            self.logger.info("Stopped command processing")
            self.logger.error("Unsupported command target")
            return False

        if not status:
            self.logger.error("Issue occured while processing the command")

        return status

    def commandSwap(self, command_target=None, command_args=None):
        index1 = None if "index1" not in command_args else command_args["index1"]
        index2 = None if "index2" not in command_args else command_args["index2"]
        if index1 is None or index2 is None:
            self.logger.info("Stopped command processing")
            self.logger.error("Missing required information about \"index1\" or \"index2\"")
            return False

        status = True
        if command_target in JOKER_TARGET:
            status = self.sim.swapPositionJoker(index1, index2)
            if status:
                self.logger.info(F"Swapped positions of joker cards from {index1} and {index2}")
        elif command_target in PLAYING_CARD_TARGET:
            status = self.sim.swapPositionPlayingCard(index1, index2)
            if status:
                self.logger.info(F"Swapped positions of playing cards in hand from {index1} and {index2}")
        else:
            self.logger.info("Stopped command processing")
            self.logger.error("Unsupported command target")
            return False

        if not status:
            self.logger.error("Issue occured while processing the command")

        return status

    def commandEdit(self, command_target=None, command_args=None):
        index = None if "index" not in command_args else command_args["index"]
        if command_target not in STATE_TARGET and index is None:
            self.logger.info("Stopped command processing")
            self.logger.error("Missing required information about \"index\"")
            return False

        status = True
        if command_target in STATE_TARGET:
            skipped_blinds = None if "skipped_blinds" not in command_args else command_args["skipped_blinds"]
            dollar_count = None if "dollar_count" not in command_args else command_args["dollar_count"]
            joker_count_max = None if "joker_count_max" not in command_args else command_args["joker_count_max"]
            card_deck_size = None if "card_deck_size" not in command_args else command_args["card_deck_size"]
            stone_card_deck_count = None if "stone_card_deck_count" not in command_args else command_args["stone_card_deck_count"]
            steel_card_deck_count = None if "steel_card_deck_count" not in command_args else command_args["steel_card_deck_count"]
            discard_remain = None if "discard_remain" not in command_args else command_args["discard_remain"]
            card_deck_remain = None if "card_deck_remain" not in command_args else command_args["card_deck_remain"]
            
            status = self.sim.setState(
                skipped_blinds=skipped_blinds,
                dollar_count=dollar_count,
                joker_count_max=joker_count_max,
                card_deck_size=card_deck_size,
                stone_card_deck_count=stone_card_deck_count,
                steel_card_deck_count=steel_card_deck_count,
                discard_remain=discard_remain,
                card_deck_remain=card_deck_remain
            )

            if status:
                self.logger.info("Updated game state")

        elif command_target in POKER_HAND_TARGET:
            played_count = None if "played_count" not in command_args else command_args["played_count"]
            level = None if "level" not in command_args else command_args["level"]

            if status and played_count is not None:
                status = self.sim.setPokerHandPlayedCount(index, played_count)
            if status and level is not None:
                status = self.sim.setPokerHandLevel(index, level)

            if status:
                self.logger.info("Updated poker hand")

        elif command_target in JOKER_TARGET:
            edition_id = None if "edition_id" not in command_args else command_args["edition_id"]
            level = None if "level" not in command_args else command_args["level"]
            add_sell_value = None if "add_sell_value" not in command_args else command_args["add_sell_value"]
            active = None if "active" not in command_args else command_args["active"]
            condition_variety = {}
            if "cond_card_suit" in command_args:
                condition_variety["card_suit"] = command_args["cond_card_suit"]
            if "cond_card_rank" in command_args:
                condition_variety["card_rank"] = command_args["cond_card_rank"]

            if status and edition_id is not None:
                status = self.sim.setJokerEdition(index, edition_id)
            if status and level is not None:
                status = self.sim.setJokerLevel(index, level)
            if status and add_sell_value is not None:
                status = self.sim.setJokerAdditionalSellValue(index, level)
            if status and active is not None:
                status = self.sim.setJokerActive(index, active)
            if status and len(condition_variety) > 0:
                status = self.sim.setJokerConditionVariety(index, condition_variety)

            if status:
                self.logger.info("Updated joker card")

        elif command_target in PLAYING_CARD_TARGET:
            suit_id = None if "suit_id" not in command_args else command_args["suit_id"]
            enhancment_id = None if "enhancment_id" not in command_args else command_args["enhancment_id"]
            edition_id = None if "edition_id" not in command_args else command_args["edition_id"]
            seal_id = None if "seal_id" not in command_args else command_args["seal_id"]
            add_chip = None if "add_chip" not in command_args else command_args["add_chip"]
            active = None if "active" not in command_args else command_args["active"]

            if status and suit_id is not None:
                status = self.sim.setPlayingCardSuit(index, suit_id)
            if status and enhancment_id is not None:
                status = self.sim.setPlayingCardEnhancment(index, enhancment_id)
            if status and edition_id is not None:
                status = self.sim.setPlayingCardEdition(index, edition_id)
            if status and seal_id is not None:
                status = self.sim.setPlayingCardSeal(index, seal_id)
            if status and add_chip is not None:
                status = self.sim.setPlayingCardAdditionalChip(index, add_chip)
            if status and active is not None:
                status = self.sim.setPlayingCardActive(index, active)

            if status:
                self.logger.info("Updated playing card")

        else:
            self.logger.info("Stopped command processing")
            self.logger.error("Unsupported command target")
            return False

        if not status:
            self.logger.error("Issue occured while processing the command")

        return status

    def commandSave(self, command_target=None, command_args=None):
        #TODO
        self.logger.info("-> Save: Not Implemented Yet")
        return True

    def commandLoad(self, command_taget=None, command_args=None):
        #TODO
        self.logger.info("-> Load: Not Implemented Yet")
        return True
    
    def commandQuit(self, command_target=None, command_args=None):
        self.logger.info("Closing the app...")
        self.running = False
        return False


if __name__ == '__main__':
    app = AppCommandLine()
    app.start()
