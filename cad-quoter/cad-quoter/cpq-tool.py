import OCC.Core.GProp as GProp
import OCC.Core.BRepGProp as BRepGProp
from OCC.Extend.DataExchange import read_step_file

fname = "cad-test-files/nist_ctc_01_asme1_ap242-e1.stp"


## works for injection molding

#cycle time x run time


# data base for alu elements / parts (e.g., tube)

# Load CAD file
# Calculate the mass of each material
# Look up unit price
# Yield total material cost


# add labor cost 
# look up machining process (?)


# add margin
# Backsolve



# ------

# Load the STEP file
shape = read_step_file(fname)

# Dictionary to store material data
material_volumes = {}
material_masses = {}

# Iterate through the topological shapes in the file
for i in range(shape.NbChildren()):
    child = shape.Child(i)

    # Get material name
    material_name = child.GetMaterial().Name()

    # Calculate volume
    prop = GProp.GProps()
    tolerance = 1e-6  # Adjust tolerance as needed
    BRepGProp.brepgprop_VolumeProperties(child, prop, tolerance)
    volume = prop.Mass()

    # Store volume and calculate mass (assuming density is known)
    material_volumes.setdefault(material_name, 0)
    material_volumes[material_name] += volume
    density = get_material_density(material_name)  # Function to retrieve density
    material_masses[material_name] = density * volume

# Print the results
print("Material Volumes:")
print(material_volumes)
print("Material Masses:")
print(material_masses)