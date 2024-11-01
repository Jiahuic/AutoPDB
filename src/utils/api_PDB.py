"""
This contains the functions to read the protein information from the PDB file 
and get the protein information from the PDB database using the GraphQL API.

Module Name: api_PDB.py

Author: Xingjian Xu
Email: 
Data: 0X/0X/2024
LastModifiedBy: jiahuic (Jiahui Chen)
LastEditTime: 03/10/2024

Functions:
* ask_RCSB_PDB(entry_id): This function takes a PDB ID as input and returns a dictionary with the title, abstract, and polymer entities of the PDB entry.

"""
import requests
try:
    from .PDB_query_prompt import query, RCSB_PDB_api_url
except:
    from PDB_query_prompt import query, RCSB_PDB_api_url

def ask_RCSB_PDB(entry_id): # entry_id is the PDB ID
    # If the response is not 200 or other faults, return an empty dictionary
    entry_dict = {"entry_id": entry_id, "title": None, "abstract": None, 
                  "entity_description": None, "entity_auth_asym_ids": None}

    # Send POST request with GraphQL query
    response = requests.post(url=RCSB_PDB_api_url, json={"query": query.format(entry_id=entry_id)})
    if response.status_code == 200:
        # print("Response for entry", entry_id)

        # Parse JSON response
        entry_info = response.json()["data"]["entry"]

        structure_info = entry_info["struct"]
        if structure_info is not None:
            entry_dict["title"] = structure_info["title"]
        else:
            print(f"Entry {entry_id} has no structure_info.")
            return entry_dict, {}

        pubmed_info = entry_info["pubmed"]
        if pubmed_info is not None:
            entry_dict["abstract"] = pubmed_info["rcsb_pubmed_abstract_text"]

        polymer_entities = entry_info["polymer_entities"]

        # Link the polymer entites to ["rcsb_polymer_entity"]["pdbx_description"]
        entity_id_pdbx_description = {}
        for polymer_entity in polymer_entities:
            entity_id = polymer_entity["rcsb_polymer_entity_container_identifiers"]["entity_id"]
            pdbx_description = polymer_entity["rcsb_polymer_entity"]["pdbx_description"]
            entity_id_pdbx_description[entity_id] = pdbx_description
        entry_dict["entity_description"] = entity_id_pdbx_description

        # Link the polymer entites to {"rcsb_polymer_entity_container_identifiers"]["auth_asym_ids"]
        entity_id_auth_asym_ids = {}
        for polymer_entity in polymer_entities:
            entity_id = polymer_entity["rcsb_polymer_entity_container_identifiers"]["entity_id"]
            auth_asym_ids = polymer_entity["rcsb_polymer_entity_container_identifiers"]["auth_asym_ids"]
            entity_id_auth_asym_ids[entity_id] = auth_asym_ids
        entry_dict["entity_auth_asym_ids"] = entity_id_auth_asym_ids

        # find out the number of expression_system from rcsb_entity_source_organism
        expression_systems_entity_id = {}
        for polymer_entity in polymer_entities:
            if polymer_entity["rcsb_entity_source_organism"] is None:
                continue
            expression_system = polymer_entity["rcsb_entity_source_organism"][0]['scientific_name']
            entity_id = polymer_entity["rcsb_polymer_entity_container_identifiers"]["entity_id"]
            if expression_system not in expression_systems_entity_id:
                expression_systems_entity_id[expression_system] = [entity_id]
            else:
                expression_systems_entity_id[expression_system].append(entity_id)

    return entry_dict, expression_systems_entity_id

if __name__ == "__main__":
    import json
    entry_id = "6nk7"
    entry_id = "3ZIA"
    entry_id = "1CMX"
    entry_id = "1FAK"
    entry_dict, expression_systems_entity_id = ask_RCSB_PDB(entry_id)
    print(entry_dict)

    # with open(f"{entry_id}.json", "w", encoding="utf-8") as f:
    #     json.dump(entry_dict, f, indent=4, ensure_ascii=False)
