from openai import OpenAI

oa_key = None # replace with caution

PROTECT_QN_FILE = True

# edit prompt as needed.
QNGEN_SYSTEM_PROMPT = """
    You are a tool to create high-quality JSON files for quizzes e.g. a vocabulary quiz.
    Each question must adhere to the following JSON format:
    
    {
        \"id\": "e2212784-4dea-454b-ac23-442e815c218f",
        \"_comments\": ["internal-index: 0"],
        \"question-type\": \"simple\",
        \"question\": [\"Question word\"],
        \"options\": [\"Option 1\", \"Option 2\", \"Option 3\", \"Option 4\"],
        \"options-alt-list\": [[\"Alt 1\", \"Alt 2\", \"Alt 3\", \"Alt 4\"],
                                [\"Alt-2 1\", \"Alt-2 2\", \"Alt-2 3\", \"Alt-2 4\"]],
        \"answer\": 0,  # Index of correct answer
        \"answer-alt\": [0, 0]  # Index of correct answer in alternative lists
    }

    Instructions:
    - Generate the required number of questions for the given task e.g. testing Vietnamese vocabulary.
    - Use a mix of questions of simple and intermediate difficulty e.g. vocabulary of different levels.
    - Provide plausible distractors for all answer options.
    - Ensure high-quality, educationally sound options.
    - Ensure an even mixture of the indices of correct answers.

    Example Question for a Vienamese vocabulary quiz:
    {
        \"id\": 0,
        \"_comments\": ["internal-index: 0"],
        \"question-type\": \"simple\",
        \"question\": [\"chó\"],
        \"options\": [\"Cat\", \"Dog\", \"Bird\", \"Fish\"],
        \"options-alt-list\": [[\"Mèo\", \"Chó\", \"Chim\", \"Cá\"],
                                [\"猫\", \"犬\", \"鳥\", \"魚\"]],
        \"answer\": 1,
        \"answer-alt\": [1, 1]
    }
    "        "Generate output as a valid JSON structure."
"""
# edit prompt to change number of questions etc.
nQuestions = 10
QNGEN_USER_PROMPT = f"{nQuestions} question of Vietnamese. \
    Easy native Vietnamese words and intermediate to advanced \
    Sino-Vietnamese words for learners with a background in both English, Chinese and Japanese."

def generate_response(system_text, user_text, oa_key=oa_key):
    if oa_key == None:
        raise ValueError("OpenAI API key is not set.")
    
    client = OpenAI(api_key=oa_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": QNGEN_SYSTEM_PROMPT
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": QNGEN_USER_PROMPT
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=1,
        max_completion_tokens=2048, # modify?
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response

def save_questions(response, id=None, filename=None):
    if filename == None:
        if id == None:
            import uuid
            filename = f"questions_{uuid.uuid4()}.json"
        else:
            filename = f"questions_{id}.json"
    
    filecontent = response.choices[0].message.content[8:-3]

    with open(filename, "w") as f:
        f.write(filecontent)

    # save questions to a set file as well
    # check if file already exists
    import os
    if os.path.exists("questions.json") and PROTECT_QN_FILE == True:
        # raise FileExistsError("WARNING: -d was not passed (questions.json is protected) \
        #     and ``questions.json`` already exists. \
        #     Please move or delete the file.\n\
        #     Continuing without overwriting... (``questions_<UUID>.json`` is still saved.)"
        print("WARNING: -d was not passed (questions.json is protected) and ``questions.json`` already exists.\nPlease move or delete the file.\nContinuing without overwriting... (``questions_<UUID>.json`` is still saved.)")

        with open("questions.json", "w") as f:
            f.write(filecontent)

def save_response_text(response, id=None, filename=None):
    if filename == None:
        if id == None:
            filename = "response_text.txt"
        else:
            filename = f"response_text_{id}.txt"
    
    with open(filename, "w") as f:
        f.write(repr(response))

def save_response_var(response, id=None, filename=None):
    import pickle

    if filename == None:
        if id == None:
            filename = "response.txt"
        else:
            filename = f"response_{id}.txt"
    
    with open(filename, "wb") as f:
        pickle.dump(response, f)

def load_response_var(filename):
    if filename == None:
        raise ValueError("load_response_var: filename is None.")
    
    import pickle
    try:
        with open(filename, "rb") as f:
            loaded_response = pickle.load(f)
        return loaded_response
    except FileNotFoundError as e:
        print(f"WARNING: load_response_var: File not found: {filename}")
        return None

def save_response_content_text(response, id=None, filename=None):
    if filename == None:
        if id == None:
            filename = "response_content_text.txt"
        else:
            filename = f"response_content_text_{id}.txt"
    
    with open(filename, "w") as f:
        f.write(response.choices[0].message.content)

def generate_questions(oa_key=oa_key):
    return generate_response(QNGEN_SYSTEM_PROMPT, QNGEN_USER_PROMPT, oa_key=oa_key)

def main():
    # process args
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--do-not-protect-qn-file", "-d",
                       dest="DNP",
                       action="store_true",
                       default=False,
                       help="Allow ``questions.json`` to be overwritten.")
    parser.add_argument("--generated-response-save", "-g",
                       dest="GEN_RES_SAVE",
                       action="store_true",
                       default=False,
                       help="Save generated responses.")
    args = parser.parse_args()
    global PROTECT_QN_FILE
    PROTECT_QN_FILE = args.DNP == False
    M_GEN_RES_SAVE = args.GEN_RES_SAVE
    
    # load .env file to obtain OpenAI API key
    import os
    from dotenv import load_dotenv

    load_dotenv()
    oa_key = os.getenv("OPENAI_API_KEY")
    if oa_key == None:
        raise ValueError("Main: OpenAI API key is not set.")

    # obtain response
    print("Attempting to obtain a response...")
    response = generate_questions(oa_key)
    print("Respose obtained.")

    # save response to file
    import uuid
    file_uuid = str(uuid.uuid4())
    filename_var = f"response_{file_uuid}.txt"
    filename_text = f"response_text_{file_uuid}.txt"
    filename_content_text = f"response_content_text_{file_uuid}.txt"

    if M_GEN_RES_SAVE:
        save_response_var(response, id=file_uuid)
        save_response_text(response, id=file_uuid)
        save_response_content_text(response, id=file_uuid)

    # save questions to file
    save_questions(response, id=file_uuid)
    
    return response

if __name__ == "__main__":
    main()