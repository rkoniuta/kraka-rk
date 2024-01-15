## Program Logic

# Load STP (CAD) file # QQ: seeing a lot of PDF files. Is it realistic to expect CAD exports?

# Iterate through all components in the file & extract metadata:
# - Volume properties
# - Mass & density properties
# - Orientation vectors
# - Material metadata
# - Machining metadata
# - Color (for visualization)

# Create UI visualization
# - Export to WebGL browser viewer
# - Paint shapes  
# - Set scene & allow scroll

# Based on orientability vectors, calculate if the shape is:
# - Based on a base piece (e.g., pipe, sheet)
# - Custom component
# Backend: lookup material price while trying to minimize wastage (to do: find common component pricing from raw materials vendors)

# If material meta-data is not tagged, request input from user:
# - Which material
# QQ: is it safe to assume that most projects are single metal? or are they mixed metal

# If machining meta-data is not tagged, request input from user on each piece:
# - Which type of machine they intend to use
# - Duration of work
# Backend: lookup expected labor costs associated with machining (to do: ??? is this based on technician prices?)
# Request labor required between pieces: e.g., soldering / joining two components / final finishing

# Allow additional customization
# - Part name
# - Part finish

# Request other ordering data
# MOQ
# Salary & admin costs
# Packaging costs # QQ: How to estimate?
# Margin on order # QQ: What is typical?

# Export costing invoice
# Unit material cost
# Unit manufacturing cost
# Unit packaging costs
# Salary & admin costs
# Total unit cost
# Total order cost

## Other to dos:
# Request free trial of costimator
# Set up demo with other should cost suppliers



from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_SOLID

import shutup
shutup.please()

step_reader = STEPControl_Reader()
step_reader.ReadFile('./test-files/test2.stp')
step_reader.TransferRoot()
myshape = step_reader.Shape()

prop = GProp_GProps()
tolerance = 1e-5 # Adjust to your liking

# volume = brepgprop_VolumeProperties(myshape, prop, tolerance)
# print(volume)

topExp = TopExp_Explorer()
topExp.Init(myshape, TopAbs_SOLID)

while topExp.More():
    curr_shape = topExp.Current()
    volume_props = GProp_GProps()
    brepgprop_VolumeProperties(curr_shape, volume_props, tolerance)
    volume = volume_props.Mass()
    
    print(volume)

    topExp.Next()


# from OCC.Core.GProp import GProp_GProps
# from OCC.Core.BRepGProp import brepgprop_VolumeProperties
# from OCC.Extend.DataExchange import read_step_file

# my_shape = read_step_file('./test-files/test1.stp')
# prop = GProp_GProps()
# tolerance = 1e-5 # Adjust to your liking

# volume = brepgprop_VolumeProperties(my_shape, prop, tolerance)
# print(volume)


