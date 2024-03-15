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
from langchain.prompts import PromptTemplate, ChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from collections import Counter


def get_protein_partner(entry_dict, epoch=10):
    entry_id         = entry_dict['entry_id']
    title            = entry_dict['title']
    abstract         = entry_dict['abstract']
    polymer_entities = entry_dict['polymer_entities']

    # Format the message with title and abstract text
    chat_prompt = ChatMessagePromptTemplate.from_template(
        role = "assistant",
        template = """ 
        You are a biologist. Your role is to identify the binding protein of protein-protein interactions. Targeting the designed particles, antibodies, nanobodies, etc. Your return will be the chain ID. If there are multiple duplicated ID, just return the first one. Otherwise, return all the chain ID. The 'polymer_entities' section provides 'rcsb_polymer_entity_container_identifiers' for chain IDs and 'rcsb_polymer_entity' for chain descriptions.
        The entry ID {entry_id}, title {title}, abstract {abstract}, and polymer entities: {polymer_entities}.
        """
    )

    llm_openai = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    print(llm_openai.invoke([chat_prompt.format(entry_id=entry_id, title=title, abstract=abstract, polymer_entities=polymer_entities)]))
    exit()

    llm = Ollama(model="llama2:70b")
    print(llm.invoke([chat_prompt.format(entry_id=entry_id, title=title, abstract=abstract, polymer_entities=polymer_entities)]))
    exit()

    proteinA = []

    # for i in range(epoch):
        # Call Ollama API
        # response = ollama.generate(model='llama2', prompt=message)

    return proteinA, proteinB

if __name__ == "__main__":
    from api_PDB import ask_PDB

    entry_id = "6nk7"
    entry_dict = ask_PDB(entry_id)

    get_protein_partner(entry_dict)
