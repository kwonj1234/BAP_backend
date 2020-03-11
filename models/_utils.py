import re

TIME_REGEX = re.compile(
    r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H))*(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M))*'
)

def time_step(instruction): # Time to do action in seconds
    cooking_verbs = {"add"   : 20,
                     "arrange" : 120,
                     "beat"  : 120,
                     "break" : 60,
                     "carve" : 180,
                     "cook"  : 300,
                     "cut"   : 300,
                     "dust"  : 20,
                     "fold"  : 600,
                     "frost" : 300,
                     "fry"   : 300,
                     "grate" : 60,
                     "grease": 120,
                     "heat"  : 60,
                     "melt"  : 120,
                     "mix"   : 180,
                     "place" : 15,
                     "pour"  : 30,
                     "roll"  : 600,
                     "reduce": 300,
                     "rub"   : 300,
                     "sear"  : 300,
                     "slice" : 300,
                     "spread": 180, 
                     "sprinkle" : 60,
                     "stir"  : 20,
                     "strain": 300,
                     "toast" : 600,
                     "top"   : 60,
                     "toss"  : 60,
                     "trim"  : 120,
                     "whisk" : 20
                     }      
    seconds = 0

    for sentence in instruction.split('.'): 
        # If the sentence tells you how many hours or minutes to do 
        # the step, time to do the action described in the sentence
        # will be that specified time. Else it will be guessed from 
        # the verbs in the sentence

        # Find the numbers preceding instances of "hours" and "minutes"
        matched = TIME_REGEX.search(sentence)

        # If the step does not tell you how long it will take, guess
        # from the verbs used in the sentence.
        if matched.groupdict().get('minutes') is None and matched.groupdict().get('hours') is None:
            
            for word in sentence.split():
                if word in cooking_verbs.keys():
                    seconds += cooking_verbs[word.lower()]

        else:
            seconds += 60 * int(matched.groupdict().get('minutes') or 0)
            seconds += 3600 * int(matched.groupdict().get('hours') or 0)

    return seconds    