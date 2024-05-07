import os
import spacy
from spacy.matcher import PhraseMatcher
from dotenv import load_dotenv

# Load English tokenizer, tagger, parser, and NER
nlp = spacy.load("en_core_web_sm")

from utils import (
    BaseLogger,
)
from chains import (
    load_llm,
    configure_llm_only_chain,

)
load_dotenv(".env")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
embedding_model_name = os.getenv("EMBEDDING_MODEL")
llm_name = os.getenv("LLM")
llm = load_llm(
    llm_name, logger=BaseLogger(), config={"ollama_base_url": ollama_base_url}
)

llm_chain = configure_llm_only_chain(llm)

PROMPT = """
YOu need to answer me with below knowledge on question bank I have provideded you with 5batch of  questions which I provided below, form that list I will give my user input question you need to suggest me which is the nearest question bank that matched to my user question your response should be simple like 
question2
(Above only give question2 as your response nothing else)

Below is my question bank:
{0}

Below is my user question please match a question from the bank and respond in the format I asked previously
User Question: {1}

NOTE: If any Question did not matched then your output will be:
None
"""
# Define the questions
question_mappings = {
    "question1": [
        "give me available data",
        "show available data",
        "what data is available?",
        "list available data",
        "display available data",
        "available data",
        "data available"
    ],
    "question2": [
        "i would like to add more data to jewish community",
        "I want to upload sources of interest",
        "add data to jewish community",
        "insert data for jewish community",
        "update jewish community data",
        "append data to jewish community",
        "add more jewish community data",
        "expand jewish community data",
        "add data"  # New variation added here
    ],
    "question3": [
        "what dates of interest are available in the ontology?",
        "available dates in the ontology?",
        "list dates of interest in the ontology",
        "display ontology dates of interest",
        "dates of interest in ontology",
        "ontology dates of interest"
    ],
    "question4": [
        "what reference threats are available in the ontology?",
        "available reference threats?",
        "list reference threats in the ontology",
        "display ontology reference threats",
        "reference threats in ontology",
        "ontology reference threats"
    ],
     "question5": [
        "show on the map routes of garbage collection",
        "display garbage collection routes on the map",
        "map garbage collection routes",
        "visualize garbage collection routes",
        "garbage collection routes on map",
        "plot garbage collection routes"
    ],
    "question6": [
        "convert container to incident",
        "change container to incident",
        "transform container to incident",
        "convert container into incident",
        "container to incident conversion"
    ],
    "question7": [
        "find similar posts",
        "search for similar posts",
        "locate similar posts",
        "retrieve similar posts",
        "discover similar posts",
        "identify similar posts"
    ],
    "question8": [
        "add a note that the event in Orrong and Glen Eiira was performed by a municipality worker, claiming he was mapping out routes for garbage disposal",
        "include note about Orrong and Glen Eiira event involving municipality worker mapping garbage disposal routes",
        "append note regarding Orrong and Glen Eiira incident with municipality worker and garbage disposal route mapping",
        "attach note to Orrong and Glen Eiira event involving municipality worker mapping garbage disposal routes"
    ],
    "question9": [
        "show on the map recent property crimes in the area",
        "display recent property crimes on map",
        "map recent property crimes in the vicinity",
        "visualize recent property crimes on map",
        "plot recent property crimes in the area"
    ],
    "question10": [
        "decrease general crime reference risk value by two with a reason of minor correlation to property crime in the area",
        "lower general crime reference risk by two due to slight connection to local property crime",
        "reduce general crime reference risk score by two because of minor association with property crime in the region",
        "decrease general crime risk rating by two points due to minor correlation with property crime nearby"
    ],
    "question11": [
        "show me patterns of hate speech in the past three months in the area",
        "display hate speech patterns over the last three months in the vicinity",
        "visualize hate speech trends in the area for the past three months",
        "plot hate speech patterns in the vicinity over the past three months"
    ],
    "question12": [
        "decrease hate crime reference risk value to two with a reason of insignificant change in hate speech in the past 3 months",
        "lower hate crime reference risk by two due to insignificant change in hate speech over the past three months",
        "reduce hate crime reference risk score by two because of no significant variation in hate speech in the last three months",
        "decrease hate crime risk rating by two points due to lack of significant change in hate speech over the past three months"
    ],
    "question13": [
        "close this incident",
        "mark this incident as closed",
        "resolve this incident",
        "finish this incident",
        "end this incident"
    ],
    "question14": [
        "based on my investigation, it is most likely the reported sightings of suspicious photography are related to neutral municipal activities",
        "conclude from investigation that reported suspicious photography sightings are linked to neutral municipal activities",
        "determine through investigation that sightings of suspicious photography likely involve neutral municipal activities",
        "find from investigation that reported sightings of suspicious photography are probably related to neutral municipal activities"
    ],
    "question15": [
        "perform linguistic analysis on the post",
        "analyze the language used in the post",
        "conduct linguistic analysis of the post",
        "examine the linguistic aspects of the post"
    ],
    "question16": [
        "convert notification to alert",
        "change notification to alert",
        "transform notification into alert",
        "modify notification to alert"
    ],
    "question17": [
        "upload new sources of interest",
        "add new sources of interest",
        "update sources of interest",
        "submit additional sources of interest"
    ],
    "question18": [
        "merge both incidents and elevate risk level for the incidents and of person of interest",
        "combine both incidents and raise the risk level for them and the person of interest",
        "merge the incidents and increase the risk level for both incidents and the person of interest",
        "consolidate both incidents and escalate the risk level for them and the person of interest"
    ],
    "question19": [
        "convert incident to Case",
        "transform incident into Case",
        "change incident to Case",
        "turn incident into Case"
    ],
    "question20": [
        "show on the map routes of garbage collection in the JC polygon"
    ],
    "question21": [
        "More posts from author"
    ]
}

