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
from temp import detect_question, detect_question_llm
from typing import List
from question_response import q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,ontology_data

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
    "content": "You have the capability to explore and analyze specific information tied to particular locations. This skill enables you to uncover valuable insights and gather pertinent details relevant to your reporting or investigative work.",
    "widget": "Multiple",
    "id": "123456",
    "data": {
      "notificationPanel": {
        "type": "km",
        "timestamp": "25/2/2024 10:50",
        "content": "Terrorist activities occur are examined and analyzed utilizing maps",
        "sourceType": "Open Sanction"
      },
      "contextPanel": {
        "type": "km",
        "timestamp": "25/2/2024 10:50",
        "content": "JC Ontology",
        "sourceType": "Open Sanction",
        "referenceThreat": "Terrorist"
      },
      "containerWidget": {
        "widgetTitleBar": {
          "timestamp": "25/2/2024 10:50",
          "containerType": "notofication",
          "typeList": [
            {
              "id": "notofication",
              "displayName": "Notification"
            },
            {
              "id": "alert",
              "displayName": "Alert"
            },
            {
              "id": "incident",
              "displayName": "Incident"
            },
            {
              "id": "case",
              "displayName": "Case"
            }
          ],
          "policyScore": "Critical",
          "policyScoreList": [
            "Low",
            "Medium",
            "High",
            "Critical"
          ],
          "assignee": "analyst",
          "id": "123456789",
          "actionsMenue": [
            "Open"
          ]
        },
        "widgetBody": {
          "content": "To initilize the system, please define your base target location by drawing it or by describing it",
          "sourceType": "System Initilization",
          "source": "map",
          "actionButtons": [
            "More"
          ],
          "referenceThreat": "",
          "referenceUseCase": "",
          "tigger": [
            "System Initial Use"
          ]
        }
      }
    },
    "type": "km",
    "actionKey": "kmEvent"
  }
]
    elif user_type_lower == "invg":
        # Add functionality for INVG user type here
        return [
  {
    "content": "A report has been made by a community member concerning an individual observed taking photographs of residential property. The individual described has been noted in the community's Facebook group, sparking concern among members. Immediate analysis and follow-up actions are required to address and understand the situation",
    "widget": "Multiple",
    "id": "123456",
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
            "originalPostLink": "URL_to_Original_Post"
          }
        }
      },
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
      ],
      "containerWidget": {
        "widgetTitleBar": {
          "timestamp": "25/2/2024 10:50",
          "containerType": "notofication",
          "policyScore": "Critical",
          "assignee": "analyst",
          "id": "123456789",
          "actionsMenue": [
            "Open"
          ]
        },
        "widgetBody": {
          "content": "To initilize the system, please define your base target location by drawing it or by describing it",
          "sourceType": "System Initilization",
          "source": "map",
          "actionButtons": [
            "More"
          ],
          "referenceThreat": "",
          "referenceUseCase": "",
          "tigger": [
            "System Initial Use"
          ]
        }
      }
    },
    "type": "event1",
    "actionKey": "event1_init"
  },
  {
    "content": "Problematic Iconography by Person of Interest.",
    "widget": "Multiple",
    "id": "1234567",
    "data": {
      "notificationPanel": {
        "type": "Notification",
        "timestamp": "25/2/2024 10:56",
        "content": "Problematic Iconography by Person of Interest.",
        "sourceType": "Social media"
      },
      "contextPanel": {
        "type": "Notification",
        "timestamp": "25/2/2024 10:56",
        "content": "Problematic Iconography by Person of Interest.",
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
            "originalPostLink": "URL_to_Original_Post"
          }
        }
      },
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
      ],
      "containerWidget": {
        "widgetTitleBar": {
          "timestamp": "25/2/2024 10:56",
          "containerType": "notofication",
          "policyScore": "Critical",
          "assignee": "John Dou",
          "id": "123456789",
          "actionsMenue": [
            "Open"
          ]
        },
        "widgetBody": {
          "content": "Unusual Iconography By a Person of interest",
          "sourceType": "Social media",
          "source": "Facebook Group - Melbourne Islamic Lectures, Classes & Events",
          "actionButtons": [
            "More"
          ],
          "referenceThreat": "Hate Crime",
          "referenceUseCase": "",
          "tigger": [
            "repeated iconography in the comments of a post by a person of interest marked as a potnetial threat"
          ]
        }
      }
    },
    "type": "event2",
    "actionKey": "event2_init"
  },
  {
    "content": "Potential merge of incidents",
    "widget": "Multiple",
    "id": "1234567",
    "data": {
      "notificationPanel": {
        "type": "Alets",
        "timestamp": "25/2/2024 10:56",
        "content": "New alert received: Potential merge of incidents",
        "sourceType": "Social media"
      },
      "contextPanel": {
        "type": "Alets",
        "timestamp": "25/2/2024 10:56",
        "content": "New alert received: Potential merge of incidents",
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
            "originalPostLink": "URL_to_Original_Post"
          }
        }
      },
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
      ],
      "containerWidget": {
        "widgetTitleBar": {
          "timestamp": "25/2/2024 10:56",
          "containerType": "notofication",
          "policyScore": "Critical",
          "assignee": "John Dou",
          "id": "123456789",
          "actionsMenue": [
            "Open"
          ]
        },
        "widgetBody": {
          "content": "Unusual Iconography By a Person of interest",
          "sourceType": "Ontoligical rule",
          "source": "Facebook Group - Melbourne Islamic Lectures, Classes & Events",
          "actionButtons": [
            "Ontology Widget"
          ],
          "referenceThreat": "Hate Crime",
          "referenceUseCase": "",
          "tigger": [
            "Rule: 'Suspect in one incident added as person of interest in another incident"
          ]
        }
      }
    },
    "type": "event3",
    "actionKey": "event3_init"
  }
]
    else:
        return {"error": "Invalid user type. Valid types are KM and INVG."}



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
class OntologyType(BaseModel):
    type: str

