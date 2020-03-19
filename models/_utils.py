import re, hashlib
from random import random

TIME_REGEX = re.compile(
    r'(\D*(?P<hours>\d+)\s*(hour|hours|hrs|hr|h|Hour|Hours|H))*(\D*(?P<minutes>\d+)\s*(minute|minutes|mins|min|m|Minute|Minutes|M))*'
)

def hash_password(password, salt):
    hashed_pw = hashlib.sha512(password.encode() + salt).hexdigest()
    return hashed_pw

def generate_token():
    seed = str(random())
    return hashlib.sha256(seed.encode()).hexdigest()[:32]

def time_step(instruction): # Time to do step in instruction in seconds
    # Time to do action and whether you have to be actively doing the step or 
    # if you can passively do the step.
    # The action is the keyword and how long it takes to do the action is the 
    # value, if the value is 0, you can passively do the step. 
    # i.e. Boiling vs. Whisking
    # You can move on to another step while boiling something, but you have
    # to constantly whisk.
    cooking_verbs = {"add"     : 20,
                     "arrange" : 120,
                     "beat"    : 120,
                     "break"   : 60,
                     "carve"   : 180,
                     "cook"    : 300,
                     "cut"     : 300,
                     "dust"    : 20,
                     "fold"    : 600,
                     "frost"   : 300,
                     "fry"     : 300,
                     "grate"   : 60,
                     "grease"  : 120,
                     "heat"    : 60,
                     "mash"    : 60,
                     "melt"    : 120,
                     "mix"     : 180,
                     "place"   : 30,
                     "pulse"   : 90,
                     "pour"    : 30,
                     "roll"    : 600,
                     "reduce"  : 300,
                     "roast"   : 0,
                     "rub"     : 300,
                     "sear"    : 300,
                     "sit"     : 0,
                     "slice"   : 300,
                     "spread"  : 180, 
                     "sprinkle": 30,
                     "stir"    : 60,
                     "strain"  : 300,
                     "toast"   : 600,
                     "top"     : 60,
                     "toss"    : 60,
                     "trim"    : 120,
                     "whisk"   : 60
                    }
    dependency_word = "immediately"
    seconds = 0
 
    # If the sentence tells you how many hours or minutes to do 
    # the step, time to do the action described in the sentence
    # will be that specified time. Else it will be guessed from 
    # the verbs in the sentence

    # Separate each sentence in the instruction. 
    instruction = instruction.split(".")
    # Analyze each sentence in instruction. Remember, instruction is actually
    # just one step in the full list of instructions
    for sentence in instruction:
        # The regex statement will only detect one instance of minutes or hours.
        # Assume each step in the instructions describes time once in each 
        # sentence.
        if "minute" in sentence or "hour" in sentence:
            # Sometimes the times is separated by a dash, we don't want that
            sentence = re.split('–|-\+', sentence)
            for portion in instruction:
                matched = TIME_REGEX.search(portion)
                seconds += 60 * int(matched.groupdict().get('minutes') or 0)
                seconds += 3600 * int(matched.groupdict().get('hours') or 0)
        # If the step does not tell you how long it will take, guess
        # from the verbs used in the sentence.
        else:
            for word in sentence.split():
                if word in cooking_verbs.keys():
                    seconds += cooking_verbs[word.lower()]
    return seconds    