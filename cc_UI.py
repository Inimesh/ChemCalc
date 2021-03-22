from tkinter import *
from tkinter import ttk

##--------------- Setting up main window ------------------------------------##
root = Tk()
root.title("ChemCalc")

# Reagents frame
reagents_frame = LabelFrame(root, text="Reactants (literature values)")
reagents_frame.grid(row=0, column=0, columnspan=2)


# Grid labels
compound_name_label = Label(reagents_frame, padx=20, text="Compound Name")
role_label = Label(reagents_frame, text="Role")
mr_label = Label(reagents_frame, text= "Mr /g mol\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}")
density_label = Label(reagents_frame, text="Density /g mL\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}")
phase_label = Label(reagents_frame, text="Phase")

lit_mass_label = Label(reagents_frame, text="lit. Mass /g\n(precalculated %wt)")
lit_vol_label = Label(reagents_frame, text="lit. Vol /mL")
lit_conc_label = Label(reagents_frame, text="Concentration /M")
lit_mol_label = Label(reagents_frame, text="lit. Mols")


# Grid label placement
compound_name_label.grid(row=0, column=1)
role_label.grid(row=0, column=2)
mr_label.grid(row=0, column=3)
density_label.grid(row=0, column=4)
phase_label.grid(row=0, column=5)

lit_mass_label.grid(row=0, column=6)
lit_vol_label.grid(row=0, column=7)
lit_conc_label.grid(row=0, column=8)
lit_mol_label.grid(row=0, column=9)



##--------------- Compound entry --------------------------------------------##
class Compound:
    """Class that defines an entry of a compound into the grid.
    Each instance of this class is a new compound with its own fields"""
    # Class variable containing list of instances
    compound_list = []

    # Drop down menu config
    role_options = [
    "Reagent",
    "Solvent",
    "Catalyst",
    ]

    phase_options = [
    "Solid",
    "Liquid",
    "Solution",
    ]

    # Class variables for layout
    field_width = 18
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
        self.role_entry = ttk.Combobox(reagents_frame, values=Compound.role_options, justify='center', state='readonly')
        self.role_entry.set("Select Role")
        self.mr_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.density_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.phase_entry = ttk.Combobox(reagents_frame, values=Compound.phase_options, justify='center', state='readonly')
        self.phase_entry.set("Select Phase")
        self.lit_mass_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.lit_vol_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.lit_conc_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')
        self.lit_mol_entry = Entry(reagents_frame, width=Compound.field_width, justify='center')

        # storing property entries in dictionary so they can be easily removed
        # when required
        self.properties_entry = {"name" : self.name_entry,
                                "role" : self.role_entry,
                                "mr" : self.mr_entry,
                                "density" : self.density_entry,
                                "phase" : self.phase_entry,
                                "lit_mass" : self.lit_mass_entry,
                                "lit_vol" : self.lit_vol_entry,
                                "lit_conc" : self.lit_conc_entry,
                                "lit_mol" : self.lit_mol_entry,
                                }


    # Compound entry layout + name updater
    def compound_entry_updater(self):
        ''' Updates input field positions for a compound'''
        if not self.removed:
            ## updates position of fields and buttons
            # Entry field positions
            self.name_entry.grid(row=Compound.compound_list.index(self)+1, column=1)
            self.role_entry.grid(row=Compound.compound_list.index(self)+1, column=2)
            self.mr_entry.grid(row=Compound.compound_list.index(self)+1, column=3)
            self.density_entry.grid(row=Compound.compound_list.index(self)+1, column=4)
            self.phase_entry.grid(row=Compound.compound_list.index(self)+1, column=5)
            self.lit_mass_entry.grid(row=Compound.compound_list.index(self)+1, column=6)
            self.lit_vol_entry.grid(row=Compound.compound_list.index(self)+1, column=7)
            self.lit_conc_entry.grid(row=Compound.compound_list.index(self)+1, column=8)
            self.lit_mol_entry.grid(row=Compound.compound_list.index(self)+1, column=9)

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

# TODO: Configure the target compound frame
target_frame = LabelFrame(root, text="Target Compound")
target_frame.grid(sticky='W', row=4, column=0)

