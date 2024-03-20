from conf import *
from utils.api_PDB import *

def check_unknown_PDB():
    # Read the list of PDB entries
    file = open(unknown_PDB_list, "r")
    PDB_list = []
    for line in file.readlines():
        PDB_list.append(line[:4])
    file.close()

    # Check the PDB entries. 
    # The main purpose is to count the "Organism" systems. 
    # If it is two, then the chains can be divided into two groups.
    cnt = 0
    for PDB in PDB_list:
        entry_dict, expression_systems_entity_id = ask_RCSB_PDB(PDB)
        # if len(expression_systems_entity_id) == 2:
        #     print(f"Entry {PDB} has two expression systems: {expression_systems_entity_id}")
        if len(expression_systems_entity_id) != 2:
            cnt += 1
    print(f"Number of PDB entries with more than two expression systems: {cnt}")

    return

check_unknown_PDB()
