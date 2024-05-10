from config import INDENT
from game.static import CARD_SEALS

class CardSeal:
    def __init__(self, id = 0):
        self.setBase(id)

    def __str__(self):
        if self.name == None:
            return ""
        
        score_modifier, _ = self.getBaseScoreModifier()
        if len(score_modifier) > 0:
            result_text = F"Seal: {self.name} -> Score modifier: {score_modifier}"
        else:
            result_text = F"Seal: {self.name}"
        
        return result_text
    
    def setBase(self, id):
        base_seal = CARD_SEALS[id]

        self.id = base_seal["id"]
        self.name = base_seal["name"]

        self.effect_active = base_seal["effect_active"] if "effect_active" in base_seal else {}
        self.effect_passive = base_seal["effect_passive"] if "effect_passive" in base_seal else {}
        self.condition = base_seal["condition"] if "condition" in base_seal else {}

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
    
    def getCondition(self):
        return self.condition
    
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