# Input labels
target_compound_name_label = Label(target_frame, padx=20, text="Product Name")
target_mr_label = Label(target_frame, text= "Mr /g mol\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}")
target_phase_label = Label(target_frame, text="Phase")
target_desired_mass_label = Label(target_frame, text="Desired mass /g")
target_product_lit_yield_label = Label(target_frame, text="lit. yield /%")


# Input labels positioning
target_compound_name_label.grid(row=0, column=0)
target_mr_label.grid(row=0, column=1)
target_phase_label.grid(row=0, column=2)
target_desired_mass_label.grid(row=0, column=3)
target_product_lit_yield_label.grid(row=0, column=4)


# Input entry fields
target_compound_name_entry = Entry(target_frame, width=Compound.compound_name_width)
target_mr_entry = Entry(target_frame, width=Compound.field_width, justify='center')
target_phase_entry = ttk.Combobox(target_frame, values=Compound.phase_options, justify='center', state='readonly')
target_phase_entry.set("Select Phase")
target_desired_mass_entry = Entry(target_frame, width=Compound.field_width, justify='center')
target_product_lit_yield_entry = Entry(target_frame, width=Compound.field_width, justify='center')

# Input entry fields positioning
target_compound_name_entry.grid(row=1, column=0)
target_mr_entry.grid(row=1, column=1)
target_phase_entry.grid(row=1, column=2)
target_desired_mass_entry.grid(row=1, column=3)
target_product_lit_yield_entry.grid(row=1, column=4)



##--------------- Below target compound frame -------------------------------##

##--------------- Calculation -----------------------------------------------##

# Calculate button will set the input attributes of each compound and the target
# product

# Calculate button function
def calculate():
    # Setting attribute values as strings for each compound instance
    for compound in Compound.compound_list:
        compound.name = compound.properties_entry["name"].get()
        compound.mr = compound.properties_entry["mr"].get()
        if compound.properties_entry["role"].get() == 'Select Role':
            compound.role = ''
        compound.density = compound.properties_entry["density"].get()
        if compound.properties_entry["phase"].get() == 'Select Phase':
            compound.phase = ''
        compound.lit_mass = compound.properties_entry["lit_mass"].get()
        compound.lit_vol = compound.properties_entry["lit_vol"].get()
        compound.lit_conc = compound.properties_entry["lit_conc"].get()
        compound.lit_mol = compound.properties_entry["lit_mol"].get()

        # Storing compound properites in a dictionary for easy access
        compound.properties = {"name" : compound.name,
                                "role" : compound.role,
                                "mr" : compound.mr,
                                "density" : compound.density,
                                "phase" : compound.phase,
                                "lit_mass" : compound.lit_mass,
                                "lit_vol" : compound.lit_vol,
                                "lit_conc" : compound.lit_conc,
                                "lit_mol" : compound.lit_mol,
                                }


    target_properties = {"name" : target_compound_name_entry.get(),
                            "mr" : target_mr_entry.get(),
                            "phase" : target_phase_entry.get(),
                            "desired_mass" : target_desired_mass_entry.get(),
                            "lit_yield" : target_product_lit_yield_entry.get(),
                            }

    # Debugging print statements
    for compound in Compound.compound_list:
        print(compound.properties)
    print(target_properties)

    # Passing input data to calculator class.

    # TODO: Create Calculator class to set up dataframe and perform conditional
    # calculations
    # results = Calculator(Compound.compound_list, target_properties):

##--------------- Calculate button ------------------------------------------##

# Calculate button declaration and position
calculate_button = Button(root, text="Calculate", command=calculate)
calculate_button.grid(sticky='W', row=4, column=1)

##--------------- Render output ---------------------------------------------##

# TODO: Create new window with display and save and print option?

### lAYOUT

## Reagents frame
# OUTPUT HERE

## Target compound frame
# Output labels
target_mass_lit_yield_label = Label(target_frame, text="Target mass\n(accounting for lit. yield) /g")
target_mol_label = Label(target_frame, text="Target mol")
# Output labels positioning
target_mass_lit_yield_label.grid(row=0, column=5)
target_mol_label.grid(row=0, column=6)

# Output text
target_mass_lit_yield = Label(target_frame, padx=73, text="", borderwidth=2, relief='solid')
target_mol_label = Label(target_frame, padx=73, text="", borderwidth=2, relief='solid')
# Output text positioning
target_mass_lit_yield.grid(row=1, column=5)
target_mol_label.grid(row=1, column=6)

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
