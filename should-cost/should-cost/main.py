## Program Logic

# Load STP (CAD) file

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
# To do: check other formats
# QQ: seeing a lot of PDF files. Is it realistic to expect CAD exports? 


from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties

from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_SOLID
from OCC.Core.XCAFDoc import XCAFDoc_ShapeTool

from OCC.Extend.DataExchange import read_step_file

from OCC.Display.WebGl import threejs_renderer

import argparse
import shutup
import json

shutup.please()

OUTPUT_SPEC_TEMPLATE = "./test-inputs/template.json"
OUTPUT_QUOTE_TEMPLATE = "./output-quote-files/template.json"
MATERIAL_DEFAULT = "aluminium-raw"
INPUT_MACHINING = "./machining-lookup.json"
INPUT_MATERIALS = "./materials-lookup.json"

# from OCC.Display.WebGl import x3dom_renderer

# my_renderer = x3dom_renderer.X3DomRenderer()
# my_renderer.DisplayShape(myshape)
# my_renderer.render()

# from OCC.Core.GProp import GProp_GProps
# from OCC.Core.BRepGProp import brepgprop_VolumeProperties
# from OCC.Extend.DataExchange import read_step_file

# my_shape = read_step_file('./test-files/test1.stp')
# prop = GProp_GProps()
# tolerance = 1e-5 # Adjust to your liking

# volume = brepgprop_VolumeProperties(my_shape, prop, tolerance)
# print(volume)

def quote_from_json(ifname):

    with open(ifname, "r") as f:
        spec = json.load(f)

    with open(OUTPUT_QUOTE_TEMPLATE, "r") as f:
        quote = json.load(f)
    
    with open(INPUT_MACHINING, "r") as f:
        machining_lookup = json.load(f)

    with open(INPUT_MATERIALS, "r") as f:
        materials_lookup = json.load(f)

    raw_material_costs = 0
    machining_costs = 0

    for component in spec["component-costs"]:
        material = component['material']
        raw_cost = float(component["volume"]) / materials_lookup[material]["material-density-per-mm3"] * materials_lookup[material]["usd-cost-per-kg"] / 1000
        machining_cost = machining_lookup[component["machining"]["machine-type"]][component["machining"]["machine-spec"]] * component["machining"]["machine-hours"]
        
        raw_material_costs += raw_cost
        machining_costs += machining_cost
    
    assembly_costs = spec["assembly-costs"]["usd-assembly"]
    processing_cost = spec["post-processing-costs"]["usd-post-processing"]
    defect_rate = spec["quality-control-costs"]["defect-rate"]
    
    quality_control_cost = sum([
        raw_material_costs,
        machining_costs,
        assembly_costs,
        processing_cost,
    ]) * (defect_rate)

    margin = spec["margin-percent"]

    subtotal_without_margin = sum([
        raw_material_costs,
        machining_costs,
        assembly_costs,
        processing_cost,
        quality_control_cost
    ])

    subtotal_with_margin = subtotal_without_margin * (1+margin)

    quote["Total unit costs"]["Total with margin"] = subtotal_with_margin
    quote["Total unit costs"]["Total without margin"] = subtotal_without_margin
    quote["Manufacturing cost subtotal"]["Subtotal"] = raw_material_costs + machining_costs
    quote["Manufacturing cost subtotal"]["Component costs"]["Raw material costs"] = raw_material_costs
    quote["Manufacturing cost subtotal"]["Component costs"]["Machining costs"] = machining_costs
    quote["Assembly cost subtotal"] = assembly_costs
    quote["Post processing cost subtotal"] = processing_cost
    quote["Quality control cost subtotal"] = quality_control_cost

    ofname = ifname.replace("output-spec-files", "output-quote-files")

    with open(ofname, "w") as f:
        json.dump(quote, f, indent=4)
    
    print("Successful quoting")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QuotingTool")
    parser.add_argument("--read", type=str, help="x")
    parser.add_argument("--calculate", type=str, help="x")

    args = parser.parse_args()

    if args.read:
        step_reader = STEPControl_Reader()
        step_reader.ReadFile(args.read)
        step_reader.TransferRoot()
        myshape = step_reader.Shape()

        prop = GProp_GProps()
        tolerance = 1e-5

        fname = args.read.split(".stp")[0] + ".json"
        fname = fname.replace("files", "inputs")

        with open(OUTPUT_SPEC_TEMPLATE, "r") as f:
            template = json.load(f)

        with open(INPUT_MACHINING, "r") as f:
            machining_lookup = json.load(f)

        with open(INPUT_MATERIALS, "r") as f:
            materials_lookup = json.load(f)

        topExp = TopExp_Explorer()
        topExp.Init(myshape, TopAbs_SOLID)

        total_volume = 0

        vol_dict = dict()
        while topExp.More():
            curr_shape = topExp.Current()
            volume_props = GProp_GProps()
            brepgprop_VolumeProperties(curr_shape, volume_props, tolerance)
            volume = volume_props.Mass()

            if volume in vol_dict:
                vol_dict[volume] += 1
            else:
                vol_dict[volume] = 1

            topExp.Next()

        template['file-path'] = fname

        for h in list(vol_dict.keys()):
            template['component-costs'].append({
                'volume': h,
                'material': MATERIAL_DEFAULT,
                'machining': {
                    "machine-type": "laser",
                    "machine-spec": "0.1mm tolerance",
                    "machine-hours": 5
                }
            })

        with open(fname, "w") as f:
            json.dump(template, f, indent=4)

        quote_from_json(fname)
        
    elif args.calculate:
        step_reader = STEPControl_Reader()
        step_reader.ReadFile(args.calculate)
        step_reader.TransferRoot()
        myshape = step_reader.Shape()

        prop = GProp_GProps()
        tolerance = 1e-5 # Adjust to your liking

        # volume = brepgprop_VolumeProperties(myshape, prop, tolerance)
        # print(volume)

        topExp = TopExp_Explorer()
        topExp.Init(myshape, TopAbs_SOLID)

        total_volume = 0

        my_ren = threejs_renderer.ThreejsRenderer()

        while topExp.More():
            curr_shape = topExp.Current()
            volume_props = GProp_GProps()
            brepgprop_VolumeProperties(curr_shape, volume_props, tolerance)
            volume = volume_props.Mass()

            # print(XCAFDoc_ShapeTool.FindShape(curr_shape))
            uuid = hash(curr_shape)
            print(f"uuid: {curr_shape}, vol: {volume}")

            total_volume += volume
            
            my_ren.DisplayShape(curr_shape)

            topExp.Next()

        print(f"TOTAL VOLUME: {total_volume:.2f}")

        my_ren.render()


    else:
        print("error - please run with --read or --calculate mode")
