import pandas as pd
import numpy as np


class Calculator():
    """Class for Calculator using pandas dataframe."""

    def __init__(self, compound_properties_list=None, target_properties=None):
        # Taking input compounds (list of dicts) and target product properties
        # (dict)

        # Dealing with mutable data-type arguments in constructor
        if not compound_properties_list:
            self.compound_properties_list = []
        else:
            self.compound_properties_list = compound_properties_list

        if not target_properties:
            self.target_properties = []
        else:
            self.target_properties = target_properties

        # Setting up dataframe of reactant compounds by passing DataFrame()
        # function a list of dictionaries. All entries in the dataframe are
        # currently strings.
        self.table = pd.DataFrame(compound_properties_list)

        # Converting empty string values to 'NaN type' (This applies to all
        # reactant property entries but inputs will not be allowed that do not
        # have necessary properties filled [compound name, role, mr and phase])
        self.table = self.table.replace('', np.NaN, regex=True)

        # Casting data frame colums to correct datatypes (strings and high
        # precision floats)
        # # NOTE: string columns are casting to 'object' dtype
        self.col_list = self.table.columns.tolist()
        self.data_type_list = [str, str, float, float, str, float, float, float, float]

        self.convert_dict = dict(zip(self.col_list, self.data_type_list))
        self.table = self.table.astype(self.convert_dict)




## ------------------------------- Test space -------------------------------##
comp_1 = {"name" : 'A',
        "role" : 'Solvent',
        "mr" : '1',
        "density" : '',
        "phase" : 'Solid',
        "lit_mass" : '3',
        "lit_vol" : '4',
        "lit_conc" : '5',
        "lit_mol" : '6',
        }

comp_2 = {"name" : 'B',
        "role" : 'Solvent',
        "mr" : '1',
        "density" : '2',
        "phase" : 'Solid',
        "lit_mass" : '',
        "lit_vol" : '4',
        "lit_conc" : '5',
        "lit_mol" : '6',
        }

lst = [comp_1, comp_2]

test = Calculator(lst)
test.table
