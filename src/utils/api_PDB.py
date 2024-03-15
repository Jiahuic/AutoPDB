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
* ask_PDB(entry_id): This function takes a PDB ID as input and returns a dictionary with the title, abstract, and polymer entities of the PDB entry.

"""
import requests

# Define the URL of the PDB API
api_PDB_url = "https://data.rcsb.org/graphql"

def ask_PDB(entry_id): # entry_id is the PDB ID
    query = f'''
    {{
      entry(entry_id: "{entry_id}") {{
        struct {{
          title
        }}
        pubmed {{
          rcsb_pubmed_abstract_text
        }}
        polymer_entities {{
          rcsb_polymer_entity_container_identifiers {{
            auth_asym_ids
          }}
          rcsb_polymer_entity {{
            pdbx_description
          }}
        }}
      }}
    }}
    '''

    # If the response is not 200 or other faults, return an empty dictionary
    entry_dict = {"entry_id": entry_id, "title": None, "abstract": None, "polymer_entities": None}

    # Send POST request with GraphQL query
    response = requests.post(url=api_PDB_url, json={"query": query})
    if response.status_code == 200:
        print("Response for entry", entry_id)

        # Parse JSON response
        entry_info = response.json()["data"]["entry"]

        structure_info = entry_info["struct"]
        if structure_info is not None:
            entry_dict["title"] = structure_info["title"]

        pubmed_info = entry_info["pubmed"]
        if pubmed_info is not None:
            entry_dict["abstract"] = pubmed_info["rcsb_pubmed_abstract_text"]

        entry_dict["polymer_entities"] = entry_info["polymer_entities"]

    return entry_dict

if __name__ == "__main__":
    import json
    entry_id = "6nk7"
    entry_dict = ask_PDB(entry_id)

    with open(f"{entry_id}.json", "w", encoding="utf-8") as f:
        json.dump(entry_dict, f, indent=4, ensure_ascii=False)
