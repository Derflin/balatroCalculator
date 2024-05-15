DEFAULT_DECK_SIZE = 52
DEFAULT_JOKER_COUNT_MAX = 5

#[
#   id = Int,
#   name = String,
#   short_code = String
#]
GAME_SCORING_ORDER = [
    {"id": 0, "name": "Played Hand", "short_code": "played_hand"},
    {"id": 1, "name": "Held Hand", "short_code": "held_hand"},
    {"id": 2, "name": "Owned Jokers", "short_code": "owned_jokers"}
]
GAME_SCORING_ORDER_STID = {
    "played_hand": 0,
    "held_hand": 1,
    "owned_jokers": 2
}

#[
#   id = Int,
#   name = String,
#   short_code = String,
#   rank = Int,
#   effect_active [
#       b_add_chip = Int
#   ]
#]
CARD_RANK = [
    {"id": 0, "name": "2", "short_code": "2", "rank": 2, "effect_active": {"b_add_chip": 2}},
    {"id": 1, "name": "3", "short_code": "3", "rank": 3, "effect_active": {"b_add_chip": 3}},
    {"id": 2, "name": "4", "short_code": "4", "rank": 4, "effect_active": {"b_add_chip": 4}},
    {"id": 3, "name": "5", "short_code": "5", "rank": 5, "effect_active": {"b_add_chip": 5}},
    {"id": 4, "name": "6", "short_code": "6", "rank": 6, "effect_active": {"b_add_chip": 6}},
    {"id": 5, "name": "7", "short_code": "7", "rank": 7, "effect_active": {"b_add_chip": 7}},
    {"id": 6, "name": "8", "short_code": "8", "rank": 8, "effect_active": {"b_add_chip": 8}},
    {"id": 7, "name": "9", "short_code": "9", "rank": 9, "effect_active": {"b_add_chip": 9}},
    {"id": 8, "name": "10", "short_code": "10", "rank": 10, "effect_active": {"b_add_chip": 10}},
    {"id": 9, "name": "Jack", "short_code": "J", "rank": 10, "effect_active": {"b_add_chip": 10}},
    {"id": 10, "name": "Queen", "short_code": "Q", "rank": 10, "effect_active": {"b_add_chip": 10}},
    {"id": 11, "name": "King", "short_code": "K", "rank": 10, "effect_active": {"b_add_chip": 10}},
    {"id": 12, "name": "Ace", "short_code": "A", "rank": 10, "effect_active": {"b_add_chip": 11}}
]
CARD_RANK_STID = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "10": 8,
    "J": 9,
    "Q": 10,
    "K": 11,
    "A": 12
}
FACE_CARD_IDS = [9, 10, 11]
STONE_CARD_ID = -2
STONE_CARD_RANK = 0

#[
#   id = Int,
#   name = String,
#   short_code = String
#]
CARD_SUIT = [
    {"id": 0, "name": "Diamonds", "short_code": "D"},
    {"id": 1, "name": "Hearts", "short_code": "H"},
    {"id": 2, "name": "Spades", "short_code": "S"},
    {"id": 3, "name": "Clubs", "short_code": "C"}
]
CARD_SUIT_STID = {
    "D": 0,
    "H": 1,
    "S": 2,
    "C": 3
}
STONE_CARD_SUIT = -2

