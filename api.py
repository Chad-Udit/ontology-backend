import os

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
        pass
    else:
        return {"error": "Invalid user type. Valid types are KM and INVG."}

# Define mappings between question variations and their IDs
# question_mappings = {
#     "question1": ["give me available data", "show available data"],
#     "question2": ["i would like to add more data to jewish community", "add data to jewish community"],
#     "question3": ["what dates of interest are available in the ontology?", "available dates in the ontology?"],
#     "question4": ["what reference threats are available in the ontology?", "available reference threats?"]
# }
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
        "expand jewish community data"
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

class QueryBody(BaseModel):
    query: str
    coordinates: list
    multi_select: bool

@app.post("/chat")
async def chat(query_body: QueryBody):
    # Process the query and identify the question ID
    query = query_body.query.lower()
    question_id = None
    for q_id, variations in question_mappings.items():
        for variation in variations:
            if variation.lower() in query:
                question_id = q_id
                break
        if question_id:
            break
    
    # Based on the identified question ID, provide the corresponding response
    if question_id:
        if question_id == "question1":
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
             
        elif question_id == "question2":
            response = {"conversation":" You have couple of options to update which one do you prefer",
 "payload": {
    "knowlege": ["Upload CSV", "Free flowing text"], "widget_type":"LIST"
}
}


        elif question_id == "question3":
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
        elif question_id == "question4":
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
        response = {"response": "Sorry, I couldn't understand your question."}
    
    return response
