"""Name Graphify's communities without a model.

    graphify update . && python tools/graphify_labels.py && graphify cluster-only . --no-label

Names written by hand after a full read-through are kept in graphify-out/community_names.json
(name -> member node ids). A community keeps a name when at least half its members carried it (a split
community gets "<name> (2)"); anything new gets "<area>: <main files>" from its members.
`--save` records the names currently in graph.json as the hand-written set (run it after naming).

Writes graphify-out/.graphify_labels.json (community id -> name). Graphify keeps these on later runs.
"""
import collections, json, sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "graphify-out"
NAMES = OUT / "community_names.json"


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
    com[n["community"]].append(n)

if "--save" in sys.argv:
    saved = {}
    for c, nodes in sorted(com.items()):
        name = nodes[0].get("community_name")
        if name and not name.startswith("Community "):
            saved[name] = sorted(n["id"] for n in nodes)
    json.dump(saved, open(NAMES, "w"), indent=0, sort_keys=True)
    print(len(saved), "hand-written names saved")
    sys.exit()

named = json.load(open(NAMES)) if NAMES.exists() else {}
owner = {i: name for name, members in named.items() for i in members}
labels, kept, used = {}, 0, collections.Counter()
for c, nodes in sorted(com.items(), key=lambda kv: -len(kv[1])):
    votes = collections.Counter(owner[n["id"]] for n in nodes if n["id"] in owner)
    best, count = votes.most_common(1)[0] if votes else (None, 0)
    if best and count * 2 >= len(nodes):      # most of this community carried that name
        used[best] += 1
        labels[str(c)] = best if used[best] == 1 else f"{best} ({used[best]})"
        kept += 1
        continue
    files = [str(n.get("source_file", "")) for n in nodes]
    a = collections.Counter(area(f) for f in files).most_common(1)[0][0]
    top = [x for x, _ in collections.Counter(f.split("/")[-1] for f in files).most_common(2) if x]
    labels[str(c)] = f"{a}: {' + '.join(top)}"[:70]
json.dump(labels, open(OUT / ".graphify_labels.json", "w"), indent=1)
print(len(labels), "communities named,", kept, "hand-written names kept")
