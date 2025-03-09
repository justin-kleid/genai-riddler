# puzzle class and puzzles list
class Puzzle:
    def __init__(self, id, question, answer, context, difficulty=1):
        self.id = id
        self.question = question
        self.answer = answer
        self.context = context
        self.difficulty = difficulty  # (1: easy, 2: medium,3: hard)

puzzles = [
    Puzzle(
        1,
        "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        "echo",
        "A riddle about something intangible that relies on sound and wind.",
        1
    ),
    Puzzle(
        2,
        "The more you take, the more you leave behind. What am I?",
        "footsteps",
        "A riddle that hints at something you leave behind as you move.",
        1
    ),
    Puzzle(
        3,
        "I have keys but no locks, space but no rooms. You can enter, but you can't go outside. What am I?",
        "keyboard",
        "A riddle involving something that has keys and space, yet isn't a traditional room.",
        1
    ),
    Puzzle(
        4,
        "What has a heart that doesn't beat?",
        "artichoke",
        "A riddle playing on the double meaning of 'heart', as in the center of something.",
        2
    ),
    Puzzle(
        5,
        "What can travel around the world while staying in a corner?",
        "stamp",
        "A riddle about an object that stays in one corner but is found all over the world.",
        1
    ),
    # Added more diverse riddles
    Puzzle(
        6,
        "I'm light as a feather, yet the strongest person can't hold me for more than a few minutes. What am I?",
        "breath",
        "A riddle about something essential yet impossible to physically hold for long.",
        2
    ),
    Puzzle(
        7,
        "I am taken from a mine, and shut up in a wooden case, from which I am never released, and yet I am used by almost every person. What am I?",
        "pencil lead",
        "A riddle about a common writing implement and its components.",
        2
    ),
    Puzzle(
        8,
        "What has roots that nobody sees, is taller than trees, up, up it goes, and yet never grows?",
        "mountain",
        "A riddle about a natural formation with metaphorical roots and height.",
        2
    ),
    Puzzle(
        9,
        "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?",
        "map",
        "A riddle about something that represents real features without containing them.",
        2
    ),
    Puzzle(
        10,
        "The person who makes it, sells it. The person who buys it, never uses it. The person who uses it, never sees it. What is it?",
        "coffin",
        "A riddle with a somber topic about an item used only after death.",
        3
    ),
    Puzzle(
        11,
        "I'm found in socks, scarves, and mittens; and often in the paws of playful kittens. What am I?",
        "yarn",
        "A riddle about a common crafting material used in various items.",
        1
    ),
    Puzzle(
        12,
        "Until I am measured, I am not known. Yet how you miss me, when I have flown. What am I?",
        "time",
        "A riddle about an abstract concept that we track and value.",
        2
    ),
    Puzzle(
        13,
        "What building has the most stories?",
        "library",
        "A play on words riddle about a building that contains many books.",
        1
    ),
    Puzzle(
        14,
        "Forward I am heavy, but backward I am not. What am I?",
        "ton",
        "A wordplay riddle where the word spelled backward changes the meaning.",
        2
    ),
    Puzzle(
        15,
        "The more you take away from me, the larger I become. What am I?",
        "hole",
        "A riddle about something that grows larger when material is removed from it.",
        2
    ),
    Puzzle(
        16,
        "I am always hungry and will die if not fed, but whatever I touch will soon turn red. What am I?",
        "fire",
        "A riddle about an element that consumes fuel and changes the color of what it burns.",
        2
    ),
    Puzzle(
        17,
        "I can be cracked, made, told, and played. What am I?",
        "joke",
        "A riddle using different verbs that can be applied to the answer.",
        1
    ),
    Puzzle(
        18,
        "What goes up but never comes down?",
        "age",
        "A riddle about something that only increases over time.",
        1
    ),
    Puzzle(
        19,
        "I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
        "fire",
        "A riddle about something that exhibits life-like qualities but isn't alive.",
        2
    ),
    Puzzle(
        20,
        "What runs around the whole yard without moving?",
        "fence",
        "A riddle about a stationary object that surrounds an area.",
        1
    )
]
# Utility functions to get puzzles
def get_random_puzzles(exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []
    
    return [puzzle for puzzle in puzzles if puzzle.id not in exclude_ids]

# cuttable, not a feature that rlly ended up in use
def get_puzzles_by_difficulty(difficulty_level):
    return [puzzle for puzzle in puzzles if puzzle.difficulty == difficulty_level]