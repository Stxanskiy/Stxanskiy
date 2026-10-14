#!/usr/bin/env python3
"""Trim the 3D contribution SVGs: keep the city, the radar, the total and the date range;
drop the language pie and the star/fork counters.

    python3 tools/trim_contrib.py profile-3d-contrib/contrib-*.svg

Groups are found by their content, not their position, so a generator update that
reorders them does not break this; anything unrecognised is left alone.
"""
import sys
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def texts(el):
    return [(t.text or "").strip() for t in el.iter(f"{{{SVG}}}text") if (t.text or "").strip()]


def trim(path):
    tree = ET.parse(path)
    root = tree.getroot()
    groups = [el for el in root if el.tag == f"{{{SVG}}}g"]
    if not groups:
        return "no groups, untouched"
    city = max(groups, key=lambda g: sum(1 for _ in g.iter()))
    removed = []
    for g in groups:
        words = texts(g)
        if g is city or "Commit" in words:
            continue
        if "contributions" in words:
            for child in list(g):
                cls = child.get("class", "")
                keep = child.tag == f"{{{SVG}}}text" and (cls in ("fill-strong", "fill-weak") or "contributions" in texts(child))
                if not keep:
                    g.remove(child)
                    removed.append("counter")
            continue
        if words:  # the language pie: the only other labelled group
            root.remove(g)
            removed.append("pie")
    tree.write(path, encoding="unicode", xml_declaration=False)
    return ", ".join(sorted(set(removed))) or "nothing to remove"


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(p, "->", trim(p))
