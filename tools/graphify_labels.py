"""Name Graphify's communities without a model: "<area>: <main files>" from each community's members.

    graphify update . && python tools/graphify_labels.py && graphify cluster-only . --no-label

Writes graphify-out/.graphify_labels.json (community id -> name). Graphify keeps these on later runs.
"""
import collections, json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "graphify-out"


def area(sf):
    p = sf.split("/")
    if p[0] == "projects" and len(p) > 1:
        return p[1]
    if p[0] == "training" and len(p) > 2:
        return "example " + p[2]
    return "skills" if p[0] == ".claude" else p[0]


g = json.load(open(OUT / "graph.json"))
com = collections.defaultdict(list)
for n in g["nodes"]:
    com[n["community"]].append(str(n.get("source_file", "")))
labels = {}
for c, files in sorted(com.items()):
    a = collections.Counter(area(f) for f in files).most_common(1)[0][0]
    top = [x for x, _ in collections.Counter(f.split("/")[-1] for f in files).most_common(2) if x]
    labels[str(c)] = f"{a}: {' + '.join(top)}"[:70]
json.dump(labels, open(OUT / ".graphify_labels.json", "w"), indent=1)
print(len(labels), "communities named")
