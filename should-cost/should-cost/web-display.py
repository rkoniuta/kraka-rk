#!/usr/bin/env python
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Display.WebGl import x3dom_renderer
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepTools import breptools_Read

# loads step
step_reader = STEPControl_Reader()
step_reader.ReadFile('./test-files/test1.stp')
step_reader.TransferRoot()
myshape = step_reader.Shape()

my_renderer = x3dom_renderer.X3DomRenderer()
my_renderer.DisplayShape(myshape)
my_renderer.render()
from OCC.Display.WebGl import x3dom_renderer