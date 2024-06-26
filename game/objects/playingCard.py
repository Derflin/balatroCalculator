from copy import deepcopy

from config import INDENT
from game.static import CARD_RANK, CARD_RANK_STID, STONE_CARD_ID, STONE_CARD_RANK, CARD_SUIT, CARD_SUIT_STID, STONE_CARD_SUIT
from game.objects.cardEdition import CardEdition
from game.objects.cardEnhancment import CardEnhancment
from game.objects.cardSeal import CardSeal

class PlayingCard:
    def __init__(self, sim_ref, id=0, stid=None, suit_id=0, suit_stid=None, enhancment_id=0, enhancment_stid=None, edition_id=0, edition_stid=None, seal_id=0, seal_stid=None, additional_chip=0, active=True):
        self.sim_ref = sim_ref
        self.setBase(id, stid)
        self.setSuit(suit_id, suit_stid)

        self.setEdition(edition_id, edition_stid)
        self.setEnhancment(enhancment_id, enhancment_stid)
        self.setSeal(seal_id, seal_stid)

        self.setAdditionalChip(additional_chip)

        self.setActive(active)

    def __str__(self):
        pattern = '\n'.join((
            "{} of {}",
            INDENT + "-> Status: {}",
            INDENT + "-> Effect: {} Chip + {} Additional Chip"
        ))
        status = "ACTIVE" if self.active else "DEBUFFED"
        base_chip = (self.getEffectActive("b_add_chip") * self.getEffectActive("m_add_chip"))
        add_chip = self.getEffectActive("a_add_chip")
        result_text = pattern.format(self.name, self.suit["name"], status, base_chip, add_chip)

        additional_texts = [str(self.edition), str(self.enhancment), str(self.seal)]
        for text in additional_texts:
            if text != "":
                result_text += F"\n{INDENT}-> {text}"

        return result_text
    
    def setBase(self, id=None, stid=None):
        if stid is not None and stid in CARD_RANK_STID:
            base_id = CARD_RANK_STID[stid]
        else:
            base_id = id if id is not None else 0
            base_id = base_id if base_id >= 0 and base_id < len(CARD_RANK) else 0

        base_card = deepcopy(CARD_RANK[base_id])

        self.id = base_card["id"]
        self.name = base_card["name"]

        self.rank = base_card["rank"]

        self.effect_active = base_card["effect_active"] if "effect_active" in base_card else {}
        self.condition = base_card["condition"] if "condition" in base_card else {}

    def getId(self, exclude_stone=False):
        return self.id if exclude_stone or not self.getStonedStatus() else STONE_CARD_ID

    def getRank(self):
        return self.rank if not self.getStonedStatus() else STONE_CARD_RANK

    def getSuit(self):
        return self.suit["id"] if not self.getStonedStatus() else STONE_CARD_SUIT
    
    def setSuit(self, id=None, stid=None):
        if stid is not None and stid in CARD_SUIT_STID:
            id = CARD_SUIT_STID[stid]
        else:
            if id is None or id < 0 or id > len(CARD_SUIT):
                id = 0 
        self.suit = CARD_SUIT[id]

    def getEdition(self):
        return self.edition

    def setEdition(self, id=None, stid=None):
        self.edition = CardEdition(id=id, stid=stid)

    def getEnhancment(self):
        return self.enhancment
    
    def setEnhancment(self, id=None, stid=None):
        self.enhancment = CardEnhancment(id=id, stid=stid)

    def getSeal(self):
        return self.seal
    
    def setSeal(self, id=None, stid=None):
        self.seal = CardSeal(id=id, stid=stid)

    def getEffectsActive(self):
        return self.effect_active
    
    def getEffectActive(self, key):
        if key in self.effect_active:
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
    
    def getAdditionalChip(self):
        return self.effect_active["a_add_chip"] if "a_add_chip" in self.effect_active else 0

    def setAdditionalChip(self, value):
        self.effect_active["a_add_chip"] = value if value is not None else 0

    def addAdditionalChip(self, value):
        if "a_add_chip" not in self.effect_active:
            self.setAdditionalChip(value)
            
        self.effect_active["a_add_chip"] += value if value is not None else 0

    def getActive(self):
        return self.active
    
    def setActive(self, value):
        self.active = bool(value) if value is not None else True

    def getWildcardStatus(self):
        enhancment_passive_effect = self.enhancment.getEffectsPassive()
        return enhancment_passive_effect["wildcard"] if self.active and enhancment_passive_effect is not None and "wildcard" in enhancment_passive_effect else False
    
    def getStonedStatus(self):
        enhancment_passive_effect = self.enhancment.getEffectsPassive()
        return enhancment_passive_effect["stoned"] if enhancment_passive_effect is not None and "stoned" in enhancment_passive_effect else False
    
    def getBaseScoreModifier(self):
        score_modifier = {}
        if self.active:
            card_add_chip = self.getEffectActive("b_add_chip") * self.getEffectActive("m_add_chip") + self.getEffectActive("a_add_chip")
            card_add_mult = self.getEffectActive("b_add_mult") * self.getEffectActive("m_add_mult") + self.getEffectActive("a_add_mult")
            card_mul_mult = self.getEffectActive("b_mul_mult") * self.getEffectActive("m_mul_mult") + self.getEffectActive("a_mul_mult")
            card_add_trig = self.getEffectActive("a_trigger")

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

    def getEnhancmentScoreModifier(self):
        if self.active:
            return self.enhancment.getBaseScoreModifier()
        else:
            return {}, None
        
    def getSealScoreModifier(self):
        if self.active:
            return self.seal.getBaseScoreModifier()
        else:
            return {}, None
        
    def toDict(self):
        export_dict = {
            "id": self.getId(exclude_stone=True),
            "suit_id": self.getSuit(),
            "enhancment": self.getEnhancment().toDict(),
            "edition": self.getEdition().toDict(),
            "seal": self.getSeal().toDict(),
            "additional_chip": self.getAdditionalChip(),
            "active": self.getActive()
        }
        return export_dict

    def fromDict(self, export_dict):
        self.__init__(
            sim_ref=self.sim_ref,
            id = export_dict["id"],
            suit_id = export_dict["suit_id"],
            additional_chip = export_dict["additional_chip"],
            active = export_dict["active"]
        )
        self.getEnhancment().fromDict(export_dict["enhancment"])
        self.getEdition().fromDict(export_dict["edition"])
        self.getSeal().fromDict(export_dict["seal"])
