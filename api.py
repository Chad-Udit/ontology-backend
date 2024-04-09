import os
import re

from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
from utils import (
    create_vector_index,
    BaseLogger,
)
from chains import (
    load_embedding_model,
    load_llm,
    configure_llm_only_chain,
    configure_qa_rag_chain,
    generate_ticket,
)
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from langchain.callbacks.base import BaseCallbackHandler
from threading import Thread
from queue import Queue, Empty
from collections.abc import Generator
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from temp import detect_question
load_dotenv(".env")

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
embedding_model_name = os.getenv("EMBEDDING_MODEL")
llm_name = os.getenv("LLM")
# Remapping for Langchain Neo4j integration
os.environ["NEO4J_URL"] = url

embeddings, dimension = load_embedding_model(
    embedding_model_name,
    config={"ollama_base_url": ollama_base_url},
    logger=BaseLogger(),
)

# if Neo4j is local, you can go to http://localhost:7474/ to browse the database
neo4j_graph = Neo4jGraph(url=url, username=username, password=password)
create_vector_index(neo4j_graph, dimension)

llm = load_llm(
    llm_name, logger=BaseLogger(), config={"ollama_base_url": ollama_base_url}
)

llm_chain = configure_llm_only_chain(llm)
rag_chain = configure_qa_rag_chain(
    llm, embeddings, embeddings_store_url=url, username=username, password=password
)


