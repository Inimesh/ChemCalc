import numpy as np
import pandas as pd


class Calculator():
    """Class for Calculator using pandas dataframe."""

    def __init__(self, compound_properties_list=None, target_properties=None):
        # Taking input compounds (list of dicts) and target product properties
        # (dict) and forming them into formatted dataframes.

        # Dealing with mutable data-type arguments in constructor
        if not compound_properties_list:
            self.compound_properties_list = []
        else:
            self.compound_properties_list = compound_properties_list

        if not target_properties:
            self.target_properties = []
        else:
            self.target_properties = target_properties

        # Initialising the dataframes
        self.react_table = pd.DataFrame(compound_properties_list)
        self.target_table = pd.DataFrame([target_properties])

        # Converting empty string values to 'NaN type' (Applies to all
        # reactant and target property entries for smoother error handling but
        # inputs will not be allowed that do not have necessary properties
        # filled [compound name, role, mr and phase])
        self.react_table = self.react_table.replace('', np.NaN, regex=True)
        self.target_table = self.target_table.replace('', np.NaN, regex=True)

        # Casting data frame colums to correct datatypes (strings and high
        # precision floats)
        # # NOTE: string columns are casting to 'object' dtype but should not be
        # # a problem
        self.react_col_list = self.react_table.columns.tolist()
        self.target_col_list = self.target_table.columns.tolist()

        self.react_data_type_list = [str, str, float, float, str, float, float, float, float]
        self.target_data_type_list = [str, float, str, float, float]

        self.react_convert_dict = dict(zip(self.react_col_list, self.react_data_type_list))
        self.target_convert_dict = dict(zip(self.target_col_list, self.target_data_type_list))

        self.react_table = self.react_table.astype(self.react_convert_dict)
        self.target_table = self.target_table.astype(self.target_convert_dict)


        # Adding 'calculated lit values' to the reactant table. This is to hold
        # quantities needed for further calculation but not supplied by the user
        self.react_table = pd.concat([self.react_table,
        pd.DataFrame(columns=['calc_lit_mass',
                            'calc_lit_mol',
                            'calc_lit_vol',
                            'calc_lit_conc'])])

        # Once input data is set up:
        # The react table is completed as best as possible
        self.complete_react_table()

        # Calculate method is run to generate results
        self.calculate()

    def complete_react_table(self):
        ''' Wrapper method that runs helper functions in dependency order;
            assuming the number of mols is known for each reactant.'''

        self.calculate_lit_mass()
        self.calculate_lit_vol()
        self.calculate_lit_mol()


    def calculate(self):
        # Step 1: Calculating key information
        # Target mass and mol accounting for literature product yield
        self.target_mass = self.target_table['desired_mass'] / (self.target_table['lit_yield'] / 100)
        self.target_mol = self.target_mass / self.target_table['mr']

        # finding lowest quantity reactant name(s) and thier number of mols as a list and value resp.
        self.reactants = self.react_table.loc[self.react_table['role'] == 'Reactant']
        self.smallest_num_mol = self.reactants['calc_lit_mol'].min()

        self.lowest_quantity_reactant_data = self.reactants.loc[self.reactants['calc_lit_mol'] == self.smallest_num_mol]
        self.lowest_quantity_reactant_names = self.lowest_quantity_reactant_data['name'].tolist()

        # Step 2: Generating dataframe to store display results
        self.display_results = pd.DataFrame(index=self.react_table.index.tolist(),
                                            columns=['molar_ratio', 'mols', 'mass', 'vol'])

        # Fill display data
        self.display_results['molar_ratio'] = self.react_table['calc_lit_mol'] / self.smallest_num_mol

        # NOTE: Need to make a 'lit. product amount' entry in UI and target table
        # to calculate scaling factor for display result reagent amounts

        # NOTE: Could also put in stoichimetric ratios as an optional input,
        # from which we can determine the limiting reagent.

        print(self.display_results)








    ## ----------------------- Helper functions -----------------------------##

    # For the initial version of this calculator it is assumed that the mols
    # of each reactant are supplied by the user, as it is a necessary convention
    # in official ACS Experimental section writing.

    def calculate_lit_mass(self):
        ''' This assumes that the number of mols is always known. '''
        conditions = [
        (pd.notna(self.react_table['lit_mass'])), # Mass already supplied
        (pd.isna(self.react_table['lit_mass'])), # Mass not supplied
        ]

        results = [
        (self.react_table['lit_mass']), # Mass already supplied
        (self.react_table['lit_mol'] * self.react_table['mr']) # Calculating from mol * mr
        ]

        self.react_table['calc_lit_mass'] = np.select(conditions, results)

    def calculate_lit_vol(self):
        ''' This assumes that the number of mols is always known. '''
        conditions = [
        (pd.notna(self.react_table['lit_vol'])), # Volume already supplied
        (pd.isna(self.react_table['lit_vol']) & pd.notna(self.react_table['density']) & pd.notna(self.react_table['calc_lit_mass'])),
        ]

        results = [
        (self.react_table['lit_vol']), # Volume already supplied
        (self.react_table['calc_lit_mass'] / self.react_table['density']), # Calculateing from mass / density
        ]

        self.react_table['calc_lit_vol'] = np.select(conditions, results)

    def calculate_lit_mol(self):
        ''' This assumes that the number of mols is always known. '''
        conditions = [
        (pd.notna(self.react_table['lit_mol'])), # Mols already supplied
        ]

        results = [
        (self.react_table['lit_mol']), # Mols already supplied
        ]

        self.react_table['calc_lit_mol'] = np.select(conditions, results)

    ## ----------------------- Helper functions end -------------------------##







## ------------------------------- Test space -------------------------------##
# comp_1 = {"name" : 'A',
#         "role" : 'Solvent',
#         "mr" : '192',
#         "density" : '',
#         "phase" : 'Solid',
#         "lit_mass" : '3',
#         "lit_vol" : '4',
#         "lit_conc" : '5',
#         "lit_mol" : '6',
#         }
#
# comp_2 = {"name" : 'B',
#         "role" : 'Solvent',
#         "mr" : '123.55',
#         "density" : '2',
#         "phase" : 'Solid',
#         "lit_mass" : '',
#         "lit_vol" : '4',
#         "lit_conc" : '5',
#         "lit_mol" : '6',
#         }
#
# lst = [comp_1, comp_2]
#
# test = Calculator(lst)
# test.react_table
