from pathlib import Path
import lxml.etree as ET
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS, OWL


# NAMESPACE & PREFIX DEFINITIONS
# Base URI for local project entities and local ontology definitions.
# Aligned with TiresiasOntology.ttl and <listPrefixDef> in tiresias.xml.
base_uri = "https://tiresias-lod.github.io/TiresiasLOD/ontology/TiresiasOntology#" #modifica una volta costruita la repository.

# Prefix mapping dictionary: maps prefix string & full namespace URI.
prefix_map = {
    "tir": base_uri,
    "crm": "http://www.cidoc-crm.org/cidoc-crm/",
    "dbo": "http://dbpedia.org/ontology/",
    "dbr": "http://dbpedia.org/resource/",
    "schema": "https://schema.org/",
    "dcterms": "http://purl.org/dc/terms/",
    "edm": "http://www.europeana.eu/schemas/edm/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "rdf": str(RDF),
    "rdfs": str(RDFS),
    "owl": str(OWL),
}


# PREFIX RESOLUTION & LABEL EXTRACTION
def resolve_term(val: str, base_uri: str = base_uri, prefix_map: dict = prefix_map) -> URIRef:
    val = val.strip()

    # Local ID (eg. '#tiresias')
    if val.startswith("#"):
        return URIRef(base_uri + val[1:])

    # authoritative sources (e.g. 'dbo:MythologicalFigure', 'schema:Place')
    if ":" in val and not val.startswith(("http://", "https://")):
        prefix, local_name = val.split(":", 1)
        if prefix in prefix_map:
            return URIRef(prefix_map[prefix] + local_name)

    # Absolute URI
    return URIRef(val)


def extract_entity_labels(element, ns: dict) -> list[tuple[str, str]]:
    """
    Extracts one or more (label_text, lang) pairs from an entity XML element,
    supporting persons (persName with forename/surname), places (placeName),
    works (title), objects/artworks (objectName), events (label), and concepts (term).
    """
    labels = []
    tag = ET.QName(element).localname

    if tag == "person":
        # May contain primary persName and alternative persName (e.g., Greek Τειρεσίας)
        pers_nodes = element.xpath("./tei:persName", namespaces=ns)
        for pnode in pers_nodes:
            # Flatten text across child elements like <forename> and <surname>
            txt = " ".join("".join(pnode.itertext()).split())
            lang = pnode.get("{http://www.w3.org/XML/1998/namespace}lang", "en")
            if txt:
                labels.append((txt, lang))

    elif tag == "place":
        txt = element.findtext("tei:placeName", namespaces=ns)
        if txt:
            labels.append((txt.strip(), "en"))

    elif tag == "bibl":
        txt = element.findtext("tei:title", namespaces=ns)
        if txt:
            labels.append((txt.strip(), "en"))

    elif tag == "object":
        txt = element.findtext(".//tei:objectName", namespaces=ns)
        if txt:
            labels.append((txt.strip(), "en"))

    elif tag == "event":
        txt = element.findtext("tei:label", namespaces=ns)
        if txt:
            labels.append((txt.strip(), "en"))

    elif tag == "item":
        txt = element.findtext("tei:term", namespaces=ns)
        if txt:
            labels.append((txt.strip(), "en"))
    return labels




# 3. BUILD RDF GRAPH FROM TEI/XML
def create_rdf_graph(xml_path: Path | str, base_uri: str = base_uri) -> Graph:
    """
    Reads the TEI/XML file, extracts all relations from <listRelation>,
    extracts labels and owl:sameAs for declared entities, binds namespaces
    to preserve prefixes in output, and returns an rdflib.Graph.
    """
    xml_path = Path(xml_path)
    if not xml_path.exists():
        raise FileNotFoundError(f"XML file not found: {xml_path}")

    # Parse TEI XML document
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    tei_ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    # Initialize RDF Graph
    g = Graph()

    # By calling g.bind(prefix, namespace) we register our prefixes with RDFLib.
    for prefix, uri in prefix_map.items():
        g.bind(prefix, Namespace(uri))

    # default prefix ':' to the base project namespace for concise local URIs
    g.bind("", Namespace(base_uri))


    # xml:id
    entity_nodes = root.xpath(
        "//tei:sourceDesc//*[@xml:id] | //tei:profileDesc//*[@xml:id]",
        namespaces=tei_ns
    )
    processed_entities = set()

    for el in entity_nodes:
        xml_id = el.get("{http://www.w3.org/XML/1998/namespace}id")
        if not xml_id or xml_id in processed_entities:
            continue
        processed_entities.add(xml_id)

        entity_uri = URIRef(base_uri + xml_id)

        #owl:sameAs 
        same_as_link = el.get("sameAs")
        if same_as_link:
            g.add((entity_uri, OWL.sameAs, URIRef(same_as_link.strip())))

        # rdfs:label 
        labels = extract_entity_labels(el, tei_ns)
        for label_text, lang in labels:
            g.add((entity_uri, RDFS.label, Literal(label_text, lang=lang)))

    # 2. RELATIONS
    relations = root.xpath("//tei:listRelation/tei:relation", namespaces=tei_ns)
    for rel in relations:
        active = rel.get("active")
        pred_name = rel.get("name")
        passive = rel.get("passive")

        if active and pred_name and passive:
            subject = resolve_term(active, base_uri=base_uri)
            predicate = resolve_term(pred_name, base_uri=base_uri)
            obj = resolve_term(passive, base_uri=base_uri)

            g.add((subject, predicate, obj))

    return g


# MAIN
if __name__ == "__main__":
    # Resolve project root relative to this script
    script_dir = Path(__file__).resolve().parent

    xml_file = "../xml/tiresias.xml"
    output_ttl ="../ttl/tiresias_graph.ttl"

    graph = create_rdf_graph(xml_file)
   
    graph.serialize(destination=str(output_ttl), format="turtle")
    print(f"RDF graph serialized to Turtle at: {output_ttl}")