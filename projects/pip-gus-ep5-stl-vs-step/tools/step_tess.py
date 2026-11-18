"""Tessellate a STEP file with OpenCascade (cadquery-ocp) into one PLY with a per-face id, plus face statistics.

The face id lets Blender colour each NURBS patch separately ("smooth patches" shot) and draw patch boundaries.
Usage: python step_tess.py IN.stp OUT.ply [--defl 0.05]   (linear deflection in model units, mm)
Prints: face count, surface-type histogram, bbox, triangle count.
"""
import sys, collections
import numpy as np
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_SurfaceType


def main():
    src, out = sys.argv[1], sys.argv[2]
    defl = float(sys.argv[sys.argv.index("--defl") + 1]) if "--defl" in sys.argv else 0.05
    r = STEPControl_Reader()
    assert r.ReadFile(src) == IFSelect_RetDone, "STEP read failed"
    r.TransferRoots()
    shape = r.OneShape()
    BRepMesh_IncrementalMesh(shape, defl, False, 0.3, True)
    V, F, FID, kinds = [], [], [], collections.Counter()
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    fid = 0
    while exp.More():
        face = TopoDS.Face(exp.Current())
        kinds[GeomAbs_SurfaceType(BRepAdaptor_Surface(face).GetType()).name] += 1
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, loc)
        if tri is not None:
            trsf = loc.Transformation()
            base = sum(len(v) for v in V)
            pts = []
            for i in range(1, tri.NbNodes() + 1):
                p = tri.Node(i).Transformed(trsf)
                pts.append((p.X(), p.Y(), p.Z()))
            V.append(pts)
            rev = face.Orientation().name == "TopAbs_REVERSED"
            for i in range(1, tri.NbTriangles() + 1):
                a, b, c = tri.Triangle(i).Get()
                F.append((base + a - 1, base + c - 1, base + b - 1) if rev else (base + a - 1, base + b - 1, base + c - 1))
                FID.append(fid)
        fid += 1
        exp.Next()
    V = np.array([p for v in V for p in v], np.float32)
    F = np.array(F, np.int32)
    FID = np.array(FID, np.int32)
    with open(out, "wb") as fh:
        fh.write((f"ply\nformat binary_little_endian 1.0\nelement vertex {len(V)}\nproperty float x\nproperty float y\n"
                  f"property float z\nelement face {len(F)}\nproperty list uchar int vertex_indices\nproperty int face_id\n"
                  "end_header\n").encode())
        fh.write(V.tobytes())
        rec = np.zeros(len(F), dtype=[("n", "u1"), ("i", "<i4", 3), ("f", "<i4")])
        rec["n"] = 3; rec["i"] = F; rec["f"] = FID
        fh.write(rec.tobytes())
    print(f"faces {fid}  types {dict(kinds)}")
    print(f"verts {len(V)}  tris {len(F)}  bbox min {V.min(0).round(1)} max {V.max(0).round(1)}")


if __name__ == "__main__":
    main()
