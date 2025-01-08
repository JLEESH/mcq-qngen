# MCQ and QNGEN

Question generation for learning.

# Explanation

## mcq.py:

``mcq.py`` - Go through generated questions.

Use ``files/questions.json``, ``files/qn-re-1401.json`` or output from ``qngen.py``.

## qngen.py:

``qngen.py`` - Generate questions.

Note: put OpenAI API key in ``.env`` as ``OPENAI_API_KEY``.

e.g. ``echo "OPEN_AI_KEY=<your-key-here>" > .env``

# Examples


## mcq.py:
``python mcq.py -f files/questions.json`` - Start a short quiz.

``python mcq.py -nf files/questions.json`` - Turn off score tracking during quiz (still shows final score).

## qngen.py: 
``python qngen.py`` - Obtains and generates response files in the same directory.

Note: some minimal changes to the response file may be necessary.