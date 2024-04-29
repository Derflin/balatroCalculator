from game.static import CARD_RANK, STONE_CARD_ID, STONE_CARD_RANK, CARD_SUIT, STONE_CARD_SUIT
from game.objects.cardEdition import CardEdition
from game.objects.cardEnhancment import CardEnhancment
from game.objects.cardSeal import CardSeal

class PlayingCard:
    def __init__(self, id, suit_id = 0, enhancment_id = 0, edition_id = 0, seal_id = 0, additional_chip = 0):
        base_card = CARD_RANK[id]

        self.id = base_card["id"]
        self.name = base_card["name"]

        self.rank = base_card["rank"]
        self.setSuit(suit_id)

        self.setEdition(edition_id)
        self.setEnhancment(enhancment_id)
        self.setSeal(seal_id)

        self.effect_active = base_card["effect_active"] if "effect_active" in base_card else {}
        self.effect_active["a_add_chip"] = additional_chip
        self.condition = base_card["condition"] if "condition" in base_card else {}

        self.active = True

    def __str__(self):
        pattern = '\n'.join((
            "{} of {}",
            "    -> Status: {}",
            "    -> Effect: {} Chip + {} Additional Chip"
        ))
        status = "ACTIVE" if self.active else "DEBUFFED"
        base_chip = (self.getEffectActive("b_add_chip") * self.getEffectActive("m_add_chip"))
        add_chip = self.getEffectActive("a_add_chip")
        result_text = pattern.format(self.name, self.suit["name"], status, base_chip, add_chip)

        additional_texts = [str(self.edition), str(self.enhancment), str(self.seal)]
        for text in additional_texts:
            if text != "":
                result_text += F"\n    -> {text}"

        return result_text

    def getId(self):
        return self.id if not self.getStonedStatus() else STONE_CARD_ID

    def getRank(self):
        return self.rank if not self.getStonedStatus() else STONE_CARD_RANK

    def getSuit(self):
        return self.suit["id"] if not self.getStonedStatus() else STONE_CARD_SUIT
    
    def setSuit(self, suit_id):
        if suit_id is None or suit_id < 0 or suit_id > len(CARD_SUIT):
            suit_id = 0
        self.suit = CARD_SUIT[suit_id]

    def getEdition(self):
        return self.edition

    def setEdition(self, edition_id):
        self.edition = CardEdition(edition_id)

    def getEnhancment(self):
        return self.enhancment
    
    def setEnhancment(self, enhancment_id):
        self.enhancment = CardEnhancment(enhancment_id)

    def getSeal(self):
        return self.seal
    
    def setSeal(self, seal_id):
        self.seal = CardSeal(seal_id)

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
    
    def setAdditionalChip(self, value):
        self.effect_active["a_add_chip"] = value

    def addAdditionalChip(self, value):
        self.effect_active["a_add_chip"] += value

    def getActive(self):
        return self.active
    
    def setActive(self, value):
        self.active = bool(value)

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
