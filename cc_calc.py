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
        self.react_col_list = self.react_table.columns.tolist()
        self.target_col_list = self.target_table.columns.tolist()
        self.react_data_type_list = [str, float, str, str, float, float, float, float, float]
        self.target_data_type_list = [str, float, str, float, float, float]

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

    ## ----------------------- Helper functions -----------------------------##

    # For the initial version of this calculator, with regard to the order of
    # precedence it is assumed that the mols are usually supplied, as it is a
    # necessary convention in official ACS Experimental section writing.
    # Some edge cases for when the mols are not supplied are taken care of.
    # The for a solution wt.% the lit_mass is the mass of the solution used in
    # the literature as input by the solution. However the calc_lit_mass is the
    # mass of the reactant dissolved in a sol wt.%. Therefor the calc_lit_mass
    # must be converted back to wieght of the solution when displayed to the
    # user.


    def calculate_lit_mass(self):
        ''' This assumes that the number of mols is always known. '''

        conditions = [
        ((self.react_table['phase']!='Solution (wt.%)') & (self.react_table['phase']!='Solution') & (pd.notna(self.react_table['lit_mass']))), # Mass already supplied and not sol wt.% [solid or liquid]
        (pd.notna(self.react_table['lit_mol'])), # Mass not supplied, mols are [any]
        ((self.react_table['phase']=='Liquid') & (pd.notna(self.react_table['lit_vol'])) & (pd.notna(self.react_table['density']))), # No Mass or mols supplied [liquid]
        ((self.react_table['phase']=='Solution (wt.%)') & (pd.notna(self.react_table['lit_vol'])) & (pd.notna(self.react_table['density'])) & (pd.notna(self.react_table['lit_conc']))), # [sol wt.% with volume]
        ((self.react_table['phase']=='Solution (wt.%)') & (pd.notna(self.react_table['lit_mass'])) & (pd.notna(self.react_table['lit_conc']))), # [sol wt.% with mass]
        ]

        results = [
        (self.react_table['lit_mass']), # Mass already supplied
        (self.react_table['lit_mol'] * self.react_table['mr']), # Calculating from mol * mr [solid or liquid]
        (self.react_table['lit_vol'] * self.react_table['density']), # Calculating from volume and density [any]
        (self.react_table['lit_vol'] * self.react_table['density'] * (self.react_table['lit_conc'] / 100)), # [sol wt.% with volume]
        (self.react_table['lit_mass'] * (self.react_table['lit_conc'] / 100)), # [sol wt.% with mass]
        ]

        self.react_table['calc_lit_mass'] = np.select(conditions, results)

    def calculate_lit_vol(self):
        ''' This assumes that the number of mols is always known. '''
        conditions = [
        (pd.notna(self.react_table['lit_vol'])), # Volume already supplied [any]
        ((self.react_table['phase']=='Liquid') & (pd.notna(self.react_table['density'])) & (pd.notna(self.react_table['calc_lit_mass']))), # Volume not supplied [liquid]
        ((self.react_table['phase']=='Solution') & (pd.notna(self.react_table['lit_mol'])) & (pd.notna(self.react_table['lit_conc']))), # mols and conc supplied [solution]
        ((self.react_table['phase']=='Solution (wt.%)') & (pd.notna(self.react_table['calc_lit_mass'])) & (pd.notna(self.react_table['density'])) & (pd.notna(self.react_table['lit_conc']))), # mass and density and conc [sol wt.%]
        ]

        results = [
        (self.react_table['lit_vol']), # Volume already supplied [any]
        (self.react_table['calc_lit_mass'] / self.react_table['density']), # Calculateing from mass / density [liquid]
        (self.react_table['lit_mol'] / (self.react_table['lit_conc'] * 1000)), # Calculating from mol / concentration * 1000 (to get L -> mL) [solution]
        (self.react_table['calc_lit_mass'] / self.react_table['lit_conc'] / self.react_table['density']), # [sol wt.%]
        ]

        self.react_table['calc_lit_vol'] = np.select(conditions, results)

    def calculate_lit_mol(self):
        ''' This assumes that the number of mols is likely always known.
            Accounting for some cases where it is not.'''
        conditions = [
        (pd.notna(self.react_table['lit_mol'])), # Mols already supplied
        ((pd.notna(self.react_table['calc_lit_mass'])) & (pd.notna(self.react_table['mr']))), # Mols not supplied (unlikely), mass already calculated [any]
        ((pd.notna(self.react_table['calc_lit_vol'])) & (pd.notna(self.react_table['density']))), # vol and density supplied [liquid]
        ((pd.notna(self.react_table['calc_lit_vol'])) & (pd.notna(self.react_table['lit_conc']))), # vol and molar supplied [solution]
        ]

        results = [
        (self.react_table['lit_mol']), # Mols already supplied
        (self.react_table['calc_lit_mass'] / self.react_table['mr']), # Calculating from mass / mr
        (self.react_table['calc_lit_vol'] * self.react_table['density'] / self.react_table['mr']), # calculating from vol * density / mr
        (self.react_table['calc_lit_vol'] * (self.react_table['lit_conc'] / 1000)), # Calculating from vol * conc (/1000 L -> mL)
        ]

        self.react_table['calc_lit_mol'] = np.select(conditions, results)

    ## ----------------------- Helper functions end -------------------------##

    def complete_react_table(self):
        ''' Wrapper method that runs helper functions in dependency order;
            assuming the number of mols is known for each reactant.'''

        self.calculate_lit_mass()
        self.calculate_lit_vol()
        self.calculate_lit_mol()

        print(f"React table:\n{self.react_table}\n")
        print(f"Target table:\n{self.target_table}\n")

    def calculate(self):
        ''' Method to calculate display data '''

        # Step 1: Calculating key information
        # Target mass and mol accounting for literature product yield
        self.target_mass = self.target_table['desired_mass'] / (self.target_table['lit_yield'] / 100) # column = column / column
        self.target_mol = self.target_mass / self.target_table['mr'] # column = column / column

        # Calculating scale factor for reactants
        self.scale_factor = self.target_mol / self.target_table['lit_mol'] # column = column / column
        self.scale_factor = self.scale_factor.iloc[0] # column -> value

        # finding lowest quantity reactant name(s) and thier number of mols as a list and value resp.
        self.reactants = self.react_table.loc[self.react_table['role'] == 'Reactant'] # column
        self.smallest_num_mol = self.reactants['calc_lit_mol'].min() # value

        # NOTE: These quantities below are calculated for a 'identify limiting reagent' feature,
        # potentially to be implemented later.
        self.lowest_quantity_reactant_data = self.reactants.loc[self.reactants['calc_lit_mol'] == self.smallest_num_mol]
        self.lowest_quantity_reactant_names = self.lowest_quantity_reactant_data['name'].tolist()




        # Step 2: Storing product display data stright into a dictionary to be returned to the UI
        # RETURNED DATA TO UI
        self.product_display_results_dict = {'target_mass' : self.target_mass.iloc[0], # column -> value
                                        'target_mol' : self.target_mol.iloc[0]} # column -> value





        # Step 3: Generating dataframe to store reactant display results first before we return it
        # to the UI as a dictionary
        self.reactant_display_results = pd.DataFrame(index=self.react_table.index.tolist(),
                                            columns=['molar_ratio', 'mols', 'mass', 'vol'])

        # Fill reactant display dataframe
        self.reactant_display_results['molar_ratio'] = self.react_table['calc_lit_mol'] / self.smallest_num_mol
        self.reactant_display_results['mols'] = self.react_table['calc_lit_mol'] * self.scale_factor

        cond = [
                (self.react_table['phase'] == 'Solution (wt.%)'), # It is sol wt.%
                (self.react_table['phase'] != 'Solution (wt.%)'), # It is not sol wt.%
                ]

        res = [
                (self.react_table['calc_lit_mass'] / (self.react_table['lit_conc'] / 100) * self.scale_factor), # converting mass of reactant in solution back to mass of whole sol
                (self.react_table['calc_lit_mass'] * self.scale_factor),
                ]
        self.reactant_display_results['mass'] = np.select(cond, res)

        self.reactant_display_results['vol'] = self.react_table['calc_lit_vol'] * self.scale_factor

        # Convert reactant display dataframe to dictionary
        # RETURNED DATA TO UI
        self.reactant_display_results_dict = self.reactant_display_results.to_dict()

        # NOTE: Could also put in stoichimetric ratios as an optional input,
        # from which we can determine the limiting reagent.

        print(self.reactant_display_results_dict)
        print(self.product_display_results_dict)















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