#[
#   id = Int,
#   name = String,
#   short_code = String,
#   effect_active [
#       b_add_chip = Int,
#       b_add_mult = Int,
#   ],
#   upgrade [
#       b_add_chip = Int,
#       b_add_mult = Int
#   ],
#   type_base = Boolean,
#   type_combine = Int[]
#]
#TODO: maybe try to add some kind of pattern for each poker hand, so that it would be possible to detect them dynamically depending on the pattern instead of hardcoded
#       --- for example "_;s+_;s+_;s+_;s+_;s"
POKER_HANDS = [
    {"id": 0, "name": "High Card", "short_code": "high_card", "effect_active": {"b_add_chip": 5, "b_add_mult": 1}, "upgrade": {"effect_active": {"b_add_chip": 10, "b_add_mult": 1}}, "type_base": True},
    {"id": 1, "name": "Pair", "short_code": "pair", "effect_active": {"b_add_chip": 10, "b_add_mult": 2}, "upgrade": {"effect_active": {"b_add_chip": 15, "b_add_mult": 1}}, "type_base": True, "type_combine": [0]},
    {"id": 2, "name": "Two Pair", "short_code": "two_pair", "effect_active": {"b_add_chip": 20, "b_add_mult": 2}, "upgrade": {"effect_active": {"b_add_chip": 20, "b_add_mult": 1}}, "type_base": True, "type_combine": [0, 1]},
    {"id": 3, "name": "Three of a Kind", "short_code": "three_of_kind", "effect_active": {"b_add_chip": 30, "b_add_mult": 3}, "upgrade": {"effect_active": {"b_add_chip": 15, "b_add_mult": 2}}, "type_base": True, "type_combine": [0, 1]},
    {"id": 4, "name": "Straight", "short_code": "straight", "effect_active": {"b_add_chip": 30, "b_add_mult": 4}, "upgrade": {"effect_active": {"b_add_chip": 20, "b_add_mult": 2}}, "type_base": True, "type_combine": [0]},
    {"id": 5, "name": "Flush", "short_code": "flush", "effect_active": {"b_add_chip": 35, "b_add_mult": 4}, "upgrade": {"effect_active": {"b_add_chip": 25, "b_add_mult": 2}}, "type_base": True, "type_combine": [0]},
    {"id": 6, "name": "Full House", "short_code": "full_house", "effect_active": {"b_add_chip": 40, "b_add_mult": 4}, "upgrade": {"effect_active": {"b_add_chip": 30, "b_add_mult": 2}}, "type_base": False, "type_combine": [0, 1, 2, 3]},
    {"id": 7, "name": "Four of a Kind", "short_code": "four_of_kind", "effect_active": {"b_add_chip": 60, "b_add_mult": 7}, "upgrade": {"effect_active": {"b_add_chip": 30, "b_add_mult": 3}}, "type_base": True, "type_combine": [0, 1, 3]},
    {"id": 8, "name": "Straight Flush", "short_code": "straight_flush", "effect_active": {"b_add_chip": 100, "b_add_mult": 8}, "upgrade": {"effect_active": {"b_add_chip": 40, "b_add_mult": 3}}, "type_base": False, "type_combine": [0, 4, 5]},
    {"id": 9, "name": "Five of a Kind", "short_code": "five_of_kind", "effect_active": {"b_add_chip": 120, "b_add_mult": 12}, "upgrade": {"effect_active": {"b_add_chip": 35, "b_add_mult": 3}}, "type_base": True, "type_combine": [0, 1, 3, 7]},
    {"id": 10, "name": "Flush House", "short_code": "flush_house", "effect_active": {"b_add_chip": 140, "b_add_mult": 14}, "upgrade": {"effect_active": {"b_add_chip": 40, "b_add_mult": 3}}, "type_base": False, "type_combine": [0, 1, 2, 3, 5]},
    {"id": 11, "name": "Flush Five", "short_code": "flush_five", "effect_active": {"b_add_chip": 160, "b_add_mult": 16}, "upgrade": {"effect_active": {"b_add_chip": 40, "b_add_mult": 3}}, "type_base": False, "type_combine": [0, 1, 3, 5, 7, 9]}
]
POKER_HANDS_STID = {
    "high_card": 0,
    "pair": 1,
    "two_pair": 2,
    "three_of_kind": 3,
    "straight": 4,
    "flush": 5,
    "full_house": 6,
    "four_of_kind": 7,
    "straight_flush": 8,
    "five_of_kind": 9,
    "flush_house": 10,
    "flush_five": 11
}

