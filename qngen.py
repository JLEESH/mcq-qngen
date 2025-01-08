from openai import OpenAI

oa_key = None # replace with caution

PROTECT_QN_FILE = True # may be modified by main()
DUMMY_RESPONSE_PATH = "sample_responses/dummy_response"
DEFAULT_RESP_PATH = "./" # not used
DEFAULT_QN_PATH = "./" # not used

# edit prompt as needed.
QNGEN_SYSTEM_PROMPT = """
    You are a tool to create high-quality JSON files for quizzes e.g. a vocabulary quiz.
    Each question must adhere to the following JSON format:
    
    {
        \"id\": "e2212784-4dea-454b-ac23-442e815c218f",     // UUID
        \"_comments\": ["internal-index: 0"],               // Internal index and other miscellaneous comments
        \"question-type\": \"simple\",
        \"question\": [\"Question word\"],
        \"options\": [\"Option 1\", \"Option 2\", \"Option 3\", \"Option 4\"],
        \"options-alt-list\": [[\"Alt 1\", \"Alt 2\", \"Alt 3\", \"Alt 4\"],
                                [\"Alt-2 1\", \"Alt-2 2\", \"Alt-2 3\", \"Alt-2 4\"]],
        \"answer\": 0,                                      //Index of correct answer
        \"answer-alt\": [0, 0]                              // Index of correct answer in alternative lists
    }

    Instructions:
    - Generate the required number of questions for the given task e.g. testing Vietnamese vocabulary.
    - Use a mix of questions of simple and intermediate difficulty e.g. vocabulary of different levels.
    - Provide plausible distractors for all answer options.
    - Ensure high-quality, educationally sound options.
    - Ensure an even mixture of the answer indices.

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

    Generate output as a valid JSON structure.
"""

# edit prompt to change number of questions etc.
nQuestions = 10
QNGEN_USER_PROMPT = f"{nQuestions} questions of Vietnamese. "\
    "Easy native Vietnamese words and intermediate to advanced Sino-Vietnamese words "\
    "for learners with a background in both English, Chinese and Japanese."

def generate_questions(oa_key=oa_key, dummy=False):
    if dummy:
        return generate_response(QNGEN_SYSTEM_PROMPT, QNGEN_USER_PROMPT, oa_key=oa_key, dummy=True)
    
    return generate_response(QNGEN_SYSTEM_PROMPT, QNGEN_USER_PROMPT, oa_key=oa_key)

def generate_response(system_text, user_text, oa_key=oa_key, dummy=False):
    if dummy:
        return load_response_var(DUMMY_RESPONSE_PATH)
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
    
    filecontent = response.choices[0].message.content[8:-3] # remove "```json\n" and "```" from the response

    with open(filename, "w") as f:
        f.write(filecontent)

    # save questions to ``questions.json``
    import os
    if os.path.exists("questions.json") and PROTECT_QN_FILE == True:
        # raise FileExistsError("WARNING: -d was not passed (questions.json is protected) \
        #     and ``questions.json`` already exists. \
        #     Please move or delete the file.\n\
        #     Continuing without overwriting... (``questions_<UUID>.json`` is still saved.)"

        # print warning instead of raising an error, for now
        print("WARNING: -d was not passed (questions.json is protected) and ``questions.json`` already exists.\nPlease move or delete the file.\nContinuing without overwriting... (``questions_<UUID>.json`` is still saved.)")
        return
    
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
    parser.add_argument("--path-question", "-q",
                        dest="QN_PATH",
                        type=str,
                        default=DEFAULT_QN_PATH,
                        help="Set path to save the questions to (unimplemented).")
    parser.add_argument("--path-response", "-r",
                        dest="RESP_PATH",
                        type=str,
                        default=DEFAULT_RESP_PATH,
                        help="Set path to save the responses to (unimplemented).")
    parser.add_argument("--dummy", "-D", action="store_true", default=False, help="Run in dummy mode.")
    args = parser.parse_args()
    global PROTECT_QN_FILE
    PROTECT_QN_FILE = args.DNP == False
    M_GEN_RES_SAVE = args.GEN_RES_SAVE
    DUMMY = args.dummy
    QN_PATH = args.QN_PATH.strip()
    RESP_PATH = args.RESP_PATH.strip()
    
    import os
    if os.path.exists(QN_PATH) == False:
        os.makedirs(QN_PATH)
    if os.path.exists(RESP_PATH) == False:
        os.makedirs(RESP_PATH)
    
    # load .env file to obtain OpenAI API key
    from dotenv import load_dotenv

    load_dotenv()
    oa_key = os.getenv("OPENAI_API_KEY")
    if oa_key == None:
        raise ValueError("Main: OpenAI API key is not set.")

    # obtain response
    print("Attempting to obtain a response...")
    response = generate_questions(oa_key, dummy=DUMMY)
    print("Respose obtained.")

    # save response to file
    import uuid
    file_uuid = str(uuid.uuid4())
    if DUMMY:
        file_uuid = "dummy_" + file_uuid
    filename_var = RESP_PATH + f"response_{file_uuid}.txt"
    filename_text = RESP_PATH + f"response_text_{file_uuid}.txt"
    filename_content_text = RESP_PATH + f"response_content_text_{file_uuid}.txt"

    if M_GEN_RES_SAVE:
        save_response_var(response, id=file_uuid, filename=filename_var)
        save_response_text(response, id=file_uuid, filename=filename_text)
        save_response_content_text(response, id=file_uuid, filename=filename_content_text)

    # save questions to file
    save_questions(response, id=file_uuid, filename=QN_PATH + f"questions_{file_uuid}.json")
    
    return response

if __name__ == "__main__":
    main()