# Combine all questions into a single list for matching
all_questions = [question for sublist in question_mappings.values() for question in sublist]

# Process the questions with spaCy
questions_docs = [nlp(question) for question in all_questions]

# Create a PhraseMatcher and add the questions as patterns
matcher = PhraseMatcher(nlp.vocab)
for question in questions_docs:
    matcher.add("Question", [question])

# Function to detect the nearest match and return the corresponding question number
def detect_question(query):
    # Process the input query with spaCy
    doc = nlp(query)
    
    # Find matches and near matches
    matches = matcher(doc)
    near_matches = []

    for token in doc:
        if token.is_alpha and not token.is_stop:
            for question_doc in questions_docs:
                similarity = token.similarity(question_doc)
                # print("similarity", similarity)
                if similarity > 0.7:  # Adjust the similarity threshold as needed
                    near_matches.append((token.text, question_doc.text))

    # Check if there's a direct match
    if matches:
        match_id, start, end = matches[0]
        span = doc[start:end]
        matched_question = span.text
    else:
        matched_question = None

    # If no direct match, return the nearest match
    if not matched_question and near_matches:
        _, matched_question = near_matches[0]

    # Find the question number corresponding to the matched question
    question_number = None
    for key, value in question_mappings.items():
        if matched_question in value:
            question_number = key
            break

    # If no question number found, return None
    return question_number


def detect_question_llm(question):
    print("No Question Detatcted Calling LLM")
    user_prompt = PROMPT.format(str(question_mappings),question)
    print("PROMPT to LLM")
    # print(user_prompt)
    result = llm_chain({"question": user_prompt, "chat_history": []}, callbacks=[])
    print(result["answer"])

    return result["answer"]

# Example usage
# input_query = "Add a note that the event in Orrong and Glen Eiira was a performed by a municipality worker, claiming he was mapping out routes for garbage disposal, and increase neutral base assumption value by one with a reason of related to garbage disposal route mapping"
# matched_question_number = detect_question(input_query)
# print("Matched question number:", matched_question_number)
# print("Now LLM response")


# matched_question_number = detect_question_llm(input_query)
# print("Matched question number:", matched_question_number)