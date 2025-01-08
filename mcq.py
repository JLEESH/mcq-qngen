import os
import sys
import argparse

DEFAULT_FLENAME = 'questions.json'
TRACK_SCORE = True

format2qn = {
                "simple": lambda x: f"What is the meaning of {x}?",
                "synonym" : lambda x: f"What is a synonym for {x}?",
                "antonym" : lambda x: f"What is an antonym for {x}?"
            }

ans2char = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}

# UUID generator
def generate_uuid():
    """
        Generate a UUID.
    """
    
    import uuid
    
    return str(uuid.uuid4())

# read json file
def read_question(file, filetype='json'):
    """
        Read a question file and return the data.
    """

    import json
    
    if filetype != 'json':
        raise NotImplementedError
    
    with open(file, 'r') as f:
        data = json.load(f)
    
    return data

def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', type=str, default=DEFAULT_FLENAME, help='Filename of the question file.')
    parser.add_argument('--generate-uuid', '-g', action='store_true', default=False, help='Generate a UUID.') # generate uuid and exit
    parser.add_argument('--no-score-track', '-n', action='store_true', default=False, help='Turn off score tracking.')
    args = parser.parse_args()

    # generate UUID and exit
    # note: quick functionality that has nothing to do with the main program
    if args.generate_uuid:
        uuid = generate_uuid()
        print(uuid)
        sys.exit(0)

    # decide whether to track score
    global TRACK_SCORE
    TRACK_SCORE = args.no_score_track == False

    # set up the quiz
    filename = args.filename
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File ``{filename}`` not found.")
    
    data = read_question(filename)
    score = 0

    # start the quiz
    #for (qindex, question) in data.items(): # if data is a dict
    for qindex, question in enumerate(data): # if data is a list

        # clear screen for next question
        # TODO: think of a better way to decrease clutter
        os.system('clear')

        # TODO: generate formatted question
        qn_str = format2qn[question['question-type']](question['question'])
        print(f"Question {qindex+1}: {qn_str}")
        print(f"Options: ")

        for oi, option in enumerate(question['options']):
            print(f"{ans2char[oi]}. {option}")
        print()

        # optionally add score tracking
        if TRACK_SCORE:
            score_str = f"Current score: {score}/{qindex}" # strings garbage collected?
            print(score_str)
        
        # process user input
        # TODO: improve user experience... too many ENTER presses
        ans = input()
        if ans2char[question['answer']] == ans.upper():
            print("Correct!")
            print(f"Answer: {ans2char[question['answer']]}, {question['options'][question['answer']]}")
            score += 1 # increase score
        elif ans == 'q':
            print("Quitting...")
            break
        else:
            print("Incorrect!")
            print(f"Answer: {ans2char[question['answer']]}, {question['options'][question['answer']]}")
        input("Press Enter to continue...")

    print(f"Final score: {score}/{qindex+1}")

if __name__ == "__main__":
    main()