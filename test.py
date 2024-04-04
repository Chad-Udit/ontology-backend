# Define patterns for each question
import re


patterns = {
    "question1": [
        r"\b(?:give|show|display|list|available) data\b"
    ],
    "question2": [
        r"\b(?:add|insert|update|append) data(?: to)? jewish community\b",
        r"\b(?:add|insert|update|append) data\b"  # For the shortened version
    ],
    "question3": [
        r"\b(?:dates|days) of interest\b",
        r"\b(?:available|list|display) dates(?: of interest)?(?: in the ontology)?\b"
    ],
    "question4": [
        r"\b(?:reference|available|list|give) threats(?: in the ontology)?\b"
    ]
}

def match_intent(query):
    # Iterate over patterns and check for matches
    for question_id, question_patterns in patterns.items():
        for pattern in question_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return question_id
    return None

print(match_intent('list threats'))