#[
#   id = Int,
#   name = String,
#   cost = Int,
#   effect_active [
#       b_add_chip = Int,
#       b_add_mult = Int,
#       b_mul_mult = Float
#   ],
#   effect_passive [
#       joker_add_max_count = Int
#   ]
#]
CARD_EDITIONS = [
    {"id": 0, "name": "Base", "cost": 0},
    {"id": 1, "name": "Foil", "cost": 2, "effect_active": {"b_add_chip": 50}},
    {"id": 2, "name": "Holographic", "cost": 3, "effect_active": {"b_add_mult": 10}},
    {"id": 3, "name": "Polychrome", "cost": 5, "effect_active": {"b_mul_mult": 1.5}},
    {"id": 4, "name": "Negative", "cost": 5, "effect_passive": {"joker_add_max_count": 1}}
]
CARD_EDITIONS_STID = {
    "base": 0,
    "foil": 1,
    "holo": 2,
    "poly": 3,
    "nega": 4
}

#[
#   id = Int,
#   name = String,
#   effect_active  [
#       b_add_chip = Int,
#       b_add_mult = Int,
#       b_mul_mult = Float
#   ],
#   effect_passive [
#       wildcard = Boolean,
#       stoned = Boolean
#   ],
#   condition [
#       card_played = Boolean,
#       card_held = Boolean,
#       activate_probability = Float
#   ]
#]
CARD_ENHANCMENTS = [
    {"id": 0, "name": None},
    {"id": 1, "name": "Bonus Card", "effect_active": {"b_add_chip": 30}, "condition": {"card_played": True}},
    {"id": 2, "name": "Mult Card", "effect_active": {"b_add_mult": 4}, "condition": {"card_played": True}},
    {"id": 3, "name": "Wild Card", "effect_passive": {"wildcard": True}},
    {"id": 4, "name": "Glass Card", "effect_active": {"b_mul_mult": 2.0}, "condition": {"card_played": True}},
    {"id": 5, "name": "Steel Card", "effect_active": {"b_mul_mult": 1.5}, "condition": {"card_held": True}},
    {"id": 6, "name": "Stone Card", "effect_active": {"b_add_chip": 50}, "effect_passive": {"stoned": True}, "condition": {"card_played": True}},
    {"id": 7, "name": "Gold Card"},
    {"id": 8, "name": "Lucky Card", "effect_active": {"b_add_mult": 20}, "condition": {"card_played": True, "activate_probability": 1.0/5.0}}
]
CARD_ENHANCMENTS_STID = {
    "bonus_card": 1,
    "mult_card": 2,
    "wild_card": 3,
    "glass_card": 4,
    "steel_card": 5,
    "stone_card": 6,
    "gold_card": 7,
    "lucky_card": 8
}

#[
#   id = Int,
#   name = String,
#   effect_active [
#       a_trigger = Int
#   ],
#   condition [
#       card_played = Boolean,
#       card_held = Boolean,
#   ]
#]
CARD_SEALS = [
    {"id": 0, "name": None},
    {"id": 1, "name": "Gold Seal"},
    {"id": 2, "name": "Red Seal", "effect_active": {"a_trigger": 1}},
    {"id": 3, "name": "Blue Seal"},
    {"id": 4, "name": "Purple Seal"}
]
CARD_SEALS_STID = {
    "gold": 1,
    "red": 2,
    "blue": 3,
    "purple": 4
}

#[
#   id = Int,
#   name = String,
#   short_code = String
#]
JOKER_RARITY = [
    {"id": 0, "name": "Common", "short_code": "common"},
    {"id": 1, "name": "Uncommon", "short_code": "uncommon"},
    {"id": 2, "name": "Rare", "short_code": "rare"},
    {"id": 3, "name": "Legendary", "short_code": "legendary"}
]
JOKER_RARITY_STID = {
    "common": 0,
    "uncommon": 1,
    "rare": 2,
    "legendary": 3
}

