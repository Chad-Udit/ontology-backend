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
# from question_response import km,invg,curr_map,upload_res,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,ontology_data
from question_response import *

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
        return km
    elif user_type_lower == "invg":
        # Add functionality for INVG user type here
        return invg
    else:
        return {"error": "Invalid user type. Valid types are KM and INVG."}



@app.get("/get-map")
async def get_map():
    response = curr_map
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
    response = upload_res
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
                response = q1_multi
            else:
                response = q1_single
             
        elif intent == "question2":
            response = q2


        elif intent == "question3":
            response = q3
        elif intent == "question4":
            response = q4
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
        elif intent == "question20":
            response == q5
        elif intent == "question21":
            response == q21
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
