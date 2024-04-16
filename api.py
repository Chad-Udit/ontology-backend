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
from typing import List
from question_response import q5,q6,q7,q8,q9,q10,q11,q12,q13,q14

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
        "Content": "You have the capability to explore and analyze specific information tied to particular locations. This skill enables you to uncover valuable insights and gather pertinent details relevant to your reporting or investigative work.",
        "Widget": "Multiple",
        "data": {
            "notificationPanel": {
                "type": "investigation",
                "timestamp": "25/2/2024 10:50",
                "content": "Terrorist activities occur are examined and analyzed utilizing maps",
                "sourceType": "Open Sanction"
            },
            "contextPanel": {
                "type": "investigation",
                "timestamp": "25/2/2024 10:50",
                "content": "Investigation Research in Melborn",
                "sourceType": "Open Sanction",
                "referenceThreat": "Terrorist"
            },
        },
        "Type": "km"
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
class OntologyType(BaseModel):
    type: str
ontology_data = [
  {
    "name": "Municipility 01",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.845985",
    "longitude": "145.000935",
    "description": "",
    "address": "32 Motherwell St, South Yarra VIC 3141, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 02",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.895103",
    "longitude": "144.992387",
    "description": "",
    "address": "32 Drake St, Brighton VIC 3186, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 03",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.922107",
    "longitude": "144.996483",
    "description": "",
    "address": "19 Windermere Cres, Brighton VIC 3186, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 04",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.873972",
    "longitude": "145.010783",
    "description": "",
    "address": "12 St Aubins Ave, Caulfield North VIC 3161, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 05",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.884232",
    "longitude": "145.058022",
    "description": "",
    "address": "Carnegie VIC 3163, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 06",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.907224",
    "longitude": "145.027034",
    "description": "",
    "address": "18 Norman St, McKinnon VIC 3204, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 07",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.855392",
    "longitude": "145.02504",
    "description": "",
    "address": "14 Tower Ct, Armadale VIC 3143, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 08",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.85926",
    "longitude": "145.021668",
    "description": "",
    "address": "13 Inverness Ave, Armadale VIC 3143, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 09",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.85926",
    "longitude": "145.021668",
    "description": "",
    "address": "13 Inverness Ave, Armadale VIC 3143, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "Municipility 10",
    "url": "",
    "image_url": "https://img.freepik.com/free-vector/city-hall-concept-illustration_114360-17135.jpg?w=826&t=st=1712125219~exp=1712125819~hmac=ddf33753238a9b2be82ac528c2850c4621ea9600284c243276986ab3c1d9d3b5",
    "latitude": "-37.835204",
    "longitude": "145.052392",
    "description": "",
    "address": "58 Pleasant Rd, Hawthorn East VIC 3123, Australia",
    "sensitivity": "0.0",
    "color": "#556B2F",
    "map_icon": "municiple.png",
    "social": [],
    "create_date": "",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "municipility"
  },
  {
    "name": "National 'social'ist Network",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.806261721099204",
    "longitude": "144.94108963946522",
    "description": "Displayed a banner reading “Expose Jewish Power” in front of a train station in Melbourne, boarded a train, handed out materials and asked passengers if they were Jewish. People affiliated with NSN posted picture of the incident and propagating the antisemitic Great Replacement conspiracy theory and on the 'social' media platform Gab, and asserted “Expose Jewish power because Jews slander gentile nationalists as baby-killers and terrorists, all the while Israel fires a missile into a Palestinian hospital killing hundreds of women and children.”",
    "address": "189 Railway Pl, West Melbourne VIC 3003, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "14/10/2023",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Arab descent",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.8026082291746",
    "longitude": "144.94112182597388",
    "description": " Two pieces of graffiti, both composed of “Kill JEWS”, were written on the pavement in south Melbourne.",
    "address": "103 Laurens St, North Melbourne VIC 3051, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "13/10/2023",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Group of Arab descents",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.83616136793307",
    "longitude": "144.9766517670443",
    "description": "A car full of men of ‘Arab descent’ reportedly boasted they were ‘on the hunt to kill Jews’ as they cruised around a Melbourne suburb, with police on alert for anti-Semitic threats in the wake of the Israel-Hamas war",
    "address": "2/8 Toorak Rd, South Yarra VIC 3141, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "11/10/2023",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "The man, a self-proclaimed 'Nazi'",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.882925549488306",
    "longitude": "145.00492131063197",
    "description": "Jewish students threatened with a knife on a bus in Melbourne, Australia. Jewish Students from the Leibler Yavneh College in Australia were traveling on a public bus when they were abused with antisemitic obscenities by a knife-wielding man on Thursday, according to a press release from the Anti-Defamation Commission (ADC).",
    "address": "22 Staniland Grove, Elsternwick VIC 3185, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "05/08/2023",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Children in a public school",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.80165672201562",
    "longitude": "144.9798424238497",
    "description": "A Jewish family from Melbourne told Daily Mail Australia that their teenage daughter had been targeted by high school students. Her mother, who wished to remain anonymous, said a series of antisemitic incidents had been directed at her daughter since the start of the year, well before the current Israel/Hamas conflict. 'She has been sent swastikas online. One child repeatedly approached her and told her 'Knock Knock' jokes in which the butt of the jokes are 'dead Jews,' she said. 'Another student approached her and declared: I will gas you and your whole family.'",
    "address": "Whitlam Place, Fitzroy VIC 3065, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "01/09/2023",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Free Palestine Melbourne activists",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.886531299065524",
    "longitude": "145.02208483972316",
    "description": "Clashes between pro-Palestinian and pro-Israeli groups in Melbourne's south-east. A rally was organised on Friday, with a spokesperson for Free Palestine Melbourne saying it was organised in response to an arson attack on a burger shop on Glenhuntly Road in Caulfield, owned by a man of Palestinian heritage. Police said on Friday they were treating the fire at Burgertory as suspicious, but repeatedly said they did not believe it was linked to the owner's attendance at an earlier pro-Palestinian rally. Small numbers of people, some draped in Israeli flags, had gathered near the boarded-up burger store throughout the day.",
    "address": "340 Hawthorn Rd, Caulfield VIC 3162, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "11/11/2023",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Unknown",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.88513402181724",
    "longitude": "145.02137483642312",
    "description": "The word 'genocide' and a picture of the Palestinian flag were found spray-painted across the Beth Weizmann Community Centre.",
    "address": "304 Hawthorn Rd, Caulfield South VIC 3162, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "07/10/2023",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Muslim Crowd",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.89368640521054",
    "longitude": "145.0227894868903",
    "description": "A synagogue in the Australian city of Melbourne was evacuated on police order on Shabbat as pro-Palestinian protesters demonstrated nearby.",
    "address": "Caulfield South VIC 3162, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "13/11/2023",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "A group of young men inside the car",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.880527532151596",
    "longitude": "145.0305463950657",
    "description": "Rabbi walking with young child on Melbourne street confronted with alleged antisemitic threats",
    "address": "84 Bambra Rd, Caulfield North VIC 3161, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "11/10/2023",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Pro-Palestinian protestors",
    "url": "",
    "image_url": "https://t4.ftcdn.net/jpg/00/84/33/59/360_F_84335986_8kvtezwbvYl99MOIhT67tRxx3ZEC7fM6.jpg",
    "latitude": "-37.81497538763534",
    "longitude": "144.96664039908464",
    "description": "A member of Melbourne’s Jewish community claims she and her husband were attacked by pro-Palestinian protestors outside the Melbourne Town Hall. The attack happened last night as the City of Melbourne voted down a motion for the council to call for a ceasefire in Gaza.",
    "address": "Melbourne Town Hall, Melbourne VIC 3000, Australia",
    "sensitivity": "0.0",
    "color": "#B22222",
    "map_icon": "past_incidents.png",
    "social": [],
    "create_date": "21/02/2024",
    "create_user": "",
    "status": "",
    "interest_level": "",
    "occupation": "",
    "workplace": "",
    "type": "past_incidents"
  },
  {
    "name": "Layla Ahmed Ibrahim",
    "url": "",
    "image_url": "/images/layla_ahmed_ibrahim.png",
    "latitude": "-37.817677963769526",
    "longitude": "144.99396042575503",
    "description": "Took photos of the jewish community ",
    "address": "123 Bridge Rd, Richmond VIC 3121",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "4/24/2023",
    "create_user": "",
    "status": "existing",
    "interest_level": "high",
    "occupation": "Barista",
    "workplace": "Richmond",
    "type": "poi"
  },
  {
    "name": "Jamal Hassan Reza",
    "url": "",
    "image_url": "/images/jamal_hassan_reza.png",
    "latitude": "-37.814688456905664",
    "longitude": "144.96318302575494",
    "description": "wrote antisemitic post on Facebook",
    "address": "Level 12, 500 Bourke St, Melbourne VIC 3000",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "3/13/2024",
    "create_user": "",
    "status": "new",
    "interest_level": "medium",
    "occupation": "Architect",
    "workplace": "Collingwood",
    "type": "poi"
  },
  {
    "name": "Yasmin Aisha Khatun",
    "url": "",
    "image_url": "/images/yasmin_aisha_khatun.png",
    "latitude": "-37.82336905157906",
    "longitude": "144.95808456808447",
    "description": "Antesemitic comment on Twitter",
    "address": "Crown Melbourne, 8 Whiteman St, Southbank VIC 3006",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "8/22/2022",
    "create_user": "",
    "status": "exisiting ",
    "interest_level": "medium ",
    "occupation": "Chef",
    "workplace": "Southbank",
    "type": "poi"
  },
  {
    "name": "Amir Mohammed Farhan",
    "url": "",
    "image_url": "/images/amir_mohammed_farhan.png",
    "latitude": "-37.82040394544925",
    "longitude": "144.9499054680843",
    "description": "Clashed with young Jews near a synagogue",
    "address": "WeWork, 727 Collins St, Docklands VIC 3008",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "8/22/2022",
    "create_user": "",
    "status": "new",
    "interest_level": "high",
    "occupation": "Web Developer",
    "workplace": "Docklands",
    "type": "poi"
  },
  {
    "name": "Sara bint Abdullah",
    "url": "",
    "image_url": "/images/sara_bint_abdullah.png",
    "latitude": "-37.784075790402554",
    "longitude": "144.9841956680829",
    "description": "Antesemitic comment on Twitter",
    "address": "Fitzroy North Primary School, 25 Brunswick St, Fitzroy North VIC 3065",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "7/12/2023",
    "create_user": "",
    "status": "new",
    "interest_level": "medium",
    "occupation": "Teacher",
    "workplace": "Fitzroy North",
    "type": "poi"
  },
  {
    "name": "Khalid Reza Ali",
    "url": "",
    "image_url": "/images/khalid_reza_ali.png",
    "latitude": "-37.82713651118103",
    "longitude": "145.03482539692",
    "description": "Threatening a Jewish student",
    "address": "Studio K, 564 Glenferrie Rd, Hawthorn VIC 3122",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "3/14/2024",
    "create_user": "",
    "status": "new",
    "interest_level": "high",
    "occupation": "Graphic Designer",
    "workplace": "Hawthorn",
    "type": "poi"
  },
  {
    "name": "Noor Fatima bint Mohammed",
    "url": "",
    "image_url": "/images/noor_fatima_bint_mohammed.png",
    "latitude": "-37.795858179989104",
    "longitude": "144.8853806969189",
    "description": "Laughing emoji under antesemitic post",
    "address": "Rapid Plumbing, 1/24 Essex St, Footscray VIC 3011",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "8/10/2023",
    "create_user": "",
    "status": "exisiting",
    "interest_level": "low",
    "occupation": "Plumber",
    "workplace": "Footscray",
    "type": "poi"
  },
  {
    "name": "Ibrahim Hassan Omar",
    "url": "",
    "image_url": "/images/ibrahim_hassan_omar.png",
    "latitude": "-37.7691146423713",
    "longitude": "144.9615048935992",
    "description": "Antesemitic comment on Twitter",
    "address": "Petal Power, 353 Sydney Rd, Brunswick VIC 3056",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "2/7/2024",
    "create_user": "",
    "status": "new",
    "interest_level": "medium",
    "occupation": "Florist",
    "workplace": "Brunswick",
    "type": "poi"
  },
  {
    "name": "Aisha bint Khalid",
    "url": "",
    "image_url": "/images/aisha_bint_khalid.png",
    "latitude": "-37.859590630628745",
    "longitude": "144.97794122575675",
    "description": "Antesemitic comment on Facebook",
    "address": "St Kilda Road Medical Centre, 127 Fitzroy St, St Kilda VIC 3182",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "3/3/2024",
    "create_user": "",
    "status": "new",
    "interest_level": "meium",
    "occupation": "Doctord",
    "workplace": "St Kilda",
    "type": "poi"
  },
  {
    "name": "Omar Ali Mohammed",
    "url": "",
    "image_url": "/images/omar_ali_monammed.png",
    "latitude": "-37.741596509857374",
    "longitude": "144.96628593924586",
    "description": "Laughing emoji under antesemitic post",
    "address": "Sparks R Us, 485 Sydney Rd, Coburg VIC 3058",
    "sensitivity": "0.0",
    "color": "#e8ada0",
    "map_icon": "poi_marker.png",
    "social": [],
    "create_date": "2/27/2024",
    "create_user": "",
    "status": "new",
    "interest_level": "low",
    "occupation": "Electrician",
    "workplace": "Coburg",
    "type": "poi"
  }
]
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
