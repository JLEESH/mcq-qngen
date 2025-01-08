# TODO's: 

## Misc.
cf. Source files.

## Ease of Use
Maybe make it such that the user can

1. run ``qngen.py`` (for a new set of questions, formatted and placed into the right path)
2. run ``mcq.py`` to solve the latest batch of questions
3. ???
4. \<imagine...\>

We could combine both files or make a mini-library, but that would be for the iteration after that.

(partially done)

## Web Version
(hmm..., simpe node server -> host a html with a js script to read and display generated questions? dynamically generate questions? -> need to keep track of cost and abuse, or pre-generate a number of questions and segment into short batches -> selection menu, etc.)

## Question Quality
Improve the quality of questions.

Some issues:
1. Shuffle the options manually as the API responses have an overwhelmingly larger share of 'A' being the answer.
2. Repetition of questions - Flexibility in not repeating questions that have already been generated.
3. Question types - increase the diversity of question types.
4. TBD