#[
#   id = Int, 
#   name = String,
#   affect_scoring = Boolean,
#   copy_compat = Boolean, 
#   rarity = Int{ 0, 1, 2, 3 },                                         ### common/uncommon/rare/legendary ###
#   cost = Int, 
#   effect_active [
#       b_add_chip = Int, 
#       b_add_mult = Int,
#       b_mul_mult = Float, 
#       m_add_chip = Int/String{ "discard_remain", "card_deck_remain", "stone_card_deck_count", "dollar_count" }, 
#       m_add_mult = Int/String{ "joker_count", "deck_below_default_count", "dollar_count_div_five", "other_jokers_sell_value", "left_jokers_sell_value", "held_queen_count", "held_lowest_rank", "played_hand_count" },
#       m_mul_mult = Int/String{ "empty_joker_slot", "steel_card_deck_count", "skipped_blinds_count" },
#       a_add_chip = Int,
#       a_add_mult = Int,
#       a_mul_mult = Float, 
#       a_trigger = Int,
#       copy_mostleft = Boolean,
#       copy_right = Boolean
#   ],
#   effect_passive [
#       double_probability = Boolean,
#       smeared_suits = Boolean,
#       joker_uncommon_mul_multiplier = Float,
#       four_flush_straight = Boolean,
#       all_face_cards = Boolean,
#       every_played_card_counts = Boolean,
#       removes_enhancements = Boolean,
#       straight_gap = Boolean,
#       face_cards_to_gold = Boolean
#   ], 
#   scoring_order = String,
#   condition [
#       card_suit = String[],                       # played_hand
#       played_hand_contain_type = String,          # joker_level
#       played_hand_size_max = Int,                 # joker_level
#       played_hand_size_min = Int,                 # joker_level
#       played_hand_suit = String[],                # joker_level
#       played_hand_no_face_card = Boolean,         # joker_level
#       held_hand_only_suit = String[],             # joker_level
#       discard_remain_max = Int,                   # joker_level
#       discard_remain_min = Int,                   # joker_level
#       card_rank = String[],                       # played_hand, held_hand
#       trigger_once = Boolean,                     # played_hand - because of it, the joker will only affect first card
#       activate_probability = Float                #depends
#   ],
#   condition_variety = String[],
#   upgrade [
#       m_add_chip = Int, 
#       m_add_mult = Int,
#       m_mul_mult = Int
#   ]
#]
JOKERS = [
    {"id": 0, "name": "Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 2, "effect_active": {"b_add_mult": 4}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 1, "name": "Greedy Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 3}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_suit": [CARD_SUIT_STID["D"]]}},
    {"id": 2, "name": "Lusty Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 3}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_suit": [CARD_SUIT_STID["H"]]}},
    {"id": 3, "name": "Wrathful Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 3}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_suit": [CARD_SUIT_STID["S"]]}},
    {"id": 4, "name": "Gluttonous Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 3}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_suit": [CARD_SUIT_STID["C"]]}},
    {"id": 5, "name": "Jolly Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 3, "effect_active": {"b_add_mult": 8}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["pair"]}},
    {"id": 6, "name": "Zany Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 12}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["three_of_kind"]}},
    {"id": 7, "name": "Mad Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 10}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["two_pair"]}},
    {"id": 8, "name": "Crazy Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 12}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["straight"]}},
    {"id": 9, "name": "Droll Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 10}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["flush"]}},
    {"id": 10, "name": "Sly Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 3, "effect_active": {"b_add_chip": 50}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["pair"]}},
    {"id": 11, "name": "Wily Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_chip": 100}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["three_of_kind"]}},
    {"id": 12, "name": "Clever Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_chip": 80}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["two_pair"]}},
    {"id": 13, "name": "Devious Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_chip": 100}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["straight"]}},
    {"id": 14, "name": "Crafty Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_chip": 80}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["flush"]}},
    {"id": 15, "name": "Half Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 20}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_size_max": 3}},
    {"id": 16, "name": "Joker Stencil", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 8, "effect_active": {"b_mul_mult": 1.0, "m_mul_mult": "empty_joker_slot"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 17, "name": "Four Fingers", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_passive": {"four_flush_straight": True}, "scoring_order": None},
    {"id": 18, "name": "Mime", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "effect_active": {"a_trigger": 1}, "scoring_order": GAME_SCORING_ORDER_STID["held_hand"]},
    {"id": 19, "name": "Credit Card", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["common"], "cost": 1, "scoring_order": None},
    {"id": 20, "name": "Ceremonial Dagger", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_add_mult": 2, "m_add_mult": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_mult": 1}}},
    {"id": 21, "name": "Banner", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_chip": 40, "m_add_chip": "discard_remain"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 22, "name": "Mystic Summit", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 15}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"discard_remain_max": 0}},
    {"id": 23, "name": "Marble Joker", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 24, "name": "Loyalty Card", "affect_scoring": True, "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "effect_active": {"b_mul_mult": 4.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 25, "name": "8 Ball", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "scoring_order": None},
    {"id": 26, "name": "Misprint", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 1, "m_add_mult": [0, 23]}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 27, "name": "Dusk", "affect_scoring": True, "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "effect_active": {"a_trigger": 1}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"]},
    {"id": 28, "name": "Raised Fist", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 2, "m_add_mult": "held_lowest_rank"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 29, "name": "Chaos the Clown", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 30, "name": "Fibonacci", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 8, "effect_active": {"b_add_mult": 8}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["2"], CARD_RANK_STID["3"], CARD_RANK_STID["5"], CARD_RANK_STID["8"], CARD_RANK_STID["A"]]}},
    {"id": 31, "name": "Steel Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_active": {"b_mul_mult": 0.20, "m_mul_mult": "steel_card_deck_count", "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 32, "name": "Scary Face", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_chip": 30}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["J"], CARD_RANK_STID["Q"], CARD_RANK_STID["K"]]}},
    {"id": 33, "name": "Abstract Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 3, "m_add_mult": "joker_count"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 34, "name": "Delayed Gratification", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 35, "name": "Hack", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"a_trigger": 1}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["2"], CARD_RANK_STID["3"], CARD_RANK_STID["4"], CARD_RANK_STID["5"]]}},
    {"id": 36, "name": "Pareidolia", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "effect_passive": {"all_face_cards": True}, "scoring_order": None},
    {"id": 37, "name": "Gros Michel", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 15}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 38, "name": "Even Steven", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 4}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["2"], CARD_RANK_STID["4"], CARD_RANK_STID["6"], CARD_RANK_STID["8"], CARD_RANK_STID["10"]]}},
    {"id": 39, "name": "Odd Todd", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_chip": 31}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["3"], CARD_RANK_STID["5"], CARD_RANK_STID["7"], CARD_RANK_STID["9"], CARD_RANK_STID["A"]]}},
    {"id": 40, "name": "Scholar", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_chip": 20, "b_add_mult": 4}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["A"]]}},
    {"id": 41, "name": "Business Card", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 42, "name": "Supernova", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 1, "m_add_mult": "played_hand_count"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 43, "name": "Ride the Bus", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 6, "effect_active": {"b_add_mult": 1, "m_add_mult": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_no_face_card": True}, "upgrade": {"effect_active": {"m_add_mult": 1}}},
    {"id": 44, "name": "Space Joker", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "scoring_order": None},
    {"id": 45, "name": "Egg", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 46, "name": "Burglar", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 47, "name": "Blackboard", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 3.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"held_hand_only_suit": [CARD_SUIT_STID["S"], CARD_SUIT_STID["C"]]}},
    {"id": 48, "name": "Runner", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_chip": 15, "m_add_chip": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_chip": 1}}},
    {"id": 49, "name": "Ice Cream", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_chip": 5, "m_add_chip": 20}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_chip": -1}}},
    {"id": 50, "name": "DNA", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "scoring_order": None},
    {"id": 51, "name": "Splash", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["common"], "cost": 3, "effect_passive": {"every_played_card_counts": True}, "scoring_order": None},
    {"id": 52, "name": "Blue Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_chip": 2, "m_add_chip": "card_deck_remain"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 53, "name": "Sixth Sense", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 54, "name": "Constellation", "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 0.1, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 55, "name": "Hiker", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "scoring_order": None},
    {"id": 56, "name": "Faceless Joker", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 57, "name": "Green Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 1, "m_add_mult": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_mult": 1}}},
    {"id": 58, "name": "Superposition", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 59, "name": "To Do List", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 60, "name": "Cavendish", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_mul_mult": 3}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 61, "name": "Card Sharp", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 3}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 62, "name": "Red Card", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 3, "m_add_mult": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_mult": 1}}},
    {"id": 63, "name": "Madness", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_active": {"b_mul_mult": 0.5, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 64, "name": "Square Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_chip": 4, "m_add_chip": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_chip": 1}}},
    {"id": 65, "name": "Seance", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 66, "name": "Riff-Raff", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 6, "scoring_order": None},
    {"id": 67, "name": "Vampire", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_active": {"b_mul_mult": 0.1, "m_mul_mult": 0, "a_mul_mult": 1.0}, "effect_passive": {"removes_enhancements": True}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 68, "name": "Shortcut", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_passive": {"straight_gap": True}, "scoring_order": None},
    {"id": 69, "name": "Hologram", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_active": {"b_mul_mult": 0.25, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 70, "name": "Vagabond", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "scoring_order": None},
    {"id": 71, "name": "Baron", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_mul_mult": 1.5}, "scoring_order": GAME_SCORING_ORDER_STID["held_hand"], "condition": {"card_rank": [CARD_RANK_STID["K"]]}},
    {"id": 72, "name": "Cloud 9", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "scoring_order": None},
    {"id": 73, "name": "Rocket", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 74, "name": "Obelisk", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_mul_mult": 0.2, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 75, "name": "Midas Mask", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_passive": {"face_cards_to_gold": True}, "scoring_order": None, "condition": {"card_rank": [CARD_RANK_STID["J"], CARD_RANK_STID["Q"], CARD_RANK_STID["K"]]}},
    {"id": 76, "name": "Luchador", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "scoring_order": None},
    {"id": 77, "name": "Photograph", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_mul_mult": 2.0}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["J"], CARD_RANK_STID["Q"], CARD_RANK_STID["K"]], "trigger_once": True}},
    {"id": 78, "name": "Gift Card", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 79, "name": "Turtle Bean", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 80, "name": "Erosion", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_add_mult": 4, "m_add_mult": "deck_below_default_count"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 81, "name": "Reserved Parking", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 6, "scoring_order": None},
    {"id": 82, "name": "Mail-In Rebate", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 83, "name": "To the Moon", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "scoring_order": None},
    {"id": 84, "name": "Hallucination", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 85, "name": "Fortune Teller", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 6, "effect_active": {"b_add_mult": 1, "m_add_mult": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_mult": 1}}},
    {"id": 86, "name": "Juggler", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 87, "name": "Drunkard", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "scoring_order": None},
    {"id": 88, "name": "Stone Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_add_chip": 25, "m_add_chip": "stone_card_deck_count"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 89, "name": "Golden Joker", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["common"], "cost": 6, "scoring_order": None},
    {"id": 90, "name": "Lucky Cat", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 0.25, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 91, "name": "Baseball Joker", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_passive": {"joker_uncommon_mul_multiplier": 1.5}, "scoring_order": None},
    {"id": 92, "name": "Bull", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_add_chip": 2, "m_add_chip": "dollar_count"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 93, "name": "Diet Cola", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 94, "name": "Trading Card", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 95, "name": "Flash Card", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "effect_active": {"b_add_mult": 2, "m_add_mult": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_mult": 1}}},
    {"id": 96, "name": "Popcorn", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 4, "m_add_mult": 5}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_mult": -1}}},
    {"id": 97, "name": "Spare Trousers", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_add_mult": 2, "m_add_mult": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_mult": 1}}},
    {"id": 98, "name": "Ancient Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_mul_mult": 1.5}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_suit": [CARD_SUIT_STID["S"]]}, "condition_variety": ["card_suit"]},
    {"id": 99, "name": "Ramen", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 0.01, "m_mul_mult": 0, "a_mul_mult": 2.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 100, "name": "Walkie Talkie", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_chip": 10, "b_add_mult": 4}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["4"], CARD_RANK_STID["10"]]}},
    {"id": 101, "name": "Seltzer", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"a_trigger": 1}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"]},
    {"id": 102, "name": "Castle", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_add_chip": 3, "m_add_chip": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_chip": 1}}},
    {"id": 103, "name": "Smiley Face", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 5}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["J"], CARD_RANK_STID["Q"], CARD_RANK_STID["K"]]}},
    {"id": 104, "name": "Campfire", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 9, "effect_active": {"b_mul_mult": 0.25, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 105, "name": "Golden Ticket", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "scoring_order": None},
    {"id": 106, "name": "Mr. Bones", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "scoring_order": None},
    {"id": 107, "name": "Acrobat", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 3.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 108, "name": "Sock and Buskin", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"a_trigger": 1}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["J"], CARD_RANK_STID["Q"], CARD_RANK_STID["K"]]}},
    {"id": 109, "name": "Swashbuckler", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"b_add_mult": 1, "m_add_mult": "other_jokers_sell_value"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 110, "name": "Troubadour", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 111, "name": "Certificate", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 112, "name": "Smeared Joker", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_passive": {"smeared_suits": True}, "scoring_order": None},
    {"id": 113, "name": "Throwback", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 0.25, "m_mul_mult": "skipped_blinds_count", "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 114, "name": "Hanging Chad", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 4, "effect_active": {"a_trigger": 2}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"trigger_once": True}},
    {"id": 115, "name": "Rough Gem", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "scoring_order": None},
    {"id": 116, "name": "Bloodstone", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_active": {"b_mul_mult": 1.5}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_suit": [CARD_SUIT_STID["H"]], "activate_probability": 1.0/2.0}},
    {"id": 117, "name": "Arrowhead", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_active": {"b_add_chip": 50}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_suit": [CARD_SUIT_STID["S"]]}},
    {"id": 118, "name": "Onyx Agate", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_active": {"b_add_mult": 7}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_suit": [CARD_SUIT_STID["C"]]}},
    {"id": 119, "name": "Glass Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 0.75, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 120, "name": "Showman", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 5, "scoring_order": None},
    {"id": 121, "name": "Flower Pot", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 3.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_suit": [[CARD_SUIT_STID["D"]], [CARD_SUIT_STID["H"]], [CARD_SUIT_STID["S"]], [CARD_SUIT_STID["C"]]], "played_hand_size_min": 4}},
    {"id": 122, "name": "Blueprint", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 10, "effect_active": {"copy_right": True}, "scoring_order": None},
    {"id": 123, "name": "Wee Joker", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_add_chip": 8, "m_add_chip": 0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_add_chip": 1}}},
    {"id": 124, "name": "Merry Andy", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "scoring_order": None},
    {"id": 125, "name": "Oops! All 6s", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 4, "effect_passive": {"double_probability": True}, "scoring_order": None},
    {"id": 126, "name": "The Idol", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 2.0}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_suit": [CARD_SUIT_STID["S"]], "card_rank": [CARD_RANK_STID["A"]]}, "condition_variety": ["card_suit", "card_rank"]},
    {"id": 127, "name": "Seeing Double", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "effect_active": {"b_mul_mult": 2.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_suit": [[CARD_SUIT_STID["C"]], [CARD_SUIT_STID["D"], CARD_SUIT_STID["H"], CARD_SUIT_STID["S"]]]}},
    {"id": 128, "name": "Matador", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "scoring_order": None},
    {"id": 129, "name": "Hit the Road", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_mul_mult": 0.5, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 130, "name": "The Duo", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_mul_mult": 2.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["pair"]}},
    {"id": 131, "name": "The Trio", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_mul_mult": 3.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["three_of_kind"]}},
    {"id": 132, "name": "The Family", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_mul_mult": 4.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["four_of_kind"]}},
    {"id": 133, "name": "The Order", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_mul_mult": 3.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["straight"]}},
    {"id": 134, "name": "The Tribe", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "effect_active": {"b_mul_mult": 2.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "condition": {"played_hand_contain_type": POKER_HANDS_STID["flush"]}},
    {"id": 135, "name": "The Stuntman", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 7, "effect_active": {"b_add_chip": 250}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 136, "name": "Invisible Joker", "affect_scoring": False, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "scoring_order": None},
    {"id": 137, "name": "Brainstorm", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 10, "effect_active": {"copy_mostleft": True}, "scoring_order": None},
    {"id": 138, "name": "Satellite", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 139, "name": "Shoot the Moon", "copy_compat": True, "rarity": JOKER_RARITY_STID["common"], "cost": 5, "effect_active": {"b_add_mult": 13}, "scoring_order": GAME_SCORING_ORDER_STID["held_hand"], "condition": {"card_rank": [CARD_RANK_STID["Q"]]}},
    {"id": 140, "name": "Driver's License", "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 7, "effect_active": {"b_mul_mult": 3.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 141, "name": "Cartomancer", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 6, "scoring_order": None},
    {"id": 142, "name": "Astromancer", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 8, "scoring_order": None},
    {"id": 143, "name": "Burnt Joker", "affect_scoring": False, "copy_compat": True, "rarity": JOKER_RARITY_STID["rare"], "cost": 8, "scoring_order": None},
    {"id": 144, "name": "Bootstraps", "copy_compat": True, "rarity": JOKER_RARITY_STID["uncommon"], "cost": 7, "effect_active": {"b_add_mult": 2, "m_add_mult": "dollar_count_div_five"}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"]},
    {"id": 145, "name": "Canio", "copy_compat": True, "rarity": JOKER_RARITY_STID["legendary"], "cost": 20, "effect_active": {"b_mul_mult": 1.0, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 146, "name": "Triboulet", "copy_compat": True, "rarity": JOKER_RARITY_STID["legendary"], "cost": 20, "effect_active": {"b_mul_mult": 2.0}, "scoring_order": GAME_SCORING_ORDER_STID["played_hand"], "condition": {"card_rank": [CARD_RANK_STID["Q"], CARD_RANK_STID["K"]]}},
    {"id": 147, "name": "Yorick", "copy_compat": True, "rarity": JOKER_RARITY_STID["legendary"], "cost": 20, "effect_active": {"b_mul_mult": 1.0, "m_mul_mult": 0, "a_mul_mult": 1.0}, "scoring_order": GAME_SCORING_ORDER_STID["owned_jokers"], "upgrade": {"effect_active": {"m_mul_mult": 1}}},
    {"id": 148, "name": "Chicot", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["legendary"], "cost": 20, "scoring_order": None},
    {"id": 149, "name": "Perkeo", "affect_scoring": False, "copy_compat": False, "rarity": JOKER_RARITY_STID["legendary"], "cost": 20, "scoring_order": None}
]
JOKERS_STID={
    
}