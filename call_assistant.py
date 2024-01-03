from openai import OpenAI
import json
import re

from dotenv import load_dotenv
import os

load_dotenv()

variable_value = os.getenv("OPENAI_PK")

def call_openai(mango_disease):
     client = OpenAI(
        # This is the default and can be omitted
            api_key=variable_value
        )

     assistant = client.beta.assistants.create(
            name="Mango expert",
            instructions="You are a mango fruit expert who specializes with deseases affecting mango leafs. You are capable of giving recomendations on how to treat the ilnesses affecting mangos. As well as diagonse possible factors that may have contributed to the mango contrating that disease",
            model="gpt-3.5-turbo-1106"
            )

     thread = client.beta.threads.create()

     message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"I have a mango crop with {mango_disease} how should I treat it, and what could be causing the diseases"
        )
     run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        )



     is_queued = True
     while is_queued == True: 
            status = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
            status = status.model_dump_json(indent=2)
            json_status= json.loads(status)['status']
            
            if json_status == 'completed':
                is_queued = False


     messages = client.beta.threads.messages.list(thread_id=thread.id)
     message_dictionary = messages.json()
     message_json = json.loads(message_dictionary)
     return message_json["data"][0]["content"][0]["text"]["value"]