from tkinter import *
from tkinter import ttk

from cc_calc import Calculator

##--------------- Setting up main window ------------------------------------##
root = Tk()
root.title("ChemCalc")

# Reagents frame
reagents_frame = LabelFrame(root, text="Reactants (literature values)")
reagents_frame.grid(row=0, column=0, columnspan=2)


# Grid labels
compound_name_label = Label(reagents_frame, padx=20, text="Compound Name")
mr_label = Label(reagents_frame, text= "Mr /g mol\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}")
phase_label = Label(reagents_frame, text="Phase")
role_label = Label(reagents_frame, text="Role")

lit_mass_label = Label(reagents_frame, text="lit. Mass /g")
lit_mol_label = Label(reagents_frame, text="lit. Mols")
lit_vol_label = Label(reagents_frame, text="lit. Vol /mL")
lit_conc_label = Label(reagents_frame, text="Concentration\n/M (or wt.%)")
density_label = Label(reagents_frame, text="Density /g mL\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}")


# Grid label placement
compound_name_label.grid(row=0, column=1)
mr_label.grid(row=0, column=2)
phase_label.grid(row=0, column=3)
role_label.grid(row=0, column=4)

lit_mass_label.grid(row=0, column=5)
lit_mol_label.grid(row=0, column=6)
lit_vol_label.grid(row=0, column=7)
lit_conc_label.grid(row=0, column=8)
density_label.grid(row=0, column=9)



##--------------- Compound entry --------------------------------------------##
class Compound:
    """Class that defines an entry of a compound into the grid.
    Each instance of this class is a new compound with its own fields"""
    # Class variable containing list of instances
    compound_list = []

    # Drop down menu config
    role_options = [
    "Reactant",
    "Solvent",
    "Catalyst",
    ]

    phase_options = [
    "Solid",
    "Liquid",
    "Solution",
    "Solution (wt.%)"
    ]

    # Class variables for layout
    field_width = 15
    compound_name_width = 30

    # Class methods
    @classmethod
    def GUI_update(cls):
        ''' Runs compound_entry_updater method for every compound created '''
        for compound in cls.compound_list:
            compound.compound_entry_updater()

    ## -------- Compound instance -------- ##
    def __init__(self):

        # Specifiying that the compound is not yet removed
        self.removed = False
        # Add instance to the compound_list class variable
        Compound.compound_list.append(self)

        # Set up remove compound button
        self.remove_compound_button = Button(reagents_frame, text="Remove compound", command=self.remove_compound)


        # Set up entry fields
        self.name_entry = Entry(reagents_frame, width=Compound.compound_name_width)
        self.mr_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.phase_entry = ttk.Combobox(reagents_frame, values=Compound.phase_options, justify='center', state='readonly', width=Compound.field_width)
        self.phase_entry.set("Select Phase")
        self.role_entry = ttk.Combobox(reagents_frame, values=Compound.role_options, justify='center', state='readonly', width=Compound.field_width)
        self.role_entry.set("Select Role")

        self.lit_mass_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.lit_mol_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.lit_vol_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.lit_conc_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.density_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')

        # storing property entries in dictionary so they can be easily removed
        # when required
        self.properties_entry = {"name" : self.name_entry,
                                "mr" : self.mr_entry,
                                "phase" : self.phase_entry,
                                "role" : self.role_entry,
                                "lit_mass" : self.lit_mass_entry,
                                "lit_mol" : self.lit_mol_entry,
                                "lit_vol" : self.lit_vol_entry,
                                "lit_conc" : self.lit_conc_entry,
                                "density" : self.density_entry,
                                }


    # Compound entry layout + name updater
    def compound_entry_updater(self):
        ''' Updates input field positions for a compound'''
        if not self.removed:
            ## updates position of fields and buttons
            # Entry field positions
            self.name_entry.grid(row=Compound.compound_list.index(self)+1, column=1)
            self.mr_entry.grid(row=Compound.compound_list.index(self)+1, column=2)
            self.phase_entry.grid(row=Compound.compound_list.index(self)+1, column=3)
            self.role_entry.grid(row=Compound.compound_list.index(self)+1, column=4)
            self.lit_mass_entry.grid(row=Compound.compound_list.index(self)+1, column=5)
            self.lit_mol_entry.grid(row=Compound.compound_list.index(self)+1, column=6)
            self.lit_vol_entry.grid(row=Compound.compound_list.index(self)+1, column=7)
            self.lit_conc_entry.grid(row=Compound.compound_list.index(self)+1, column=8)
            self.density_entry.grid(row=Compound.compound_list.index(self)+1, column=9)

            # Position 'remove compound' button
            self.remove_compound_button.grid(row=Compound.compound_list.index(self)+1, column = 0)
            # set compound button to "disabled" if it is the only compound entry
            if len(Compound.compound_list) < 2:
                self.remove_compound_button["state"] = DISABLED
            else:
                self.remove_compound_button["state"] = NORMAL

            # Updates name of compound
            self.name = "compound_"+ str(Compound.compound_list.index(self))


    # Remove compound button functionality
    def remove_compound(self):
        # remove entry fields
        for entry in self.properties_entry:
            self.properties_entry[entry].destroy()

        # Removing remove compound button
        self.remove_compound_button.destroy()

        # remove compound reference from list
        Compound.compound_list.remove(self)

        # delete self
        self.removed = True
        del self
        # Run update
        Compound.GUI_update()
        print(Compound.compound_list)

    # Representing each compound as its input name
    def __repr__(self):
        return self.name


