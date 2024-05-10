from config import INDENT
from game.static import POKER_HANDS

class PokerHand:
    def __init__(self, id = 0, level = 1, played_count = 0):
        self.setBase(id)

        self.setLevel(level, init_value=1)

        self.setPlayedCount(played_count)

    def __str__(self):
        pattern = '\n'.join((
            "{} Lv. {}",
            INDENT + "-> Effect: {} Chip x {} Mult",
            INDENT + "-> Upgrade: {} Chip AND {} Mult",
        ))

        base_score_modifier = self.getBaseScoreModifier()
        upgrade_score_modifier = self.getUpgradeScoreModifier()
        return pattern.format(self.name, self.level, base_score_modifier[0], base_score_modifier[1], upgrade_score_modifier[0], upgrade_score_modifier[1])

    def setBase(self, id):
        base_hand = POKER_HANDS[id]

        self.id = base_hand["id"]
        self.name = base_hand["name"]
        self.short_code = base_hand["short_code"]

        self.effect_active = base_hand["effect_active"]

        self.upgrade = base_hand["upgrade"] if "upgrade" in base_hand else None

        self.type_base = base_hand["type_base"]
        self.type_combine = base_hand["type_combine"] if "type_combine" in base_hand else []

    def getId(self):
        return self.id

    def getShortCode(self):
        return self.short_code

    def getEffectsActive(self):
        return self.effect_active

    def getLevel(self):
        return self.level

    def setLevel(self, value, init_value=None):
        if init_value is not None:
            self.level = init_value

        if value != self.level:
            if self.upgrade is not None:
                level_offset = value - self.level

                if "effect_active" in self.upgrade:
                    for u_name, u_value in self.upgrade["effect_active"].items():
                        self.effect_active[u_name] += u_value * level_offset
            
            self.level = value

    def addLevel(self, value = 1):
        if self.upgrade is not None:
            level_offset = value
            
            if "effect_active" in self.upgrade:
                for u_name, u_value in self.upgrade["effect_active"].items():
                    self.effect_active[u_name] += u_value * level_offset

        self.level += value

    def getType(self):
        return self.type_base, self.type_combine

    def getPlayedCount(self):
        return self.played_count
    
    def setPlayedCount(self, value):
        self.played_count = value

    def addPlayedCount(self, value = 1):
        self.played_count += value

    def getBaseScoreModifier(self):
        base_chip = self.effect_active["b_add_chip"]
        base_mult = self.effect_active["b_add_mult"]
        return base_chip, base_mult
    
    def getUpgradeScoreModifier(self):
        base_chip = self.upgrade["effect_active"]["b_add_chip"] if "effect_active" in self.upgrade and "b_add_chip" in self.upgrade["effect_active"] else 0
        base_mult = self.upgrade["effect_active"]["b_add_mult"] if "effect_active" in self.upgrade and "b_add_mult" in self.upgrade["effect_active"] else 0
        return base_chip, base_mult
    
    def toDict(self):
        export_dict = {
            "id": self.getId(),
            "level": self.getLevel(),
            "played_count": self.getPlayedCount()
        }
        return export_dict

    def fromDict(self, export_dict):
        self.__init__(
            id = export_dict["id"], 
            level = export_dict["level"], 
            played_count = export_dict["played_count"]
        )