# Endpoint to filter the array based on the provided ontology types
@app.post("/get_ontology")
async def get_ontology(ontology_type: List[OntologyType]):
    filtered_results = []
    for item in ontology_data:
        for criterion in ontology_type:
            if item.get('type') == criterion.type:
                filtered_results.append(item)
                # break
    return filtered_results   

@app.post("/upload")
async def upload():
    # logic for adding data to neo4j
    response = {
        "conversation": "Your location data has been incorporated into the ontology graph. Feel free to analyze it for insights and patterns."
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
    if intent == None:
        intent = detect_question_llm(query)
        print("Response From LLM: ", intent)
        
    # Based on the identified question ID, provide the corresponding response
    if intent:
        if intent == "question1":
            if query_body.multi_select:
                response = {
                              "conversation": "We Found below data sets for you to analyse which one would be of your interest please select",
                              "payload": {
                                "knowlege": [
                                  {
                                    "type": "municipility",
                                    "value": "Municipality"
                                  },
                                  {
                                    "type": "past_incidents",
                                    "value": "Past Incidents"
                                  },
                                  {
                                    "type": "poi",
                                    "value": "Known Offenders"
                                  },
                                  {
                                    "type": "jwish_community",
                                    "value": "Jewish Community"
                                  }
                                ],
                                "widgetType": "MULTI_SELECT_LIST"
                              }
                            }
            else:
                response = {
                              "conversation": "To initilize the system please select your region",
                              "payload": {
                                "knowlege": [
                                  "Draw on map",
                                  "describe the required area"
                                ],
                                "widget_type": "SINGLE_SELECT_LIST"
                              }
                            }
             
        elif intent == "question2":
            response = {
                          "conversation": "How will you add data?",
                          "payload": {
                            "knowledge": [
                              "Upload CSV",
                              "Free flowing text"
                            ],
                            "widgetType": "SINGLE_SELECT_LIST"
                          }
                        }


        elif intent == "question3":
            response = {
                          "conversation": "Below are significant dates and holidays of interest along with their dates or date ranges for this year.",
                          "payload": {
                            "knowledge": [
                              {
                                "holiday": "Rosh Hashanah",
                                "duration": "2 days",
                                "start": "September 25",
                                "end": "September 27",
                                "freequency": "First and second day of the Jewish month of Tishrei",
                                "effectiveHours": "Full day",
                                "reference": "https://simple.wikipedia.org/wiki/Rosh_Hashanah",
                                "related": {
                                  "caseId": "1234567890",
                                  "personOfInterest": "John Murphy",
                                  "reason": "Some Reason",
                                  "locationOfInterest": "Melborn, Austrailia"
                                },
                                "policyScore": "low",
                                "justification": ""
                              },
                              {
                                "holiday": "Yom Kippur",
                                "duration": "1 day",
                                "start": "October 4",
                                "end": "October 4",
                                "freequency": "Tenth day of the Jewish month of Tishrei",
                                "effectiveHours": "Full day (fasting)",
                                "reference": "https://simple.wikipedia.org/wiki/Yom_Kippur",
                                "related": {
                                  "caseId": "1234567890",
                                  "personOfInterest": "John Murphy",
                                  "reason": "Some Reason",
                                  "locationOfInterest": "Melborn, Austrailia"
                                },
                                "policyScore": "low",
                                "justification": ""
                              }
                            ],
                            "widgetType": "CALENDAR_TABLE"
                          }
                        }
        elif intent == "question4":
            response = {
                          "conversation": "Here are the types of crimes that our system monitors, along with descriptions and common examples.",
                          "payload": {
                            "knowledge": [
                              {
                                "crimeType": "Cyber Crime",
                                "description": "Crimes committed using computers or over the internet.",
                                "commonTypes": "Phishing, Malware, Ransomware"
                              }
                            ],
                            "widgetType": "CRIME_OVERVIEW_TABLE",
                            "actionKey": "km_crime"
                          }
                        }
        elif intent == "question5":
            response = q5
        elif intent == "question6":
            response = q6
        elif intent == "question7":
            response = q7
        elif intent == "question8":
            response = q8
        elif intent == "question9":
            response = q9
        elif intent == "question10":
            response = q10
        elif intent == "question11":
            response = q11
        elif intent == "question12":
            response = q12
        elif intent == "question13":
            response = q13
        elif intent == "question14":
            response = q14
        elif intent == "question15":
            response = q15
        elif intent == "question16":
            response = q16
        elif intent == "question17":
            response = q17
        elif intent == "question18":
            response = q18
        elif intent == "question19":
            response = q19
        elif "None" in intent:
            result = llm_chain({"question": query_body.query, "chat_history": []}, callbacks=[])
            response =  {
                  "conversation": result["answer"],
                  "payload": {
                    "knowlege": [],
                    "widget_type": ""
                  }
                }
        elif intent.__contains__("None"):
            result = llm_chain({"question": query_body.query, "chat_history": []}, callbacks=[])
            response =  {
                  "conversation": result["answer"],
                  "payload": {
                    "knowlege": [],
                    "widget_type": ""
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
