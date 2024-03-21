"""

Module Name: prepare_prompt.py

Author: Jiahui Chen
Email: 
Data: 0X/0X/2024
LastModifiedBy: jiahuic (Jiahui Chen)
LastEditTime: 03/10/2024

Functions:

"""

import os, re
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
    # Preprocess text to remove leading spaces from each line
    response = "\n".join(line.strip() for line in response.splitlines())

    # Pattern to match the entity ID and entity description, e.g., "6 - HEAVY CHAIN" check prompt
    reply_pattern = re.compile(r"(\d+) - ([\w\s,]+)")

    # Use re.findall() to find all matches
    matches = reply_pattern.findall(response)

    # Convert numbers to integers for sorting, keep descriptions as is
    matches_with_integers = [(int(number), description) for number, description in matches]
    
    # Sort matches based on the number
    matches = sorted(matches_with_integers, key=lambda x: x[0])

    # Check if matches were found
    if matches:
        binding_proteins = {}
        for number, description in matches:
            binding_proteins[str(number)] = description.replace("\n", "")
        return binding_proteins
    else:
        return None

def vote_binding_proteins(binding_proteins=None):
    # Here we do not consider the case where the responses are different
    from collections import Counter
    entity_IDs = [key for bp in binding_proteins for key in bp.keys()]
    return Counter(entity_IDs).most_common(1)[0]

def get_protein_partner(entry_dict, epoch=10, model="gpt-3.5-turbo"):
    entry_id    = entry_dict['entry_id']
    title       = entry_dict['title']
    abstract    = entry_dict['abstract']
    entity_name = entry_dict['entity_description']

    # Get the polymer entity chain IDs. Only needed after the reply
    entity_id_auth_asym_ids = entry_dict["entity_auth_asym_ids"] 

    # Format the message with title and abstract text
    system_message = SystemMessagePromptTemplate.from_template(biologist_PPI)
    user_message = HumanMessagePromptTemplate.from_template(message_PPI)

    chat_prompt = ChatPromptTemplate.from_messages([system_message, user_message]).format(entry_id=entry_id, title=title, abstract=abstract, entity_name=entity_name)

    binding_proteins = []
    for i in range(epoch): # ensemble of all the models
        if model[:3] == "gpt":
            llm_openai = ChatOpenAI(model=model, temperature=0)
            response = llm_openai.invoke([chat_prompt]).content # each line of the response is a separate entity
            # print(response)
        elif model[:6] == "llama2":
            llm = Ollama(model=model)
            response = llm.invoke([chat_prompt])
            # print(response)
        elif model[:7] == "mistral":
            llm = Ollama(model=model)
            response = llm.invoke([chat_prompt])
        else:
            raise ValueError("Model not supported.")

        # check if the response contains the "I cannot identify the binding protein."
        if message_failure in response:
            continue
        binding_proteins.append(parse_response(response))

    if not binding_proteins:
        print("I cannot identify the binding protein.")
        return
    (entity_ID, counts) = vote_binding_proteins(binding_proteins)
    print(f"The binding protein is {entity_ID} with {counts} votes.")

    return entity_ID, counts

if __name__ == "__main__":
    from api_PDB import ask_RCSB_PDB

    entry_id = "6nk7"
    entry_id = "3ZIA"
    # entry_id = "1rvj" # 1rvj has no binding protein. The binding is about reaction center and the quinone molecule QB.
    entry_dict, expression_systems_entity_id = ask_RCSB_PDB(entry_id)

    get_protein_partner(entry_dict, model="llama2:7b")
    # get_protein_partner(entry_dict, model="mistral")
    # get_protein_partner(entry_dict)