##--------------- Below Reagents frame --------------------------------------##

# Buttons
def add_compound():
    new_compound = Compound()
    Compound.GUI_update()
    print(Compound.compound_list)
add_compound_button = Button(root, text="Add compound", command=add_compound)
add_compound_button.grid(sticky='W', row=1, column=0, padx=12, pady=5)
##--------------- reagent frame/target frame spacer -------------------------------------##

spacer = Label(root, text="")
spacer.grid(sticky="W", row=3, column=0)

##--------------- Target compound frame -------------------------------------##

target_frame = LabelFrame(root, text="Target Compound")
target_frame.grid(sticky='W', row=4, column=0)

# Input labels
target_compound_name_label = Label(target_frame, padx=20, text="Product Name")
target_mr_label = Label(target_frame, text= "Mr /g mol\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}")
target_lit_mol_label = Label(target_frame, text="lit. mols of\nproduct /mol")
target_product_lit_yield_label = Label(target_frame, text="lit. yield /%")
desired_quantity_options = ["Desired mols", "Desired mass /g"]
target_desired_quantity_label = ttk.Combobox(target_frame, values=desired_quantity_options , justify='center', state='readonly', width=Compound.field_width)
target_desired_quantity_label.set("Desired quantity")

# Input labels positioning
target_compound_name_label.grid(row=0, column=0)
target_mr_label.grid(row=0, column=1)
target_lit_mol_label.grid(row=0, column = 2)
target_product_lit_yield_label.grid(row=0, column=3)
target_desired_quantity_label.grid(row=0, column=4)


# Input entry fields
target_compound_name_entry = Entry(target_frame, width=Compound.compound_name_width)
target_mr_entry = Entry(target_frame, width=Compound.field_width, justify='center')
target_lit_mol_entry = Entry(target_frame, width=Compound.field_width, justify='center')
target_product_lit_yield_entry = Entry(target_frame, width=Compound.field_width, justify='center')
target_desired_quantity_entry = Entry(target_frame, width=Compound.field_width+4, justify='center')

# Input entry fields positioning
target_compound_name_entry.grid(row=1, column=0)
target_mr_entry.grid(row=1, column=1)
target_lit_mol_entry.grid(row=1, column=2)
target_product_lit_yield_entry.grid(row=1, column=3)
target_desired_quantity_entry.grid(row=1, column=4)



##--------------- Below target compound frame -------------------------------##

##--------------- Calculation -----------------------------------------------##

