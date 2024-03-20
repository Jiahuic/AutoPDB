"""

Module Name: prepare_prompt.py

Author: Jiahui Chen
Email: 
Data: 0X/0X/2024
LastModifiedBy: jiahuic (Jiahui Chen)
LastEditTime: 03/10/2024

Functions:

"""

import os
import ollama
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from collections import Counter

try:
    from .PDB_query_prompt import biologist_PPI, message_PPI, message_failure
except:
    from PDB_query_prompt import biologist_PPI, message_PPI, message_failure

def parse_response(response):
    response = response.split("\n")
    number_entities = len(response)

    binding_protein = {}
    for entity in response:
        entity_id, entity_description = entity.split(" - ")
        binding_protein[entity_id] = entity_description

    return binding_protein

def get_protein_partner(entry_dict, epoch=10, model="gpt-3.5-turbo"):
    entry_id           = entry_dict['entry_id']
    title              = entry_dict['title']
    abstract           = entry_dict['abstract']
    entity_description = entry_dict['entity_description']

    # Get the polymer entity chain IDs. Only needed after the reply
    entity_id_auth_asym_ids = entry_dict["entity_auth_asym_ids"] 

    # Format the message with title and abstract text
    system_message = SystemMessagePromptTemplate.from_template(biologist_PPI)
    user_message = HumanMessagePromptTemplate.from_template(message_PPI)

    chat_prompt = ChatPromptTemplate.from_messages([system_message, user_message]).format(entry_id=entry_id, title=title, abstract=abstract, entity_description=entity_description)

    binding_proteins = []
    for i in range(epoch): # ensemble of all the models
        if model[:3] == "gpt":
            llm_openai = ChatOpenAI(model=model, temperature=0)
            response = llm_openai.invoke([chat_prompt]).content # each line of the response is a separate entity
        elif model[:6] == "llama2":
            llm = Ollama(model=model)
            response = llm.invoke([chat_prompt])

        # check if the response contains the "I cannot identify the binding protein."
        if message_failure in response:
            # print(message_failure)
            binding_proteins.append(None)
        try:
            binding_protein = parse_response(response)
            binding_proteins.append(binding_protein)
        except:
            binding_proteins.append(None)

    # for i in range(epoch):
        # Call Ollama API
        # response = ollama.generate(model='llama2', prompt=message)

    return

if __name__ == "__main__":
    from api_PDB import ask_RCSB_PDB

    entry_id = "6nk7"
    entry_id = "3ZIA"
    # entry_id = "1rvj" # 1rvj has no binding protein. The binding is about reaction center and the quinone molecule QB.
    entry_dict, expression_systems_entity_id = ask_RCSB_PDB(entry_id)

    get_protein_partner(entry_dict)
