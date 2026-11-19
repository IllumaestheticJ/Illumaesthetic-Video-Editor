import sys, numpy as np
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID, TopAbs_FACE
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/projects/bf-miata-mr2-night-meet/tools")
from scan_to_glb import write_stl
r = STEPControl_Reader(); r.ReadFile(sys.argv[1]); r.TransferRoots(); shape = r.OneShape()
allt = []
ex = TopExp_Explorer(shape, TopAbs_SOLID); k = 0
while ex.More():
    sol = ex.Current(); tris = []
    for defl in (0.3, 1.0, 3.0):
        BRepMesh_IncrementalMesh(sol, defl, False, 0.5, True)
        tris = []
        fe = TopExp_Explorer(sol, TopAbs_FACE); nf = nbad = 0
        while fe.More():
            f = TopoDS.Face(fe.Current()); loc = TopLoc_Location(); tri = BRep_Tool.Triangulation_s(f, loc); nf += 1
            if tri is None: nbad += 1
            else:
                tr = loc.Transformation()
                P = np.array([[tri.Node(i).Transformed(tr).X(), tri.Node(i).Transformed(tr).Y(), tri.Node(i).Transformed(tr).Z()] for i in range(1, tri.NbNodes() + 1)])
                rev = f.Orientation() == 1
                for j in range(1, tri.NbTriangles() + 1):
                    a, b, c = tri.Triangle(j).Get(); idx = [a - 1, c - 1, b - 1] if rev else [a - 1, b - 1, c - 1]; tris.append(P[idx])
            fe.Next()
        if nbad == 0: break
    T = np.array(tris); print("solid", k, "faces", nf, "unmeshed", nbad, "tris", len(T), T.reshape(-1, 3).min(0).round(0), T.reshape(-1, 3).max(0).round(0))
    allt.append(T); k += 1; ex.Next()
write_stl(sys.argv[2], np.concatenate(allt))