# Calculate button will set the input attributes of each compound and the target
# product

# TODO: Do not let calculator submission without all name, role, mr and phase
# entries


# Calculate button function
def calculate():
    # Creating empty list to store compound property dictionaries
    compound_properties_list = []
    # Setting attribute values as strings for each compound instance
    for compound in Compound.compound_list:
        compound.name = compound.properties_entry["name"].get()
        compound.mr = compound.properties_entry["mr"].get()
        if compound.properties_entry["phase"].get() == 'Select Phase':
            compound.phase = ''
        else:
            compound.phase = compound.properties_entry["phase"].get()
        if compound.properties_entry["role"].get() == 'Select Role':
            compound.role = ''
        else:
            compound.role = compound.properties_entry["role"].get()
        compound.lit_mass = compound.properties_entry["lit_mass"].get()
        compound.lit_mol = compound.properties_entry["lit_mol"].get()
        compound.lit_vol = compound.properties_entry["lit_vol"].get()
        compound.lit_conc = compound.properties_entry["lit_conc"].get()
        compound.density = compound.properties_entry["density"].get()

        # Storing compound properites in a dictionary for easy access
        compound.properties = {"name" : compound.name,
                                "mr" : compound.mr,
                                "phase" : compound.phase,
                                "role" : compound.role,
                                "lit_mass" : compound.lit_mass,
                                "lit_mol" : compound.lit_mol,
                                "lit_vol" : compound.lit_vol,
                                "lit_conc" : compound.lit_conc,
                                "density" : compound.density,
                                }

        # Storing dictionaries in a list to be passed to calculator
        compound_properties_list.append(compound.properties)

    # Ensuring 'name', 'mr', 'pahse', and 'role' options are filled before
    # calculation
    valid = True
    for prop in compound_properties_list:
        if "" in (prop["name"], prop["mr"], prop["phase"], prop["role"]):
            valid = False
            invalid_issue = "compound_issue"

    # Storing compound properites in a dictionary for easy accesss. Will be
    # passed to calculator.
    if valid:
        # Checking required input for target compound
        if target_desired_quantity_label.get() == "Desired quantity":
            target_desired_quantity_holder = ""
        else:
            target_desired_quantity_holder = target_desired_quantity_label.get()

        target_properties = {"name" : target_compound_name_entry.get(),
                            "mr" : target_mr_entry.get(),
                            "lit_mol" : target_lit_mol_entry.get(),
                            "lit_yield" : target_product_lit_yield_entry.get(),
                            "desired_quantity" : target_desired_quantity_entry.get(),
                            "desired_quantity_unit" : target_desired_quantity_holder,
                            }

        # Checking for all required input supplied in target product section
        for prop in target_properties:
            if target_properties[prop] == "":
                valid = False
                invalid_issue = "product_issue"

    if valid:
        # Passing input data to calculator class.
        calculator = Calculator(compound_properties_list, target_properties)
        # Reactant display data retrieved as a dictionary of dictionaries
        reactant_display_results_dict = calculator.reactant_display_results_dict
        # Product display data retrieved as a dictionary
        product_display_results_dict = calculator.product_display_results_dict

        ##--------------------- Displaying the results --------------------------##
        # Displaying reactant results in a new window

        # Setting up new window
        reactant_results_display_window = Tk()
        reactant_results_display_window.title("ChemCalc Results")

        # Creating frame in which to display results in new window
        reactant_display_frame = LabelFrame(reactant_results_display_window, text="Results", height=reagents_frame.winfo_height())
        reactant_display_frame.grid(row=0, column=0)

        result_compound_name_label = Label(reactant_display_frame, text="Compound name")
        result_molar_ratio_label = Label(reactant_display_frame, text="molar ratio")
        result_mols_label = Label(reactant_display_frame, text="mols")
        result_mass_label = Label(reactant_display_frame, text="mass")
        result_vol_label = Label(reactant_display_frame, text="vol")

        result_compound_name_label.grid(row=0, column=0)
        result_molar_ratio_label.grid(row=0, column=1)
        result_mols_label.grid(row=0, column=2)
        result_mass_label.grid(row=0, column=3)
        result_vol_label.grid(row=0, column=4)

        # Compound results display options
        compound_result_pady = 3
        result_precision = 5

        for index, compound in enumerate(Compound.compound_list):
            # Looping through each compound in the compound list to get the index of each
            # and applying display options including dp precision.
            result_compound_name = Label(reactant_display_frame, text=compound.properties['name'], pady=compound_result_pady)
            result_molar_ratio = Label(reactant_display_frame, text=round(reactant_display_results_dict['molar_ratio'][index], result_precision), pady=compound_result_pady)
            result_mols = Label(reactant_display_frame, text=round(reactant_display_results_dict['mols'][index], result_precision), pady=compound_result_pady)
            result_mass = Label(reactant_display_frame, text=round(reactant_display_results_dict['mass'][index], result_precision), pady=compound_result_pady)
            result_vol = Label(reactant_display_frame, text=round(reactant_display_results_dict['vol'][index], result_precision), pady=compound_result_pady)

            result_compound_name.grid(row=index+1, column=0)
            result_molar_ratio.grid(row=index+1, column=1)
            result_mols.grid(row=index+1, column=2)
            result_mass.grid(row=index+1, column=3)
            result_vol.grid(row=index+1, column=4)


        # Displaying product window results
        target_mass['text'] = round(product_display_results_dict['target_mass'], result_precision)
        target_mol['text'] = round(product_display_results_dict['target_mol'], result_precision)

    # If key input information is not supplied, a window will appear and the
    # calculation will not proceed.
    else:
        def okay_close_button_func():
            missing_input_window.destroy()
        missing_input_window = Tk()
        missing_input_window.title("Missing input")

        if invalid_issue == "compound_issue":
            invalid_txt = "Please ensure valid inputs are supplied for\n'Compound Name', 'Mr', 'Phase' and 'Role' attributes\nfor each compound"
        else:
            invalid_txt = "Please ensure valid inputs are supplied for\nall input fields including the 'Desired quantity' option"

        missing_input_text = Label(missing_input_window, relief='solid', text=invalid_txt)
        missing_input_text_okay_button = Button(missing_input_window, text='Okay', command=okay_close_button_func)

        missing_input_text.grid(row=0)
        spacer = Label(missing_input_window).grid(row=1)
        missing_input_text_okay_button.grid(row=2)





