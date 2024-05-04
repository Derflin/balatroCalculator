import logging

from game.static import GAME_SCORING_ORDER, POKER_HANDS, FACE_CARD_IDS, STONE_CARD_ID, CARD_SUIT, STONE_CARD_SUIT, CARD_RANK, DEFAULT_DECK_SIZE, DEFAULT_JOKER_COUNT_MAX
from game.objects.pokerHand import PokerHand
from game.objects.playingCard import PlayingCard
from game.objects.jokerCard import JokerCard

SCIENTIFIC_NOTATION_MIN_VALUE = pow(10, 10)

class Simulation:
    def __init__(self):
        self.__setLoggers__()

        self.state = {
            "skipped_blinds": 0,
            "dollar_count": 0,
            "joker_count": 0,
            "joker_count_max": DEFAULT_JOKER_COUNT_MAX,
            "card_deck_size": DEFAULT_DECK_SIZE,
            "stone_card_deck_count": 0,
            "steel_card_deck_count": 0,
            "discard_remain": 0,
            "card_deck_remain": DEFAULT_DECK_SIZE
        }

        self.poker_hands = []
        for poker_hand_details in POKER_HANDS:
            hand_type = PokerHand(poker_hand_details["id"])
            self.poker_hands.append(hand_type)

        self.rules = {}

        self.hand = {"type_id": 0, "detected_types": [], "cards": [], "scoring_cards_indexes": []}

        self.jokers = []
        self.cur_joker_index = None

    def __setLoggers__(self):
        # Set logger for current object
        self.logger = logging.getLogger(__name__)

    def getState(self, key = None):
        if key is not None:
            if key in self.state:
                return self.state[key]
            else:
                return None
        else:
            return self.state

    def setState(self, skipped_blinds = None, dollar_count = None, joker_count = None, joker_count_max = None, card_deck_size = None, stone_card_deck_count = None, steel_card_deck_count = None, discard_remain = None, card_deck_remain = None):
        if skipped_blinds is not None:
            self.state["skipped_blinds"] = skipped_blinds
        if dollar_count is not None:
            self.state["dollar_count"] = dollar_count
        if joker_count is not None:
            self.state["joker_count"] = joker_count
        if joker_count_max is not None:
            self.state["joker_count_max"] = joker_count_max
        if card_deck_size is not None:
            self.state["card_deck_size"] = card_deck_size
        if stone_card_deck_count is not None:
            self.state["stone_card_deck_count"] = stone_card_deck_count
        if steel_card_deck_count is not None:
            self.state["steel_card_deck_count"] = steel_card_deck_count
        if discard_remain is not None:
            self.state["discard_remain"] = discard_remain
        if card_deck_remain is not None:
            self.state["card_deck_remain"] = card_deck_remain

        return True

    def getPokerHandLevel(self, index):
        if index >= 0 and index < len(self.poker_hands):
            return self.poker_hands[index].getLevel()
        return None

    def addPokerHandLevel(self, index, value = 1):
        if index >= 0 and index < len(self.poker_hands):
            self.poker_hands[index].addLevel(value)
            return True
        return False

    def setPokerHandLevel(self, index, value):
        if index >= 0 and index < len(self.poker_hands):
            self.poker_hands[index].setLevel(value)
            return True
        return False

    def getPokerHandPlayedCount(self, index):
        if index >= 0 and index < len(self.poker_hands):
            return self.poker_hands[index].getPlayedCount()
        return None

    def setPokerHandPlayedCount(self, index, value):
        if index >= 0 and index < len(self.poker_hands):
            self.poker_hands[index].setPlayedCount(value)
            return True
        return False

    def addPlayingCard(self, id, index = None, suit_id = 0, enhancment_id = 0, edition_id = 0, seal_id = 0, add_chip = 0):
        suit_id = 0 if suit_id is None else suit_id
        enhancment_id = 0 if enhancment_id is None else enhancment_id
        edition_id = 0 if edition_id is None else edition_id
        seal_id = 0 if seal_id is None else seal_id
        add_chip = 0 if add_chip is None else add_chip
        
        playing_card = {
            "selected": False,
            "card": PlayingCard(id, suit_id=suit_id, enhancment_id=enhancment_id, edition_id=edition_id, seal_id=seal_id, additional_chip=add_chip)
        }

        if index is None:
            self.hand["cards"].append(playing_card)
        else:
            self.hand["cards"].insert(index, playing_card)

        self.updateSelectedPokerHand()

    def removePlayingCard(self, index):
        if index >= 0 and index < len(self.hand["cards"]):
            removed_elem = self.hand["cards"].pop(index)
            self.updateSelectedPokerHand()
            return True
        return False

    def setPlayingCardSuit(self, index, suit_id):
        if index >= 0 and index < len(self.hand["cards"]):
            self.hand["cards"][index]["card"].setSuit(suit_id)
            return True
        return False

    def setPlayingCardEnhancment(self, index, enhancment_id):
        if index >= 0 and index < len(self.hand["cards"]):
            self.hand["cards"][index]["card"].setEnhancment(enhancment_id)
            self.updateSelectedPokerHand()
            return True
        return False

    def setPlayingCardEdition(self, index, edition_id):
        if index >= 0 and index < len(self.hand["cards"]):
            self.hand["cards"][index]["card"].setEdition(edition_id)
            return True
        return False

    def setPlayingCardSeal(self, index, seal_id):
        if index >= 0 and index < len(self.hand["cards"]):
            self.hand["cards"][index]["card"].setSeal(seal_id)
            return True
        return False

    def setPlayingCardAdditionalChip(self, index, value):
        if index >= 0 and index < len(self.hand["cards"]):
            self.hand["cards"][index]["card"].setAdditionalChip(value)
            return True
        return False
        
    def addPlayingCardAdditionalChip(self, index, value):
        if index >= 0 and index < len(self.hand["cards"]):
            self.hand["cards"][index]["card"].addAdditionalChip(value)
            return True
        else:
            return False

    def setPlayingCardActive(self, index, value):
        if index >= 0 and index < len(self.hand["cards"]):
            self.hand["cards"][index]["card"].setActive(value)
            self.updateSelectedPokerHand()
            return True
        return False

    def movePositionPlayingCard(self, old_index, new_index):
        if old_index >= 0 and old_index < len(self.hand["cards"]) and new_index >= 0 and new_index < len(self.hand["cards"]):
            if old_index < new_index:
                new_index -= 1
            playing_card = self.hand["cards"].pop(old_index)
            self.hand["cards"].insert(new_index, playing_card)
            self.updateSelectedPokerHand()
            return True
        return False

    def swapPositionPlayingCard(self, index1, index2):
        if index1 > 0 and index1 < len(self.hand["cards"]) and index2 > 0 and index2 < len(self.hand["cards"]):
            self.hand["cards"][index1], self.hand["cards"][index2] = self.hand["cards"][index2], self.hand["cards"][index1]
            self.updateSelectedPokerHand()
            return True
        return False

    def triggerSelectPlayingCard(self, index):
        if index >= 0 and index < len(self.hand["cards"]):
            self.hand["cards"][index]["selected"] = not self.hand["cards"][index]["selected"]
            self.updateSelectedPokerHand()
            return True
        return False

    def addJoker(self, id, index = None, edition_id = 0, level = 0, add_sell_value = 0):
        edition_id = 0 if edition_id is None else edition_id
        level = 0 if level is None else level
        add_sell_value = 0 if add_sell_value is None else add_sell_value
        
        joker = {
            "copied_index": None,    
            "card": JokerCard(id, edition_id=edition_id, level=level, additional_sell_value=add_sell_value)
        }

        if index is None:
            self.jokers.append(joker)
        else:
            self.jokers.insert(index, joker)

        self.setState(joker_count=len(self.jokers))
        self.updateJokerRules()
        self.updateSelectedPokerHand()

    def removeJoker(self, index):
        if index >= 0 and index < len(self.jokers):
            removed_elem = self.jokers.pop(index)

            self.setState(joker_count=len(self.jokers))
            self.updateJokerRules()
            self.updateSelectedPokerHand()
            return True
        return False

    def setJokerEdition(self, index, edition_id):
        if index >= 0 and index < len(self.jokers):
            self.jokers[index]["card"].setEdition(edition_id)
            return True
        return False

    def getJokerConditionVariety(self, index):
        if index >= 0 and index < len(self.jokers):
            return self.jokers[index]["card"].getConditionVariety()
        return None
    
    def setJokerConditionVariety(self, index, condition_variety):
        if index >= 0 and index < len(self.jokers):
            self.jokers[index]["card"].setConditionVariety(condition_variety)
            return True
        return False

    def setJokerLevel(self, index, value):
        if index >= 0 and index < len(self.jokers):
            self.jokers[index]["card"].setLevel(value)
            return True
        return False

    def addJokerLevel(self, index, value = 1):
        if index >= 0 and index < len(self.jokers):
            self.jokers[index]["card"].addLevel(value)
            return True
        return False

    def setJokerAdditionalSellValue(self, index, value):
        if index >= 0 and index < len(self.jokers):
            self.jokers[index]["card"].setAdditionalSellValue(value)
            return True
        return False

    def addJokerAdditionalSellValue(self, index, value):
        if index >= 0 and index < len(self.jokers):
            self.jokers[index]["card"].addAdditionalSellValue(value)
            return True
        return False

    def getJokerSellValueFromLeft(self, joker_stop_index=None):
        sell_value = 0
        stop_index = joker_stop_index if joker_stop_index is not None else self.cur_joker_index
        for joker_index in range(len(self.jokers)):
            if joker_index == stop_index:
                break
            sell_value += self.jokers[joker_index]["card"].getSellValue()
        return sell_value

    def setJokerActive(self, index, value):
        if index >= 0 and index < len(self.jokers):
            self.jokers[index]["card"].setActive(value)
            self.updateJokerRules()
            return True
        return False

    def movePositionJoker(self, old_index, new_index):
        if old_index >= 0 and old_index < len(self.jokers) and new_index >= 0 and new_index < len(self.jokers):
            if old_index < new_index:
                new_index -= 1
            joker = self.jokers.pop(old_index)
            self.jokers.insert(new_index, joker)
            self.updateJokerRules()
            return True
        return False

    def swapPositionJoker(self, index1, index2):
        if index1 > 0 and index1 < len(self.jokers) and index2 > 0 and index2 < len(self.jokers):
            self.jokers[index1], self.jokers[index2] = self.jokers[index2], self.jokers[index1]
            self.updateJokerRules()
            return True
        return False

    def updateJokerRules(self):
        self.rules = {}
        for index in range(len(self.jokers)):
            # Find joker index from which the rules should be read from 
            cur_index, found_compat = index, False
            joker = None
            while True:
                joker = self.jokers[cur_index]["card"]
                if joker.getActive():
                    if cur_index != index and not joker.getCopyCompat():
                        break

                    joker_effects = joker.getEffectsActive()
                    if "copy_mostleft" in joker_effects:
                        cur_index = 0
                    elif "copy_right" in joker_effects:
                        cur_index += 1
                    else:
                        found_compat = True
                        break

                    if cur_index >= len(self.jokers) or cur_index == index:
                        break
                else:
                    break

            # Save found joker index
            if found_compat and index != cur_index:
                self.jokers[cur_index]["copied_index"] = cur_index
            else:
                self.jokers[cur_index]["copied_index"] = None

            # Get passive effects from found joker index and save them in simulation rules
            if found_compat:
                joker_rules = joker.getEffectsPassive()
                for rule, value in joker_rules.items():
                    if isinstance(value, bool):
                        if rule in self.rules:
                            self.rules[rule] += 1
                        else:
                            self.rules[rule] = 1 
                    elif isinstance(value, float):
                        if rule in self.rules:
                            self.rules[rule].append(value)
                        else:
                            self.rules[rule] = [value]

    def getHandSelectedPlayingCardIndexes(self):
        selected_indexes = []

        for index in range(len(self.hand["cards"])):
            if self.hand["cards"][index]["selected"]:
                selected_indexes.append(index)

        return selected_indexes

    def updateSelectedPokerHand(self):
        # Gather data about currently selected cards
        selected_indexes = self.getHandSelectedPlayingCardIndexes()
        selected_cards = {"indexes": [], "ids": [], "suits": [], "wildcards": []}
        for selected_index in selected_indexes:
            selected_cards["indexes"].append(selected_index)
            selected_cards["ids"].append(self.hand["cards"][selected_index]["card"].getId())
            card_suit = self.hand["cards"][selected_index]["card"].getSuit()
            selected_cards["suits"].append(card_suit - 1 if "smeared_suits" in self.rules and card_suit % 2 != 0 else card_suit)
            selected_cards["wildcards"].append(self.hand["cards"][selected_index]["card"].getWildcardStatus())

        # Detect which poker hands are contained in currently selected cards and which cards are used for them
        poker_hands_count = len(self.poker_hands)
        detected_poker_hands = [False for index in range(poker_hands_count)]
        detected_selected_indexes = [[] for index in range(poker_hands_count)]
        for cur_index in range(poker_hands_count):
            poker_hand_type_base, poker_hand_type_combine = self.poker_hands[cur_index].getType()

            # Check if current poker hand is valid based on other poker hands that should be contained in it
            poker_hand_valid = True
            for type_id in poker_hand_type_combine:
                if not detected_poker_hands[type_id]:
                    poker_hand_valid = False
                    break

            # Check if current poker hand is valid based on the defined rules for the base poker hands
            if poker_hand_valid:
                detected_indexes = []
                if poker_hand_type_base:
                    poker_hand_short_code = self.poker_hands[cur_index].getShortCode()

                    detected, last_indexes = False, []
                    repeat_count, last_value = 0, None
                    match poker_hand_short_code:
                        case "high_card":
                            id_list = sorted(zip(selected_cards["indexes"], selected_cards["ids"]), key=lambda zipped_elem: zipped_elem[1], reverse=True)
                            
                            for card_index in range(len(id_list)):
                                # Detect stone card
                                if id_list[card_index][1] == STONE_CARD_ID:
                                    detected_indexes.append(id_list[card_index][0])
                                    continue
                                
                                # Detect poker hand
                                if not detected:
                                    last_indexes.append(id_list[card_index][0])
                                    detected = True

                            # High card is the base poker hand, so it will always be set as detected
                            detected = True

                        case "pair":
                            required_size = 2
                            id_list = sorted(zip(selected_cards["indexes"], selected_cards["ids"]), key=lambda zipped_elem: zipped_elem[1], reverse=True)
                            
                            for card_index in range(len(id_list)):
                                # Detect stone card
                                if id_list[card_index][1] == STONE_CARD_ID:
                                    detected_indexes.append(id_list[card_index][0])
                                    continue

                                # Detect poker hand
                                if not detected:
                                    if last_value is None or last_value != id_list[card_index][1]:
                                        last_value = id_list[card_index][1]
                                        last_indexes = [id_list[card_index][0]]
                                        repeat_count = 1
                                    else:
                                        last_indexes.append(id_list[card_index][0])
                                        repeat_count += 1

                                    if repeat_count >= required_size:
                                        detected = True

                        case "two_pair":
                            required_size = 2
                            id_list = sorted(zip(selected_cards["indexes"], selected_cards["ids"]), key=lambda zipped_elem: zipped_elem[1], reverse=True)
                            detected_count = 0
                            
                            for card_index in range(len(id_list)):
                                # Detect stone card
                                if id_list[card_index][1] == STONE_CARD_ID:
                                    detected_indexes.append(id_list[card_index][0])
                                    continue

                                # Detect poker hand
                                if not detected:
                                    if last_value is None or last_value != id_list[card_index][1]:
                                        last_value = id_list[card_index][1]
                                        repeat_count = 1
                                    else:
                                        repeat_count += 1
                                        if repeat_count == 2:
                                            detected_count += 1
                                            last_indexes.append(id_list[card_index-1][0])
                                            last_indexes.append(id_list[card_index][0])

                                    if detected_count >= required_size:
                                        detected = True

                        case "three_of_kind":
                            required_size = 3
                            id_list = sorted(zip(selected_cards["indexes"], selected_cards["ids"]), key=lambda zipped_elem: zipped_elem[1], reverse=True)
                            
                            for card_index in range(len(id_list)):
                                # Detect stone card
                                if id_list[card_index][1] == STONE_CARD_ID:
                                    detected_indexes.append(id_list[card_index][0])
                                    continue

                                # Detect poker hand
                                if not detected:
                                    if last_value is None or last_value != id_list[card_index][1]:
                                        last_value = id_list[card_index][1]
                                        last_indexes = [id_list[card_index][0]]
                                        repeat_count = 1
                                    else:
                                        last_indexes.append(id_list[card_index][0])
                                        repeat_count += 1

                                    if repeat_count >= required_size:
                                        detected = True

                        case "straight":
                            required_size = 4 if "four_flush_straight" in self.rules else 5
                            max_size = 5
                            id_offset = 1 if "straight_gap" in self.rules else 0
                            id_list = sorted(zip(selected_cards["indexes"], selected_cards["ids"]), key=lambda zipped_elem: zipped_elem[1], reverse=True)
                            
                            # Add id loop for aces
                            for card_index in range(len(id_list)):
                                if id_list[card_index][0] == len(CARD_RANK) - 1:
                                    id_list.append(id_list[card_index])
                                else:
                                    break

                            for card_index in range(len(id_list)):
                                # Detect stone card
                                if id_list[card_index][1] == STONE_CARD_ID:
                                    detected_indexes.append(id_list[card_index][0])
                                    continue

                                # Detect poker hand
                                if not detected:
                                    if last_value is None or last_value > id_list[card_index][1] + id_offset + 1:
                                        last_value = id_list[card_index][1]
                                        last_indexes = [id_list[card_index][0]]
                                        repeat_count = 1
                                    elif last_value != id_list[card_index][1]:
                                        last_value = id_list[card_index][1]
                                        last_indexes.append(id_list[card_index][0])
                                        repeat_count += 1

                                    if repeat_count >= required_size:
                                        detected = True
                                elif repeat_count < max_size:
                                    if last_value is None or last_value > id_list[card_index][1] + id_offset + 1:
                                        repeat_count = max_size
                                    elif last_value != id_list[card_index][1]:
                                        last_value = id_list[card_index][1]
                                        last_indexes.append(id_list[card_index][0])
                                        repeat_count += 1

                        case "flush":
                            required_size = 4 if "four_flush_straight" in self.rules else 5
                            max_size = 5
                            id_list = sorted(zip(selected_cards["indexes"], selected_cards["suits"], selected_cards["wildcards"]), key=lambda zipped_elem: zipped_elem[1], reverse=True)
                            wildcard_count = 0
                            for card_index in range(len(id_list)):
                                if id_list[card_index][2]:
                                    wildcard_count += 1 
                            
                            cur_suit_wildcard_count = 0
                            for card_index in range(len(id_list)):
                                # Detect stone card
                                if id_list[card_index][1] == STONE_CARD_SUIT:
                                    detected_indexes.append(id_list[card_index][0])
                                    continue

                                # Detect poker hand
                                if not detected:
                                    if last_value is None or last_value != id_list[card_index][1]:
                                        last_value = id_list[card_index][1]
                                        last_indexes = [id_list[card_index][0]]
                                        repeat_count = 1
                                        cur_suit_wildcard_count = wildcard_count
                                    else:
                                        last_indexes.append(id_list[card_index][0])
                                        repeat_count += 1

                                    if id_list[card_index][2]:
                                        cur_suit_wildcard_count -= 1 

                                    if repeat_count + cur_suit_wildcard_count >= required_size:
                                        detected = True
                                elif repeat_count < max_size:
                                    if id_list[card_index][1] == last_value or id_list[card_index][2]:
                                        last_indexes.append(id_list[card_index][0])
                                        repeat_count += 1

                        case "four_of_kind":
                            required_size = 4
                            id_list = sorted(zip(selected_cards["indexes"], selected_cards["ids"]), key=lambda zipped_elem: zipped_elem[1], reverse=True)
                            
                            for card_index in range(len(id_list)):
                                # Detect stone card
                                if id_list[card_index][1] == STONE_CARD_ID:
                                    detected_indexes.append(id_list[card_index][0])
                                    continue

                                # Detect poker hand
                                if not detected:
                                    if last_value is None or last_value != id_list[card_index][1]:
                                        last_value = id_list[card_index][1]
                                        last_indexes = [id_list[card_index][0]]
                                        repeat_count = 1
                                    else:
                                        last_indexes.append(id_list[card_index][0])
                                        repeat_count += 1

                                    if repeat_count == required_size:
                                        detected = True

                        case "five_of_kind":
                            required_size = 5
                            id_list = sorted(zip(selected_cards["indexes"], selected_cards["ids"]), key=lambda zipped_elem: zipped_elem[1], reverse=True)
                            
                            for card_index in range(len(id_list)):
                                # Detect stone card
                                if id_list[card_index][1] == STONE_CARD_ID:
                                    detected_indexes.append(id_list[card_index][0])
                                    continue

                                # Detect poker hand
                                if not detected:
                                    if last_value is None or last_value != id_list[card_index][1]:
                                        last_value = id_list[card_index][1]
                                        last_indexes = [id_list[card_index][0]]
                                        repeat_count = 1
                                    else:
                                        last_indexes.append(id_list[card_index][0])
                                        repeat_count += 1

                                    if repeat_count == required_size:
                                        detected = True

                    # Save which selected cards were used for the poker hand
                    if detected:
                        poker_hand_valid = True
                        for last_index in last_indexes:
                            detected_indexes.append(last_index)
                    else:
                        poker_hand_valid = False

                else:
                    # Save which selected cards were used for the poker hand
                    for type_id in poker_hand_type_combine:
                        for selected_index in detected_selected_indexes[type_id]:
                            if selected_index not in detected_indexes:
                                detected_indexes.append(selected_index)

            detected_poker_hands[cur_index] = poker_hand_valid
            detected_selected_indexes[cur_index] = detected_indexes

        # Check and save which poker hand is currently active
        self.hand["type_id"] = None
        self.hand["detected_types"] = detected_poker_hands
        for cur_index in reversed(range(poker_hands_count)):
            if detected_poker_hands[cur_index]:
                self.hand["type_id"] = cur_index
                self.hand["scoring_cards_indexes"] = detected_selected_indexes[cur_index]
                break

    def getHandPlayingCards(self, held_hand=False, played_hand=False, card_id=False, card_rank=False, card_suit=False):
        result = {}
        result_id, result_rank, result_suit = [], [], []
        
        if held_hand:
            for card_index in range(len(self.hand["cards"])):
                if not self.hand[card_index]["selected"]:
                    if card_id:
                        result_rank.append(self.hand["cards"][card_index]["card"].getId())
                    if card_rank:
                        result_rank.append(self.hand["cards"][card_index]["card"].getRank())
                    if card_suit:
                        result_suit.append(self.hand["cards"][card_index]["card"].getSuit())
        if played_hand:
            scoring_cards_indexes = self.getHandSelectedPlayingCardIndexes() if "every_played_card_counts" in self.rules else self.hand["scoring_cards_indexes"]
            for card_index in scoring_cards_indexes:
                if card_id:
                    result_rank.append(self.hand["cards"][card_index]["card"].getId())
                if card_rank:
                    result_rank.append(self.hand["cards"][card_index]["card"].getRank())
                if card_suit:
                    result_suit.append(self.hand["cards"][card_index]["card"].getSuit())
        
        if card_id:
            result["id"] = result_id
        if card_rank:
            result["rank"] = result_rank
        if card_suit:
            result["suit"] = result_suit
        
        return result

    def checkConditions(self, game_scoring_stage, condition, card_index = None, triggered_once=False):
        has_activate_probability = True if "activate_probability" in condition else False

        condition_passed = True
        match game_scoring_stage["short_code"]:
            case "played_hand":
                card = self.hand["cards"][card_index]["card"]

                if "card_suit" in condition:
                    card_suit = card.getSuit()
                    card_id = card.getId()
                    card_active = card.getActive()

                    if card_suit == STONE_CARD_SUIT:
                        if card_suit not in condition["card_suit"]:
                            condition_passed = False
                            return condition_passed, has_activate_probability
                    else:
                        card_wildcard = card.getWildcardStatus()
                        if card_wildcard:
                            if "removes_enhancements" in self.rules or ("face_cards_to_gold" in self.rules and ("all_face_cards" in self.rules or card_id in FACE_CARD_IDS)):
                                card_wildcard = False

                        if not card_wildcard:
                            if card_suit not in condition["card_suit"]:
                                #NOTE: not sure if debuffed card ignores passive effects from jokers
                                if "smeared_suits" in self.rules and "ignores_smeared_suits" not in condition and card_active:
                                    smeared_card_suit_id = card_suit - 1 if card_suit % 2 == 1 else card_suit + 1
                                    if smeared_card_suit_id not in condition["card_suit"]:
                                        condition_passed = False
                                        return condition_passed, has_activate_probability
                                else:
                                    condition_passed = False
                                    return condition_passed, has_activate_probability

                if "card_rank" in condition:
                    card_id = card.getId()

                    if card_id not in condition["card_rank"]:
                        condition_passed = False
                        return condition_passed, has_activate_probability

                if "trigger_once" in condition and triggered_once:
                    condition_passed = False
                    return condition_passed, has_activate_probability

                if "card_held" in condition:
                    condition_passed = False
                    return condition_passed, has_activate_probability

            case "held_hand":
                card = self.hand["cards"][card_index]["card"]

                if "card_rank" in condition:
                    card_id = card.getid()

                    if card_id not in condition["card_rank"]:
                        condition_passed = False
                        return condition_passed, has_activate_probability

                if "card_played" in condition:
                    condition_passed = False
                    return condition_passed, has_activate_probability

            case "owned_jokers":
                if "played_hand_contain_type" in condition:
                    if not self.hand["detected_types"][condition["played_hand_contain_type"]]:
                        condition_passed = False
                        return condition_passed, has_activate_probability

                if "played_hand_size_max" in condition:
                    if len(self.getHandSelectedPlayingCardIndexes()) > condition["played_hand_size_max"]:
                        condition_passed = False
                        return condition_passed, has_activate_probability

                if "played_hand_size_min" in condition:
                    if len(self.getHandSelectedPlayingCardIndexes()) < condition["played_hand_size_min"]:
                        condition_passed = False
                        return condition_passed, has_activate_probability

                if "played_hand_suit" in condition:
                    card_count_min = None if "played_hand_size_min" not in condition else condition["played_hand_size_min"]

                    # Gather data about cards
                    cards_indexes = self.getHandSelectedPlayingCardIndexes() if "every_played_card_counts" in self.rules else self.hand["scoring_cards_indexes"]
                    cards_suits = []
                    wildcard_count = 0
                    for card_index in cards_indexes:
                        card_wildcard = self.hand["cards"][card_index]["card"].getWildcardStatus()
                        if card_wildcard:
                            wildcard_count += 1
                        else:
                            card_suit = self.hand["cards"][card_index]["card"].getSuit()
                            card_suits = [card_suit]
                            if "smeared_suits" in self.rules and card_suit != STONE_CARD_SUIT:
                                card_suits.append(card_suit - 1 if card % 2 == 1 else card_suit + 1)
                            cards_suits.append(card_suits)
                        
                    # Check condition
                    checked_indexes = []
                    conditions_fulfilled = 0
                    for condition_suits in condition["played_hand_suit"]:
                        found = False
                        for card_index in range(len(cards_suits)):
                            if card_index not in checked_indexes:
                                for card_suit in cards_suits[card_index]:
                                    if card_suit in condition_suits:
                                        found = True
                                        conditions_fulfilled += 1
                                        if card_count_min is not None:
                                            checked_indexes.append(card_index)
                                        break
                                if found:
                                    break

                    if conditions_fulfilled + wildcard_count < len(condition["played_hand_suit"]):
                        condition_passed = False
                        return condition_passed, has_activate_probability

                if "played_hand_no_face_card" in condition:
                    scoring_cards_indexes = self.getHandSelectedPlayingCardIndexes() if "every_played_card_counts" in self.rules else self.hand["scoring_cards_indexes"]
                    for card_index in scoring_cards_indexes:
                        card_id = self.hand["cards"][card_index]["card"].getId()
                        if "all_face_cards" in self.rules or card_id in FACE_CARD_IDS:
                            condition_passed = False
                            return condition_passed, has_activate_probability

                if "held_hand_only_suit" in condition:
                    # Gather data about cards
                    selected_cards_indexes = self.getHandSelectedPlayingCardIndexes()
                    cards_indexes = [index for index in range(len(self.hand["cards"])) if index not in selected_cards_indexes]
                    cards_suits = []
                    wildcard_count = 0
                    for card_index in cards_indexes:
                        card_wildcard = self.hand["cards"][card_index]["card"].getWildcardStatus()
                        if card_wildcard:
                            wildcard_count += 1
                        else:
                            card_suit = self.hand["cards"][card_index]["card"].getSuit()
                            card_suits = [card_suit]
                            if "smeared_suits" in self.rules and card_suit != STONE_CARD_SUIT:
                                card_suits.append(card_suit - 1 if card % 2 == 1 else card_suit + 1)
                            cards_suits.append(card_suits)
                        
                    # Check condition
                    if wildcard_count > 0:
                        condition_passed = False
                        return condition_passed, has_activate_probability
                    else:
                        condition_only_suits = condition["held_hand_only_suit"]
                        for card_suits in cards_suits:
                            for card_suit in cards_suits[card_index]:
                                if card_suit not in condition_only_suits:
                                    condition_passed = False
                                    return condition_passed, has_activate_probability

                if "discard_remain_max" in condition:
                    if self.state["discard_remain"] > condition["discard_remain_max"]:
                        condition_passed = False
                        return condition_passed, has_activate_probability

                if "discard_remain_min" in condition:
                    if self.state["discard_remain"] < condition["discard_remain_min"]:
                        condition_passed = False
                        return condition_passed, has_activate_probability

        return condition_passed, has_activate_probability

    def getPokerHandActivePlayedCount(self):
        return self.poker_hands[self.hand["type_id"]].getPlayedCount()
    
    def getJokerCountMax(self):
        count = self.getState(key="joker_count_max")
        for joker_index in range(len(self.jokers)):
            edition_effects_passive = self.joker[joker_index]["card"].getEdition().getEffectsPassive()
            if "joker_add_max_count" in edition_effects_passive:
                count += edition_effects_passive["joker_add_max_count"]

        return count
    
    def getJokerCount(self, ignore_id=None):
        count = 0
        for joker_index in range(len(self.jokers)):
            joker_id = self.jokers[joker_index]["card"].getId()
            if ignore_id is None or ignore_id != joker_id:
                count += 1

        return count

    def checkConditionScoring(self, game_scoring_stage, card_effects_history, score_modifier, condition, card_index=None, activated_joker_indexes=None, joker_index=None):
        additional_trigger_count = 0
        condition_passed, has_activate_probability = True, False
        if condition is not None and len(condition) > 0:
            triggered_once = False if activated_joker_indexes is None or joker_index is None else activated_joker_indexes[joker_index]
            condition_passed, has_activate_probability = self.checkConditions(game_scoring_stage, condition, card_index=card_index, triggered_once=triggered_once)
        
        if condition_passed:
            score_modifier["activate_probability"] = has_activate_probability
            card_effects_history.append(score_modifier)
            if "add_trig" in score_modifier:
                additional_trigger_count += score_modifier["add_trig"]

            if activated_joker_indexes is not None and joker_index is not None:
                activated_joker_indexes[joker_index] = True

        return additional_trigger_count

    def calculateScore(self):
        # Get starting chip and mult based on currently active poker hand 
        cur_score = {
            "min_chip": 0,
            "max_chip": 0,
            "min_mult": 0,
            "max_mult": 0
        }
        cur_score["min_chip"], cur_score["min_mult"] = self.poker_hands[self.hand["type_id"]].getBaseScoreModifier()
        cur_score["max_chip"], cur_score["max_mult"] = cur_score["min_chip"], cur_score["min_mult"]

        effects_history = []
        for game_scoring_stage in GAME_SCORING_ORDER:
            # Check which joker should be included in each scoring stage
            active_joker_indexes = []
            for joker_index in range(len(self.jokers)):
                cur_joker_index = joker_index if self.jokers[joker_index]["copied_index"] is None else self.jokers[joker_index]["copied_index"]
                cur_joker_scoring_order = self.jokers[cur_joker_index]["card"].getScoringOrder()
                if cur_joker_scoring_order is not None and cur_joker_scoring_order == game_scoring_stage["id"] and self.jokers[cur_joker_index]["card"].getActive():
                    active_joker_indexes.append(cur_joker_index)
                else:
                    active_joker_indexes.append(None)
            activated_joker_indexes = [False for elem in active_joker_indexes]

            # Get score modifiers for each scoring stage
            match game_scoring_stage["short_code"]:
                case "played_hand":
                    scoring_cards_indexes = self.getHandSelectedPlayingCardIndexes() if "every_played_card_counts" in self.rules else self.hand["scoring_cards_indexes"]

                    for card_index in scoring_cards_indexes:
                        if self.hand["cards"][card_index]["card"].getActive():
                            additional_trigger_count = 0
                            card_effects_history = []

                            # Count card base effect
                            score_modifier, condition = self.hand["cards"][card_index]["card"].getBaseScoreModifier()
                            additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition, card_index=card_index)
                            
                            # Count card enhancment effect
                            card_id = self.hand["cards"][card_index]["card"].getId()
                            if not "removes_enhancements" in self.rules and not ("face_cards_to_gold" in self.rules and ("all_face_cards" in self.rules or card_id in FACE_CARD_IDS)):
                                score_modifier, condition = self.hand["cards"][card_index]["card"].getEnhancmentScoreModifier()
                                additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition, card_index=card_index)

                            # Count card seal effect
                            score_modifier, condition = self.hand["cards"][card_index]["card"].getSealScoreModifier()
                            additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition, card_index=card_index)

                            # Count joker effect on card
                            for joker_index in active_joker_indexes:
                                if joker_index is None:
                                    continue
                                self.cur_joker_index = joker_index
                                score_modifier, condition = self.jokers[joker_index]["card"].getBaseScoreModifier(simulation=self)
                                additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition, card_index=card_index, activated_joker_indexes=activated_joker_indexes, joker_index=joker_index)

                            # Count edition effect on card
                            score_modifier, condition = self.hand["cards"][card_index]["card"].getEditionScoreModifier()
                            additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition, card_index=card_index)

                            # Save card effects history in the general effects history along with trigger count information
                            effects_history.append({
                                "effect": [score_modifier for score_modifier in card_effects_history],
                                "trigger_count": 1 + additional_trigger_count
                            })

                case "held_hand":
                    selected_cards_indexes = self.getHandSelectedPlayingCardIndexes()
                    held_cards_indexes = [index for index in range(len(self.hand["cards"])) if index not in selected_cards_indexes]

                    for card_index in held_cards_indexes:
                        if self.hand["cards"][card_index]["card"].getActive():
                            additional_trigger_count = 0
                            card_effects_history = []

                            # Count card enhancment effect
                            score_modifier, condition = self.hand["cards"][card_index]["card"].getEnhancmentScoreModifier()
                            additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition, card_index=card_index)

                            # Count card seal effect
                            score_modifier, condition = self.hand["cards"][card_index]["card"].getSealScoreModifier()
                            additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition, card_index=card_index)

                            # Count joker effect on card
                            for joker_index in active_joker_indexes:
                                if joker_index is None:
                                    continue
                                self.cur_joker_index = joker_index
                                score_modifier, condition = self.jokers[joker_index]["card"].getBaseScoreModifier(simulation=self)
                                additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition, card_index=card_index, activated_joker_indexes=activated_joker_indexes, joker_index=joker_index)

                            # Save card effects history in the general effects history along with trigger count information
                            effects_history.append({
                                "effect": [score_modifier for score_modifier in card_effects_history],
                                "trigger_count": 1 + additional_trigger_count
                            })

                case "owned_jokers":
                    for joker_index in range(len(self.jokers)):
                        additional_trigger_count = 0
                        card_effects_history = []

                        # Count card base effect
                        active_joker_index = active_joker_indexes[joker_index]
                        if active_joker_index is not None:
                            self.cur_joker_index = active_joker_index
                            score_modifier, condition = self.jokers[active_joker_index]["card"].getBaseScoreModifier(simulation=self)
                            additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition)

                        # Count edition effect on card
                        score_modifier, condition = self.jokers[joker_index]["card"].getEditionScoreModifier()
                        additional_trigger_count += self.checkConditionScoring(game_scoring_stage, card_effects_history, score_modifier, condition)

                        # Count mult multipliers for joker rarity
                        rarity_short_code = self.jokers[joker_index]["card"].getRarityShortCode()
                        if rarity_short_code == "uncommon" and "joker_uncommon_mul_multiplier" in self.rules and len(self.rules["joker_uncommon_mul_multiplier"]) > 0:
                            mul_mult = 1.0
                            for m_mul_mult in self.rules["joker_uncommon_mul_multiplier"]:
                                mul_mult *= m_mul_mult
                            score_modifier = {"mul_mult": mul_mult}
                            card_effects_history.append(score_modifier)

                        # Save card effects history in the general effects history along with trigger count information
                        effects_history.append({
                            "effect": [score_modifier for score_modifier in card_effects_history],
                            "trigger_count": 1 + additional_trigger_count
                        })

        # Calculate score modifiers based on data saved in general effects history
        for card in effects_history:
            card_effect = card["effect"]
            for trigger_index in range(card["trigger_count"]):
                for score_modifier in card_effect:
                    if "add_chip" in score_modifier:
                        cur_score["max_chip"] += score_modifier["add_chip"]
                        if "activate_probability" not in score_modifier or not score_modifier["activate_probability"]:
                            cur_score["min_chip"] += score_modifier["add_chip"]
                    if "add_mult" in score_modifier:
                        cur_score["max_mult"] += score_modifier["add_mult"]
                        if "activate_probability" not in score_modifier or not score_modifier["activate_probability"]:
                            cur_score["min_mult"] += score_modifier["add_mult"]
                    if "mul_mult" in score_modifier:
                        cur_score["max_mult"] *= score_modifier["mul_mult"]
                        if "activate_probability" not in score_modifier or not score_modifier["activate_probability"]:
                            cur_score["min_mult"] *= score_modifier["mul_mult"]

        return cur_score
    
    def printState(self):
        self.logger.info("State:")
        for name, value in self.state.items():
            self.logger.info(F"-> {name}: {value}")

    def printPokerHands(self, index=None):
        self.logger.info("Poker hands: None" if len(self.poker_hands) == 0 else "Poker hands:")
        
        if index is not None:
            if index >= 0 and index < len(self.poker_hands):
                self.logger.info(F"{index + 1}) {self.poker_hands[index]}")
            else:
                self.logger.error("ERROR: Index out of scope")
        else:
            for index in range(len(self.poker_hands)):
                self.logger.info(F"{index + 1}) {self.poker_hands[index]}")

    def printHand(self, index=None):
        self.logger.info("Cards: None" if len(self.hand["cards"]) == 0 else "Cards")
        
        if index is not None:
            if index >= 0 and index < len(self.hand["cards"]):
                card = self.hand["cards"][index]["card"]
                selected = self.hand['cards'][index]['selected']

                self.logger.info(F"Card: {card}")
                self.logger.info(F"Selected: {str(selected)}")
            else:
                self.logger.error("ERROR: Index out of scope")
        else:
            selected_indexes = []
            for index in range(len(self.hand["cards"])):
                card = self.hand["cards"][index]["card"]
                selected = self.hand['cards'][index]['selected']
                if selected:
                    selected_indexes.append(index + 1)

                self.logger.info(F"{index + 1}) {card}")
            
            self.logger.info("---")
            self.logger.info(F"Selected: {selected_indexes}")

    def printJokers(self, index=None):
        self.logger.info("Jokers: None" if len(self.jokers) == 0 else "Jokers:")
        
        if index is not None:
            if index >= 0 and index < len(self.jokers):
                joker = self.jokers[index]["card"]
                self.logger.info(F"Joker: {joker}")
            else:
                self.logger.error("ERROR: Index out of scope")
        else:
            for index in range(len(self.jokers)):
                joker = self.jokers[index]["card"]
                self.logger.info(F"{index + 1}) {joker}")
    
    def printCalculatedScore(self):
        calculated_score = self.calculateScore()
        if calculated_score["min_chip"] == calculated_score["max_chip"] and calculated_score["min_mult"] == calculated_score["max_mult"]:
            chip = calculated_score["min_chip"] if calculated_score["min_chip"] < SCIENTIFIC_NOTATION_MIN_VALUE else "{:.2E}".format(calculated_score["min_chip"])
            mult = calculated_score["min_mult"] if calculated_score["min_mult"] < SCIENTIFIC_NOTATION_MIN_VALUE else "{:.2E}".format(calculated_score["min_mult"])
            result = calculated_score["min_chip"] * calculated_score["min_mult"]
            if result > SCIENTIFIC_NOTATION_MIN_VALUE: result = "{:.2E}".format(result)
            
            self.logger.info(F"Calculated score:")
            self.logger.info(F"    -> {chip} Chip x {mult} Mult = {result} Points")
        else:
            min_chip = calculated_score["min_chip"] if calculated_score["min_chip"] < SCIENTIFIC_NOTATION_MIN_VALUE else "{:.2E}".format(calculated_score["min_chip"])
            min_mult = calculated_score["min_mult"] if calculated_score["min_mult"] < SCIENTIFIC_NOTATION_MIN_VALUE else "{:.2E}".format(calculated_score["min_mult"])
            min_result = calculated_score["min_chip"] * calculated_score["min_mult"]
            if min_result > SCIENTIFIC_NOTATION_MIN_VALUE: min_result = "{:.2E}".format(min_result)

            max_chip = calculated_score["max_chip"] if calculated_score["max_chip"] < SCIENTIFIC_NOTATION_MIN_VALUE else "{:.2E}".format(calculated_score["max_chip"])
            max_mult = calculated_score["max_mult"] if calculated_score["max_mult"] < SCIENTIFIC_NOTATION_MIN_VALUE else "{:.2E}".format(calculated_score["max_mult"])
            max_result = calculated_score["max_chip"] * calculated_score["max_mult"]
            if max_result > SCIENTIFIC_NOTATION_MIN_VALUE: max_result = "{:.2E}".format(max_result)
            
            self.logger.info(F"Calculated score:")
            self.logger.info(F"    -> Min: {min_chip} Chip x {min_mult} Mult = {min_result} Points")
            self.logger.info(F"    -> Max: {max_chip} Chip x {max_mult} Mult = {max_result} Points")