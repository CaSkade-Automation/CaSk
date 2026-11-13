"""Regenerates the QUDT unit block in cask.ttl from a QUDT release file.

CaSk ships the units of the QUDT unit vocabulary as individuals, so that a user
does not have to fetch them. QUDT itself is not imported; the QUDT terms used
here are declared in cask.ttl. Only the properties CaSk declares are copied:

    qudt:conversionMultiplier   qudt:conversionOffset   qudt:hasDimensionVector
    qudt:iec61360Code           qudt:uneceCommonCode    rdfs:label (English)

Everything else QUDT states about a unit stays in QUDT. The copied triples are
verbatim; the only addition is the owl:NamedIndividual typing, which QUDT
leaves implicit.

Usage:
    python tools/generate_units.py <qudt-all.ttl> [cask.ttl]

Source: https://qudt.org/3.5.3/qudt-all (QUDT 3.5.3, CC BY 4.0, QUDT.org).
Download it, then run this script and commit the result.
"""
import io
import sys

from rdflib import Graph, URIRef, RDF, RDFS

NL = "\r\n"
UNIT = "http://qudt.org/vocab/unit/"
DIMVEC = "http://qudt.org/vocab/dimensionvector/"
QUDT = "http://qudt.org/schema/qudt/"
# Provenance, as QUDT itself states it on every unit.
SOURCE_IRI = "http://qudt.org/3.5.3/vocab/unit"

# The block is written between the first QUDT individual and this anchor.
# Protege sorts individuals by IRI, so qudt.org stays ahead of openmath.org.
ANCHOR = "###  http://www.openmath.org/cd/FundamentalPhysicalConstants1"

FIELDS = [("qudt:conversionMultiplier", "conversionMultiplier", "number"),
          ("qudt:conversionOffset", "conversionOffset", "number"),
          ("qudt:hasDimensionVector", "hasDimensionVector", "iri"),
          ("qudt:iec61360Code", "iec61360Code", "text"),
          ("qudt:uneceCommonCode", "uneceCommonCode", "text")]


def one(graph, iri, name):
    values = list(graph.objects(iri, URIRef(QUDT + name)))
    return values[0] if values else None


def english_label(graph, iri):
    fallback = None
    for value in graph.objects(iri, RDFS.label):
        if value.language == "en":
            return value
        if value.language in (None, "en-US"):
            fallback = value
    return fallback


def escape(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def entity(iri, type_name, fields):
    head = "<%s>" % iri
    pad = " " * (len(head) + 1)
    lines = ["%s rdf:type owl:NamedIndividual ," % head,
             "%s%s%s ;" % (pad, " " * len("rdf:type "), type_name)]
    for index, (predicate, value, kind) in enumerate(fields):
        if kind == "number":
            written = str(value)
        elif kind == "iri":
            written = "<%s>" % value
        else:
            lang = getattr(value, "language", None)
            written = '"%s"%s' % (escape(value), "@" + lang if lang else "")
        lines.append("%s%s %s%s"
                     % (pad, predicate, written,
                        " ;" if index < len(fields) - 1 else " ."))
    return "###  %s%s%s" % (iri, NL, NL.join(lines))


def main(source_path, cask_path):
    source = Graph()
    source.parse(source_path, format="turtle")

    units, vectors = [], set()
    for iri in sorted(source.subjects(RDF.type, URIRef(QUDT + "Unit")), key=str):
        fields = []
        for predicate, name, kind in FIELDS:
            value = one(source, iri, name)
            if value is None:
                continue
            fields.append((predicate, value, kind))
            if name == "hasDimensionVector":
                vectors.add(str(value))
        label = english_label(source, iri)
        if label is not None:
            fields.append(("rdfs:label", label, "label"))
        fields.append(("rdfs:isDefinedBy", URIRef(SOURCE_IRI), "iri"))
        if fields:
            units.append(entity(iri, "qudt:Unit", fields))

    vector_blocks = []
    for vector in sorted(vectors):
        iri = URIRef(vector)
        label = english_label(source, iri)
        vector_blocks.append(entity(
            iri, "qudt:QuantityKindDimensionVector",
            [("rdfs:label", label if label is not None
              else vector.rsplit("/", 1)[-1], "label"),
             ("rdfs:isDefinedBy", URIRef(SOURCE_IRI), "iri")]))

    block = (NL * 2).join(vector_blocks + units) + NL * 3

    text = io.open(cask_path, encoding="utf-8", newline="").read()
    starts = [text.index("###  " + prefix) for prefix in (DIMVEC, UNIT)
              if "###  " + prefix in text]
    if not starts:
        raise SystemExit("no QUDT individuals found in %s" % cask_path)
    start, end = min(starts), text.index(ANCHOR)
    if start >= end:
        raise SystemExit("QUDT block is not where this script expects it")
    io.open(cask_path, "w", encoding="utf-8", newline="").write(
        text[:start] + block + text[end:])
    print("wrote %d units and %d dimension vectors to %s"
          % (len(units), len(vector_blocks), cask_path))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "cask.ttl")