##--------------- Calculate button ------------------------------------------##


# Calculate button declaration and position
calculate_button = Button(root, text="Calculate", command=calculate)
calculate_button.grid(sticky='W', row=4, column=1)

##--------------- Target compound output init -------------------------------##

# TODO: Create new window with display and save and print option?

### lAYOUT

## Target compound frame
# Output labels
target_mass_label = Label(target_frame, text="Target mass\n(accounting for lit. yield) /g")
target_mol_label = Label(target_frame, text="Target mol")
# Output labels positioning
target_mass_label.grid(row=0, column=6)
target_mol_label.grid(row=0, column=7)

# Output text
target_mass = Label(target_frame, width=20, padx=3, text="", borderwidth=2, relief='solid')
target_mol = Label(target_frame, width=20, padx=3, text="", borderwidth=2, relief='solid')
# Output text positioning
target_mass.grid(row=1, column=6)
target_mol.grid(row=1, column=7)

##--------------- Initialisation --------------------------------------------##
start_compound = Compound()
Compound.GUI_update()

# Insert 'add compound' button
initial = True
if initial:
    add_compound_button.grid(row=len(Compound.compound_list)+1, column=0)
    initial = False

# Main Loop
root.mainloop()

# ------- Useful Debugging code -----------------------------#
# print(Compound.compound_list)
# print(f"length of list: {len(Compound.compound_list)}")
#
# info = add_compound_button.grid_info()
# print(f"Add button is located at: {(info['row'], info['column'])}")
