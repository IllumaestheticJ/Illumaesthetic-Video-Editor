"""STEP -> STL with OpenCascade's BRepMesh (robust where gmsh hangs on CAD fin surfaces).

    python projects/toyota-gr-corolla/tools/step2stl.py part.stp out.stl [--defl 0.05] [--ang 0.3]

Keeps STEP units (mm). Prints the bbox of each solid so you can see whether the CAD is already in the car's frame
(core_7.6.23.stp, the Jackson Racing intercooler, is: it lands on the stock intercooler without any transform).
"""
import argparse

from OCP.BRep import BRep_Tool
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.Bnd import Bnd_Box
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_Reader
from OCP.StlAPI import StlAPI_Writer
from OCP.TopAbs import TopAbs_SOLID, TopAbs_SHELL
from OCP.TopExp import TopExp_Explorer

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--defl", type=float, default=0.05); ap.add_argument("--ang", type=float, default=0.3)
a = ap.parse_args()
r = STEPControl_Reader()
assert r.ReadFile(a.src) == IFSelect_RetDone
r.TransferRoots()
shape = r.OneShape()
ex = TopExp_Explorer(shape, TopAbs_SOLID)
while ex.More():
    b = Bnd_Box(); BRepBndLib.Add_s(ex.Current(), b)
    lo, hi = b.CornerMin(), b.CornerMax()
    print("solid", [round(v, 1) for v in (lo.X(), lo.Y(), lo.Z(), hi.X(), hi.Y(), hi.Z())])
    ex.Next()
BRepMesh_IncrementalMesh(shape, a.defl, False, a.ang, True)
w = StlAPI_Writer(); w.ASCIIMode = False
print("written", w.Write(shape, a.out))