class QueueCallback(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to a queue."""

    def __init__(self, q):
        self.q = q

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.q.put(token)

    def on_llm_end(self, *args, **kwargs) -> None:
        return self.q.empty()


def stream(cb, q) -> Generator:
    job_done = object()

    def task():
        x = cb()
        q.put(job_done)

    t = Thread(target=task)
    t.start()

    content = ""

    # Get each new token from the queue and yield for our generator
    while True:
        try:
            next_token = q.get(True, timeout=1)
            if next_token is job_done:
                break
            content += next_token
            yield next_token, content
        except Empty:
            continue


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Question(BaseModel):
    text: str
    rag: bool = False


class BaseTicket(BaseModel):
    text: str


@app.get("/query-stream")
def qstream(question: Question = Depends()):
    output_function = llm_chain
    if question.rag:
        output_function = rag_chain

    q = Queue()

    def cb():
        output_function(
            {"question": question.text, "chat_history": []},
            callbacks=[QueueCallback(q)],
        )

    def generate():
        yield json.dumps({"init": True, "model": llm_name})
        for token, _ in stream(cb, q):
            yield json.dumps({"token": token})

    return EventSourceResponse(generate(), media_type="text/event-stream")


@app.get("/query")
async def ask(question: Question = Depends()):
    output_function = llm_chain
    if question.rag:
        output_function = rag_chain
    result = output_function(
        {"question": question.text, "chat_history": []}, callbacks=[]
    )

    return {"result": result["answer"], "model": llm_name}


@app.get("/generate-ticket")
async def generate_ticket_api(question: BaseTicket = Depends()):
    new_title, new_question = generate_ticket(
        neo4j_graph=neo4j_graph,
        llm_chain=llm_chain,
        input_question=question.text,
    )
    return {"result": {"title": new_title, "text": new_question}, "model": llm_name}

@app.get("/notification")
async def notification(user_type: str = Query(..., description="User type (KM/INVG)")):
    user_type_lower = user_type.lower()
    if user_type_lower == "km":
        return [
  {
    "description": "Urgent: Unidentified Aircraft Detected” - Immediate attention required. An unknown aircraft has been detected in Sector 17. Action required.",
    "date": "12/09/2024",
    "user": "UDITH",
    "id": "map_01"
  },
  {
    "description": "Urgent: Unidentified Aircraft Detected” - Immediate attention required. An unknown aircraft has been detected in Sector 17. Action required.",
    "date": "12/09/2024",
    "user": "UDITH",
    "id": "ontology_01"
  }
]
    elif user_type_lower == "invg":
        # Add functionality for INVG user type here
        return [{
"Content": "A report has been made by a community member concerning an individual observed taking photographs of residential property. The individual described has been noted in the community's Facebook group, sparking concern among members. Immediate analysis and follow-up actions are required to address and understand the situation",
"Widget": "Multiple",
"data": {
  "notificationPanel": {
    "type": "Notification",
    "timestamp": "25/2/2024 10:50",
    "content": "suspicious person watching JC homes",
    "sourceType": "Social media"
  },
  "contextPanel": {
    "type": "Notification",
    "timestamp": "25/2/2024 10:50",
    "content": "suspicious person watching JC homes",
    "sourceType": "Social media",
    "referenceThreat": "Hate Crime"
  },
  "socialMediaWidget": {
  "widgetTitleBar": {
    "createdDatetime": "25/02/2024, 10:07",
    "source": {
      "platform": "Facebook",
      "logoUrl": "URL_to_Facebook_Logo"
    },
    "author": {
      "image": "URL_to_Author_Image_Provided_by_Ben",
      "name": "Sheila Schwartz",
      "personOfInterest": {
        "isLit": True,
        "hoverText": "Sheila Schwartz is a member of the community.",
        "entityOfInterestWidget": "URL_or_ID_to_Entity_of_Interest_Widget"
      }
    }
  },
  "widgetBody": {
    "source": "Facebook group 'JOM - Jews of Melbourne'",
    "content": {
      "text": "Just seen a suspicious-looking man seemingly take a bunch of pictures of our house at Briggs st in Caulfield... I’m a little creeped out, did anyone else see something like that?",
      "postDatetime": "25/02/2024, 10:07",
      "reacts": {
        "likes": 17,
        "loves": 3,
        "cares": 9,
        "hahas": 0, 
        "wows": 2,
        "sads": 1,
        "angry": 1
      },
      "shares": 2,
      "totalComments": 15,
      "originalPostLink": "URL_to_Original_Post",
 "assumptionsTable": [
      {
        "category": "Hate Crime",
        "concern": "Physical harm to JC members",
        "assumption": "Suspect may be surveilling JC property/people planning a hate crime",
        "confidenceScore": "5"
      },
      {
        "category": "General Crime",
        "concern": "Property crime",
        "assumption": "Suspect may be surveilling JC property/people, planning robbery or theft",
        "confidenceScore": "5"
      },
      {
        "category": "Neutral",
        "concern": "Naive",
        "assumption": "Suspect may be scoping out the area for professional/sightseeing reasons",
        "confidenceScore": "5"
      }
    ]
    }
  }
  }
},
"Type": "Event1_5"

}]
    else:
        return {"error": "Invalid user type. Valid types are KM and INVG."}

# Define patterns for each question
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
        r"\b(?:reference|available|list) threats(?: in the ontology)?\b"
    ]
}

def match_intent(query):
    # Iterate over patterns and check for matches
    for question_id, question_patterns in patterns.items():
        for pattern in question_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return question_id
    return None

@app.get("/get-map")
async def get_map():
    response = {
  "latitude": "40.7127281",
  "longitude": "-74.0060152",
  "image_url": "https://www.gstatic.com/images/branding/product/1x/sheets_2020q4_48dp.png",
  "address": "Flinders Street 24, Melbourne, Australia",
  "sensitivity": "12.2",
  "description": "S23 in Melbourne, Flinders Street24' is a strategically located surveillance post overseeing critical sectors of Melbourne's Flinders Street24 area. Tasked with monitoring and analyzing real-time data, S23 serves as a vital node in the city's security infrastructure, ensuring timely response to potential threats and facilitating informed decision-making by authorities. Equipped with advanced surveillance technology and manned by trained personnel, S23 plays a pivotal role in safeguarding the integrity and safety of Flinders Street24, contributing to the overall security posture of the region.",
  "social": [
    {
      "name": "facebook",
      "icon": "fas fa-facebook",
      "link": "https://facebook.com"
    },
    {
      "name": "linkedin",
      "icon": "fas fa-linkedin",
      "link": "https://linkedin.com"
    }
  ],
  "entities": [
    {
      "name": "Entity One",
      "url": "https://entity-one.com",
      "image_url": "https://www.gstatic.com/images/branding/product/1x/sheets_2020q4_48dp.png",
      "latitude": "6.927079",
      "longitude": "79.861244",
      "description": "Entity One Description",
      "address": "Entity One Address",
      "sensitivity": "12.2",
      "social": [
        {
          "name": "facebook",
          "icon": "fas fa-facebook",
          "link": "https://facebook.com"
        },
        {
          "name": "linkedin",
          "icon": "fas fa-linkedin",
          "link": "https://linkedin.com"
        }
      ]
    }
  ]
}
    return response

@app.post("/upload")
async def upload():
    # logic for adding data to neo4j
    response = {
        "conversation": "Your Data Succesfuly Added"
}
    return response

class QueryBody(BaseModel):
    query: str
    coordinates: list
    multi_select: bool

@app.post("/chat")
async def chat(query_body: QueryBody):
    # Process the query and identify the question ID
    query = query_body.query.lower()
    intent = detect_question(query)
    print("intent")
    print(intent)
    
    # Based on the identified question ID, provide the corresponding response
    if intent:
        if intent == "question1":
            if query_body.multi_select:
                response = {
                              "conversation": "We Found below data sets for you to analyse which one would be of your interest please select",
                              "payload": {
                                "knowlege": [
                                  "Jewish community locations",
                                  "Past incidents",
                                  "Municipality locations",
                                  "Known offenders"
                                ],
                                "widget_type": "MULTI_SELECT_LIST"
                              }
                            }
            else:
                response = {
                              "conversation": "We Found below data sets for you to analyse which one would be of your interest please select",
                              "payload": {
                                "knowlege": [
                                  "Draw on map",
                                  "describe the required area"
                                ],
                                "widget_type": "SINGLE_SELECT_LIST"
                              }
                            }
             
        elif intent == "question2":
            response = {"conversation":" You have couple of options to update which one do you prefer",
                        "payload": {
                            "knowledge": ["Upload CSV", "Free flowing text"], "widget_type":"SINGLE_SELECT_LIST"
                        }
                        }


        elif intent == "question3":
            response = {
                          "conversation": "Below are significant dates and holidays of interest along with their dates or date ranges for this year.",
                          "payload": {
                            "knowledge": [
                              {"Holiday": "Rosh Hashanah", "Date": "September 25-27"},
                              {"Holiday": "Yom Kippur", "Date": "October 4"},
                              {"Holiday": "Sukkot", "Date": "October 9-16"},
                              {"Holiday": "Hanukkah", "Date": "December 7-14"},
                              {"Holiday": "Purim", "Date": "March 6-7"},
                              {"Holiday": "Passover", "Date": "April 5-13"},
                              {"Holiday": "Shavuot", "Date": "May 25-27"}
                            ],
                            "widget_type": "CALENDAR_TABLE"
                          }
                        }
        elif intent == "question4":
            response = {
                          "conversation": "Here are the types of crimes that our system monitors, along with descriptions and common examples.",
                          "payload": {
                            "knowledge": [
                              {
                                "Crime Type": "Cyber Crime",
                                "Description": "Crimes committed using computers or over the internet.",
                                "Common Types": "Phishing, Malware, Ransomware"
                              },
                              {
                                "Crime Type": "General Crime",
                                "Description": "Crimes affecting persons or properties not specifically categorized as hate crimes.",
                                "Common Types": "Theft, Vandalism, Burglary"
                              },
                              {
                                "Crime Type": "Hate Crime",
                                "Description": "Crimes motivated by biases against a race, religion, ethnicity, or sexual orientation.",
                                "Common Targets": "Religious institutions, Minority communities"
                              }
                            ],
                            "widget_type": "CRIME_OVERVIEW_TABLE"
                          }
                        }
    else:
        result = llm_chain({"question": query_body.query, "chat_history": []}, callbacks=[])
        return {
                              "conversation": result["answer"],
                              "payload": {
                                "knowlege": [],
                                "widget_type": ""
                              }
                }
    
    
    return response
