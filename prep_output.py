# Prep dictionaries for output json

import pandas as pd
import numpy as np
from glob import glob
import sys


def prep_output_dict(emu_mapping, map_conditions):
    # # # # # # # # # # # # # # # # #
    # Single (Un-grouped) h2i fields
    
    # Try filtering/appending fields into groups at end. Otherwise, include in each field-type loop [slow?]
    # TO DO: differentiate between data-types for repeatable [] and non-repeatable "" in schema; currently all repeatable []
    h2i_single_emu = emu_mapping[emu_mapping['h2i_container'].isnull()]['h2i_field'].values
    h2i_single_map = map_conditions[map_conditions['h2i_container'].isnull()]['h2i_field'].values

    single_dict = dict()
    for single_emu in h2i_single_emu:
        single_dict[single_emu] = []

    for single_map in h2i_single_map:
        single_dict[single_map] = []


    # # # # # # # # # # # # # # # # #
    # Grouped h2i fields
    h2i_groups = emu_mapping[emu_mapping['h2i_container'].notnull()]['h2i_container'].values
    # h2i_con_groups = map_condition['h2i_container'].values  # Safe to assume all container-values show in emu_map?

    for group_key in h2i_groups:
        h2i_group_emu = emu_mapping.query('h2i_container == @group_key')['h2i_field'].values
        h2i_group_maps = map_conditions.query('h2i_container == @group_key')['h2i_field'].values

        single_dict[group_key] = []

    return single_dict



# To run convert_xml.py directly, run:
#   python3 convert_xml.py file1 file2 etc
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            prep_output_dict(arg)