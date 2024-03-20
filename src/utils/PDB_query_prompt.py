"""
This contains the query to call the GraphQL API.

Module Name: api_PDB_query.py

Author: Jiahui Chen
Email: 
Data: 03/16/2024
LastModifiedBy: jiahuic (Jiahui Chen)
LastEditTime: 03/16/2024

Variables:
query: This is the query to call the GraphQL API. It takes an entry_id as input and returns a dictionary with the title, abstract, and polymer entities of the PDB entry.

RCSB_PDB_api_url: This is the URL of the PDB API.

biologist_PPI and user_message: This is the prompt for the biologist to identify the binding protein of protein-protein interactions.

"""

# Define the prompt of biologist_PPI
biologist_PPI = """ 
You are a biologist. Your role is to identify the binding protein of protein-protein interactions. 
Targeting the designed particles, antibodies, nanobodies, inhibitor protein, etc. 
Your return will be the entity ID. 
The polymer entities provide the information of each entity description.
If you cannot identify the binding protein, please return "I cannot identify the binding protein."
For example, the chains in the entity description are from one protein, and the other protein is not in the entity description.
Your responses should adhere to the following formats:
===
If the chain ID(s) can be identified, return all relevant IDs with descriptions split by "-" as:
[ID] - entity description ...
6 - HEAVY CHAIN
===
If the binding protein cannot be identified, only reply as:
I cannot identify the binding protein.
===
"""

message_PPI = """
The entry ID {entry_id}, title {title}, abstract {abstract}, and entity description: {entity_description}.
"""

message_failure = "I cannot identify the binding protein."

# Define the URL of the PDB API
RCSB_PDB_api_url = "https://data.rcsb.org/graphql"

query = '''
{{
  entry(entry_id: "{entry_id}") {{
    rcsb_id
    struct {{
      title
    }}
    pubmed {{
      rcsb_pubmed_container_identifiers {{
        pubmed_id
      }}
      rcsb_pubmed_doi
      rcsb_pubmed_abstract_text
    }}
    rcsb_external_references {{
      id
      type
      link
    }}
    struct_keywords {{
      pdbx_keywords
      text
    }}
    pdbx_database_related {{
      content_type
      db_id
      details
    }}
    em_3d_reconstruction {{
      resolution
    }}
    pdbx_database_related {{
      db_id
      db_name
    }}
    rcsb_entry_info {{
      molecular_weight
      deposited_atom_count
      deposited_model_count
      deposited_polymer_monomer_count
      deposited_modeled_polymer_monomer_count
      deposited_unmodeled_polymer_monomer_count
      polymer_entity_count_protein
      polymer_entity_count_nucleic_acid
      polymer_entity_count_nucleic_acid_hybrid
    }}
    rcsb_binding_affinity {{
      comp_id
      type
      value
      unit
      reference_sequence_identity
      provenance_code
      link
    }}
    polymer_entities {{
      polymer_entity_instances {{
        rcsb_polymer_entity_instance_container_identifiers {{
          auth_asym_id
          asym_id
          entity_id
        }}
      }}
      rcsb_polymer_entity_container_identifiers {{
        entity_id
        asym_ids
        auth_asym_ids
        uniprot_ids
        reference_sequence_identifiers {{
          database_accession
        }}
      }}
      uniprots {{
        rcsb_id
        rcsb_uniprot_protein {{
          source_organism {{
            scientific_name
          }}
        }}
        rcsb_uniprot_external_reference {{
          reference_name
          reference_id
        }}
      }}
      rcsb_polymer_entity {{
        pdbx_description
        rcsb_ec_lineage {{
          id
        }}
        pdbx_ec
        rcsb_enzyme_class_combined {{
          ec
          provenance_source
        }}
      }}
      rcsb_polymer_entity_annotation {{
        type
        annotation_lineage {{
          name
          depth
        }}
      }}
      entity_poly {{
        type
        rcsb_entity_polymer_type
        pdbx_seq_one_letter_code_can
        rcsb_sample_sequence_length
        rcsb_mutation_count
      }}
      rcsb_entity_source_organism {{
        scientific_name
        ncbi_scientific_name
        rcsb_gene_name {{
          value
          provenance_source
        }}
      }}
      rcsb_entity_host_organism {{
        scientific_name
        ncbi_scientific_name
      }}
      prd {{
        rcsb_id
        pdbx_reference_molecule {{
          prd_id
          chem_comp_id
          name
          type
          class
        }}
      }}
      chem_comp_nstd_monomers {{
        chem_comp {{
          id
          name
          formula
          type
          mon_nstd_parent_comp_id
        }}
      }}
    }}
  }}
}}
'''
