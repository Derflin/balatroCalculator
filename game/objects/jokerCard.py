import math

from config import INDENT
from game.static import JOKERS, JOKER_RARITY, DEFAULT_DECK_SIZE, CARD_RANK_STID
from game.objects.cardEdition import CardEdition

class JokerCard:
    def __init__(self, id=0, edition_id=0, level=0, additional_sell_value=0, active=True):
        self.setBase(id)
        
        self.setEdition(edition_id)

        self.setLevel(level, init_value=0)
    
        self.setAdditionalSellValue(additional_sell_value)

        self.setActive(active)

    def __str__(self):
        pattern = '\n'.join((
            "{}{} | {}",
            INDENT + "-> Status: {}",
            INDENT + "-> Effect Active: {}",
            INDENT + "-> Effect Passive: {}",
            INDENT + "-> Condition: {}",
            INDENT + "-> Sell Value: {}"
        ))
        level = F" Lv. {self.level}" if self.upgrade is not None else ""
        rarity_name = JOKER_RARITY[self.rarity_id]["name"]
        status = "ACTIVE" if self.active else "DEBUFFED"
        effect_active = "None" if not self.effect_active else str(self.effect_active)
        effect_passive = "None" if not self.effect_passive else " | ".join([key for key in self.effect_passive])
        condition = "None" if not self.condition else str(self.condition)
        condition += "" if not self.condition_variety else F" | Variety: {str(self.condition_variety)}"
        result_text = pattern.format(self.name, level, rarity_name, status, effect_active, effect_passive, condition, self.getSellValue())

        additional_texts = [str(self.edition)]
        for text in additional_texts:
            if text != "":
                result_text += F"\n{INDENT}-> {text}"

        return result_text
    
    def setBase(self, id):
        base_id = id if id is not None else 0
        base_id = base_id if base_id >= 0 and base_id < len(JOKERS) else 0

        base_joker = JOKERS[base_id]

        self.id = base_joker["id"]
        self.name = base_joker["name"]
        self.rarity_id = base_joker["rarity"]

        self.affect_scoring = base_joker["affect_scoring"] if "affect_scoring" in base_joker else True
        self.copy_compat = base_joker["copy_compat"]

        self.scoring_order = base_joker["scoring_order"]
        
        self.effect_active = base_joker["effect_active"] if "effect_active" in base_joker else {}
        self.effect_passive = base_joker["effect_passive"] if "effect_passive" in base_joker else {}
        self.condition = base_joker["condition"] if "condition" in base_joker else {}
        self.condition_variety = base_joker["condition_variety"] if "condition_variety" in base_joker else {}
        
        self.upgrade = base_joker["upgrade"] if "upgrade" in base_joker else None

        self.b_cost = base_joker["cost"]

    def getId(self):
        return self.id

    def getRarityShortCode(self):
        return JOKER_RARITY[self.rarity_id]["short_code"]

    def getEdition(self):
        return self.edition

    def setEdition(self, edition_id):
        self.edition = CardEdition(edition_id)

    def getCopyCompat(self):
        return self.copy_compat
    
    def getScoringOrder(self):
        return self.scoring_order

    def getEffectsActive(self):
        return self.effect_active
    
    def getEffectActive(self, key, simulation=None):
        if key in self.effect_active:
            if isinstance(self.effect_active[key], str):
                key_value = self.effect_active[key]
                match key_value:
                    case "discard_remain":
                        discard_count = simulation.getState(key="discard_remain")
                        if discard_count is not None:
                            return discard_count
                    case "card_deck_remain":
                        card_deck_remain = simulation.getState(key="card_deck_remain")
                        if card_deck_remain is not None:
                            return card_deck_remain
                    case "stone_card_deck_count":
                        stone_card_deck_count = simulation.getState(key="stone_card_deck_count")
                        if stone_card_deck_count is not None:
                            return stone_card_deck_count
                    case "dollar_count":
                        dollar_count = simulation.getState(key="dollar_count")
                        if dollar_count is not None:
                            return dollar_count
                    case "joker_count":
                        joker_count = simulation.getState(key="joker_count")
                        if joker_count is not None:
                            return joker_count
                    case "deck_below_default_count":
                        card_deck_size = simulation.getState(key="card_deck_size")
                        if card_deck_size is not None:
                            value = DEFAULT_DECK_SIZE - card_deck_size
                            return value if value >= 0 else 0
                    case "dollar_count_div_five":
                        dollar_count = simulation.getState(key="dollar_count")
                        if dollar_count is not None:
                            value = dollar_count // 5
                            return value if value >= 0 else 0
                    case "left_jokers_sell_value":
                        sell_value = simulation.getJokerSellValueFromLeft()
                        return sell_value if sell_value >= 0 else 0
                    case "held_queen_count":
                        count = 0
                        held_cards = simulation.getHandPlayingCards(held_hand=True, card_id=True)
                        for card_id in held_cards["id"]:
                            if card_id == CARD_RANK_STID["Q"]:
                                count += 1
                        return count
                    case "held_lowest_rank":
                        value = None
                        held_cards = simulation.getHandPlayingCards(held_hand=True, card_rank=True)
                        for card_rank in held_cards["rank"]:
                            if value is None or value > card_rank:
                                value = card_rank
                        return value if value is not None else 0
                    case "played_hand_count":
                        played_hand_count = simulation.getPokerHandActivePlayedCount()
                        return played_hand_count
                    case "empty_joker_slot":
                        joker_count_max = simulation.getJokerCountMax()
                        joker_count = simulation.getJokerCount(ignore_id=self.getId())
                        value = joker_count_max - joker_count
                        return value if value >= 0 else 0
                    case "full_deck_steel_card_count":
                        steel_card_deck_count = simulation.getState(key="steel_card_deck_count")
                        if steel_card_deck_count is not None:
                            return steel_card_deck_count
                    case "skipped_blinds_count":
                        skipped_blinds = simulation.getState(ky="skipped_blinds")
                        if skipped_blinds is not None:
                            return skipped_blinds
            else:
                return self.effect_active[key]
        
        # Return default value
        if key[0:2] == "b_":
            if key[2:6] == "mul_":
                return 1
            else:
                return 0
        if key[0:2] == "a_":
            return 0
        elif key[0:2] in ["m_"]:
            return 1
        else:
            return None

    def getEffectsPassive(self):
        return self.effect_passive
    
    def getConditions(self):
        return self.condition

    def getConditionVariety(self):
        result = {}

        for condition_variety in self.condition_variety:
            result[condition_variety] = self.condition[condition_variety]

        return result 

    def setConditionVariety(self, conditions_dict):
        for condition_name, condition_value in conditions_dict.items():
            if condition_name in self.condition_variety:
                self.condition[condition_name] = [condition_value]

    def getLevel(self):
        return self.level

    def setLevel(self, value, init_value=None):
        if init_value is not None:
            self.level = init_value
        value = value if value is not None else self.level

        if value != self.level:
            if self.upgrade is not None:
                level_offset = value - self.level

                if "effect_active" in self.upgrade:
                    for u_name, u_value in self.upgrade["effect_active"].items():
                        self.effect_active[u_name] += u_value * level_offset
            
            self.level = value

    def addLevel(self, value=1):
        if self.upgrade is not None:
            level_offset = value
            
            if "effect_active" in self.upgrade:
                for u_name, u_value in self.upgrade["effect_active"].items():
                    self.effect_active[u_name] += u_value * level_offset

        self.level += value

    def getBaseCost(self):
        return self.b_cost
    
    def getAdditionalSellValue(self):
        return self.a_sell_value

    def setAdditionalSellValue(self, value):
        self.a_sell_value = value if value is not None else 0

    def addAdditionalSellValue(self, value):
        self.a_sell_value += value if value is not None else 0

    def getActive(self):
        return self.active
    
    def setActive(self, value):
        self.active = bool(value) if value is not None else True

    #NOTE: Based on: https://www.reddit.com/r/balatro/comments/1b6lito/base_sell_value_calculation/
    def getSellValue(self, discount_rate=0.0, game_inflation=0):
        cost = (self.getBaseCost() + game_inflation + self.edition.getBaseCost()) * (1.0 - discount_rate)
        sell_value = max(1, math.floor(cost / 2.0)) + self.getAdditionalSellValue()

        return sell_value
    
    def getBaseScoreModifier(self, simulation):
        score_modifier = {}
        if self.active:
            card_add_chip = self.getEffectActive("b_add_chip", simulation) * self.getEffectActive("m_add_chip", simulation) + self.getEffectActive("a_add_chip", simulation)
            card_add_mult = self.getEffectActive("b_add_mult", simulation) * self.getEffectActive("m_add_mult", simulation) + self.getEffectActive("a_add_mult", simulation)
            card_mul_mult = self.getEffectActive("b_mul_mult", simulation) * self.getEffectActive("m_mul_mult", simulation) + self.getEffectActive("a_mul_mult", simulation)
            card_add_trig = self.getEffectActive("a_trigger", simulation)

            if card_add_chip != 0:
                score_modifier["add_chip"] = card_add_chip
            if card_add_mult != 0:
                score_modifier["add_mult"] = card_add_mult
            if card_mul_mult != 1:
                score_modifier["mul_mult"] = card_mul_mult
            if card_add_trig != 0:
                score_modifier["add_trig"] = card_add_trig

        return score_modifier, self.condition
    
    def getEditionScoreModifier(self):
        if self.active:
            return self.edition.getBaseScoreModifier()
        else:
            return {}, None
        
    def toDict(self):
        export_dict = {
            "id": self.getId(),
            "edition": self.getEdition().toDict(),
            "level": self.getLevel(),
            "additional_sell_value": self.getAdditionalSellValue(),
            "active": self.getActive()
        }
        return export_dict

    def fromDict(self, export_dict):
        self.__init__(
            id = export_dict["id"],
            level = export_dict["level"],
            additional_sell_value = export_dict["additional_sell_value"],
            active = export_dict["active"]
        )
        self.getEdition().fromDict(export_dict["edition"])
