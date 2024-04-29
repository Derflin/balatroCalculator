from config import COMMANDS, TARGETS, STATE_TARGET, POKER_HAND_TARGET, JOKER_TARGET, PLAYING_CARD_TARGET, SEPARATOR_SIZE
from game.simulation import Simulation

class AppCommandLine:
    def __init__(self, simulation):
        self.sim = simulation

    def start(self):
        print("Welcome to calculator for Balatro")
        print("Please type \"h\" or \"help\" to check possible commands")
        self.printSeparator()

        # Prepare main app loop
        while True:
            user_input = input('Type command: ')
            self.printSeparator()

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

                status = True
                match command_name:
                    case "show" | "sh":
                        status = self.commandShow(command_target, command_args)
                    case "calc" | "c":
                        status = self.commandCalc(command_target, command_args)
                    case "select" | "sl":
                        status = self.commandSelect(command_target, command_args)
                    case "add" | "a":
                        status = self.commandAdd(command_target, command_args)
                    case "remove" | "r":
                        status = self.commandRemove(command_target, command_args)
                    case "move" | "m":
                        status = self.commandMove(command_target, command_args)
                    case "swap" | "sw":
                        status = self.commandSwap(command_target, command_args)
                    case "edit" | "e":
                        status = self.commandEdit(command_target, command_args)
                    case "save":
                        status = self.commandSave(command_target, command_args)
                    case "load":
                        status = self.commandLoad(command_target, command_args)
                    case "help" | "h":
                        status = self.commandHelp(command_target, command_args)
                    case "quit" | "q":
                        exit()
                    case _:
                        print(F"-> Couldn't find a command called \"{command_name}\"")
                        print("-> Please type \"h\" or \"help\" to check possible commands")
                        self.printSeparator()
                        status = False

                if not status:
                    break
                else:
                    self.printSeparator()

    def printSeparator(self):
        print("-" * SEPARATOR_SIZE)

    def commandHelp(self, command_target=None, command_args=None):
        if command_target is not None:
            found = False
            for command_details in COMMANDS.values():
                if command_target in command_details["command_name"]:
                    found = True

                    print(F'-> Desc: {command_details["desc"]}')
                    
                    required = "[REQUIRED]" if None not in command_details["command_target"] else "[OPTIONAL]"
                    print(F'-> {required} Command Targets: {"Not Supported" if len(command_details["command_target"]) == 0 else ""}')
                    for target_name in command_details["command_target"]:
                        if target_name is not None:
                            command_target_name = target_name if target_name is not None else "None" 
                            print(F'     -- {command_target_name}')
                    
                    print(F'-> Command Args: {"Not Supported" if len(command_details["command_args"]) == 0 else ""}')
                    for arg in command_details["command_args"]:
                        target = ("[" + arg["target"] + "]") if arg["target"] is not None else "[All]"
                        required = "[REQUIRED]" if arg["required"] else "[OPTIONAL]"
                        command_arg_name = "\"" + arg["name"] + "\""
                        print(F'     -- {target}{required} {command_arg_name} -> {arg["desc"]}')

                    break

            if not found:
                print(F"-> Couldn't find a command called \"{command_target}\"")
                print("-> Please type \"h\" or \"help\" to check possible commands")

        else:
            print("This app is meant to be used as a score calculator for game \"Balatro\"")
            print("---")
            print("-> Command structure: [command_name] [command_target] [command_args]")

            print("-> \"[command_name]\" is used to determine which command should be executed and can be one of the following:")
            for command_details in COMMANDS.values():
                command_name = " or ".join(["\"" + name + "\"" for name in command_details["command_name"]])
                print(F'     -- {command_name} -> {command_details["desc"]}')
            
            print("-> \"[command_target]\" is used to specify what game objects exactly should be affected by the command and these might be one of the following:")
            for target_details in TARGETS.values():
                command_target = " or ".join(["\"" + name + "\"" for name in target_details["command_target"]])
                print(F'     -- {command_target} -> {target_details["name"]}')
            
            print("-> \"[command_args]\" is used to specify additional parameters that can be passed along with the command")
            print("     -- Syntax for the additional command arguments is: \"-[arg_name]=[arg_value]\"")
            print("     -- If there is more than one additional argument passed, every additional argument should be seperated from previous one by blank space")
            
            print("---")
            print("You can also type \"help [command_name]\" in order to learn more about specific command and what [command_target] and [command_args] it supports")
        
        return True

    def commandShow(self, command_target=None, command_args=None):
        if command_target is None:
            status = self.sim.printState()
            print("-" * SEPARATOR_SIZE)
            status = self.sim.printPokerHands()
            print("-" * SEPARATOR_SIZE)
            status = self.sim.printJokers()
            print("-" * SEPARATOR_SIZE)
            status = self.sim.printHand()
        elif command_target in STATE_TARGET:
            status = self.sim.printState()
        elif command_target in POKER_HAND_TARGET:
            status = self.sim.printPokerHands()
        elif command_target in JOKER_TARGET:
            status = self.sim.printJokers()
        elif command_target in PLAYING_CARD_TARGET:
            status = self.sim.printHand()
        else:
            print("-> Stopped command processing")
            print("-> ERROR: Unsupported command target")
            return False
        
        return True

    def commandCalc(self, command_target=None, command_args=None):
        self.sim.printCalculatedScore()
        return True

    def commandSelect(self, command_target=None, command_args=None):
        index = None if "index" not in command_args else command_args["index"]
        if index is None:
            print("-> Stopped command processing")
            print("-> ERROR: Missing required information about \"index\"")
            return False

        status = True
        if command_target is None or command_target in PLAYING_CARD_TARGET:
            status = self.sim.triggerSelectPlayingCard(index)

        if not status:
            print("-> Issue occured while processing the command")
        
        return status

    def commandAdd(self, command_target=None, command_args=None):
        index = None if "index" not in command_args else command_args["index"]
        id = None if "id" not in command_args else command_args["id"]
        if id is None:
            print("-> Stopped command processing")
            print("-> ERROR: Missing required information about \"id\"")
            return False

        if command_target is None or command_target in JOKER_TARGET:
            edition_id = None if "edition_id" not in command_args else command_args["edition_id"]
            level = None if "level" not in command_args else command_args["level"]
            add_sell_value = None if "add_sell_value" not in command_args else command_args["add_sell_value"]

            self.sim.addJoker(id=id, index=index, edition_id=edition_id, level=level, add_sell_value=add_sell_value)

        elif command_target is None or command_target in PLAYING_CARD_TARGET:
            suit_id = None if "suit_id" not in command_args else command_args["suit_id"]
            enhancment_id = None if "enhancment_id" not in command_args else command_args["enhacment_id"]
            edition_id = None if "edition_id" not in command_args else command_args["edition_id"]
            seal_id = None if "seal_id" not in command_args else command_args["seal_id"]
            add_chip = None if "add_chip" not in command_args else command_args["add_chip"]

            self.sim.addPlayingCard(id=id, suit_id=suit_id, index=index, enhancment_id=enhancment_id, edition_id=edition_id, seal_id=seal_id, add_chip=add_chip)

        else:
            print("-> Stopped command processing")
            print("-> ERROR: Unsupported command target")
            return False
        
        return True

    def commandRemove(self, command_target=None, command_args=None):
        index = None if "index" not in command_args else command_args["index"]

        status = True
        if command_target in JOKER_TARGET:
            status = self.sim.removeJoker(index)
        elif command_target in PLAYING_CARD_TARGET:
            status = self.sim.removePlayingCard(index)
        else:
            print("-> Stopped command processing")
            print("-> ERROR: Unsupported command target")
            return False
        
        if not status:
            print("-> Issue occured while processing the command")

        return status

    def commandMove(self, command_target=None, command_args=None):
        index1 = None if "index1" not in command_args else command_args["index1"]
        index2 = None if "index2" not in command_args else command_args["index2"]
        if index1 is None or index2 is None:
            print("-> Stopped command processing")
            print("-> ERROR: Missing required information about \"index1\" or \"index2\"")
            return False

        status = True
        if command_target in JOKER_TARGET:
            status = self.sim.movePositionJoker(index1, index2)
        elif command_target in PLAYING_CARD_TARGET:
            status = self.sim.movePositionPlayingCard(index1, index2)
        else:
            print("-> Stopped command processing")
            print("-> ERROR: Unsupported command target")
            return False

        if not status:
            print("-> Issue occured while processing the command")

        return status

    def commandSwap(self, command_target=None, command_args=None):
        index1 = None if "index1" not in command_args else command_args["index1"]
        index2 = None if "index2" not in command_args else command_args["index2"]
        if index1 is None or index2 is None:
            print("-> Stopped command processing")
            print("-> ERROR: Missing required information about \"index1\" or \"index2\"")
            return False

        status = True
        if command_target in JOKER_TARGET:
            status = self.sim.swapPositionJoker(index1, index2)
        elif command_target in PLAYING_CARD_TARGET:
            status = self.sim.swapPositionPlayingCard(index1, index2)
        else:
            print("-> Stopped command processing")
            print("-> ERROR: Unsupported command target")
            return False

        if not status:
            print("-> Issue occured while processing the command")

        return status

    def commandEdit(self, command_target=None, command_args=None):
        index = None if "index" not in command_args else command_args["index"]
        if command_target not in STATE_TARGET and index is None:
            print("-> Stopped command processing")
            print("-> ERROR: Missing required information about \"index\"")
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
            
            self.sim.setState(
                skipped_blinds=skipped_blinds,
                dollar_count=dollar_count,
                joker_count_max=joker_count_max,
                card_deck_size=card_deck_size,
                stone_card_deck_count=stone_card_deck_count,
                steel_card_deck_count=steel_card_deck_count,
                discard_remain=discard_remain,
                card_deck_remain=card_deck_remain
            )

        elif command_target in POKER_HAND_TARGET:
            played_count = None if "played_count" not in command_args else command_args["played_count"]
            level = None if "level" not in command_args else command_args["level"]

            if status and played_count is not None:
                status = self.sim.setPokerHandPlayedCount(index, played_count)
            if status and level is not None:
                status = self.sim.setPokerHandLevel(index, level)

        elif command_target in JOKER_TARGET:
            edition_id = None if "edition_id" not in command_args else command_args["edition_id"]
            level = None if "level" not in command_args else command_args["level"]
            add_sell_value = None if "add_sell_value" not in command_args else command_args["add_sell_value"]
            active = None if "active" not in command_args else command_args["active"]

            if status and edition_id is not None:
                status = self.sim.setJokerEdition(index, edition_id)
            if status and level is not None:
                status = self.sim.setJokerLevel(index, level)
            if status and add_sell_value is not None:
                status = self.sim.setJokerAdditionalSellValue(index, level)
            if status and active is not None:
                status = self.sim.setJokerActive(index, active)

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

        else:
            print("-> Stopped command processing")
            print("-> ERROR: Unsupported command target")
            return False

        if not status:
            print("-> Issue occured while processing the command")

        return status

    def commandSave(self, command_target=None, command_args=None):
        #TODO
        print("-> Save: Not Implemented Yet")
        return True

    def commandLoad(self, command_taget=None, command_args=None):
        #TODO
        print("-> Load: Not Implemented Yet")
        return True


if __name__ == '__main__':
    sim = Simulation()
    app = AppCommandLine(sim)
    app.start()
