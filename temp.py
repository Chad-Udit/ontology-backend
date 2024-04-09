import spacy
from spacy.matcher import PhraseMatcher

# Load English tokenizer, tagger, parser, and NER
nlp = spacy.load("en_core_web_sm")

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

# Example usage
# input_query = "update data"
# matched_question_number = detect_question(input_query)
# print("Matched question number:", matched_question_number)
