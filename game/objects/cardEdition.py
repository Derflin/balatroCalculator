from config import INDENT
from game.static import CARD_EDITIONS, CARD_EDITIONS_STID

class CardEdition:
    def __init__(self, id=0, stid=None):
        self.setBase(id, stid)

    def __str__(self):
        if self.name == None:
            return ""
        
        score_modifier, _ = self.getBaseScoreModifier()
        if len(score_modifier) > 0:
            result_text = F"Edition: {self.name} -> Score modifier: {score_modifier}"
        else:
            result_text = F"Edition: {self.name}"

        return result_text

    def setBase(self, id=None, stid=None):
        if stid is not None and stid in CARD_EDITIONS_STID:
            base_id = CARD_EDITIONS_STID[stid]
        else:
            base_id = id if id is not None else 0
            base_id = base_id if base_id >= 0 and base_id < len(CARD_EDITIONS) else 0

        base_edition = CARD_EDITIONS[base_id]
        
        self.id = base_edition["id"]
        self.name = base_edition["name"]

        self.effect_active = base_edition["effect_active"] if "effect_active" in base_edition else {}
        self.effect_passive = base_edition["effect_passive"] if "effect_passive" in base_edition else {}
        self.condition = base_edition["condition"] if "condition" in base_edition else {}
        
        self.b_cost = base_edition["cost"]

    def getId(self):
        return self.id

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

    def getEffectsPassive(self):
        return self.effect_passive
    
    def getBaseCost(self):
        return self.b_cost
    
    def getBaseScoreModifier(self):
        card_add_chip = self.getEffectActive("b_add_chip") * self.getEffectActive("m_add_chip") + self.getEffectActive("a_add_chip")
        card_add_mult = self.getEffectActive("b_add_mult") * self.getEffectActive("m_add_mult") + self.getEffectActive("a_add_mult")
        card_mul_mult = self.getEffectActive("b_mul_mult") * self.getEffectActive("m_mul_mult") + self.getEffectActive("a_mul_mult")
        card_add_trig = self.getEffectActive("a_trigger")

        score_modifier = {}
        if card_add_chip != 0:
            score_modifier["add_chip"] = card_add_chip
        if card_add_mult != 0:
            score_modifier["add_mult"] = card_add_mult
        if card_mul_mult != 1:
            score_modifier["mul_mult"] = card_mul_mult
        if card_add_trig != 0:
            score_modifier["add_trig"] = card_add_trig

        return score_modifier, self.condition
    
    def toDict(self):
        export_dict = {
            "id": self.getId()
        }
        return export_dict

    def fromDict(self, export_dict):
        self.__init__(
            id = export_dict["id"]
        )