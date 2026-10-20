"""
Tiresias LOD — HTML Dossier Generator
Generates Tufte-style HTML dossier pages with Stanford Encyclopedia of Philosophy palette
for all items in ttl/tiresias_graph.ttl.
"""

import os
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL, URIRef, Literal, Namespace

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
TTL_PATH = BASE_DIR / "ttl" / "tiresias_graph.ttl"
OUTPUT_DIR = BASE_DIR / "html" / "items"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Project Base URI
BASE_URI = "https://tiresias-lod.github.io/TiresiasLOD/ontology/TiresiasOntology#"

PREDICATE_CONFIG = {
    "rdf:type": {"human": "Entity Type", "order": 1},
    "rdfs:label": {"human": "Preferred Label", "order": 2},
    "owl:sameAs": {"human": "Authority Match (sameAs)", "order": 99},
    "dcterms:creator": {"human": "Creator / Author", "order": 10},
    "crm:P62_depicts": {"human": "Depicts (CIDOC CRM)", "order": 12},
    "crm:P129_is_about": {"human": "Is About (CIDOC CRM)", "order": 14},
    "crm:P11_had_participant": {"human": "Participant (CIDOC CRM)", "order": 15},
    "crm:P14_carried_out_by": {"human": "Carried Out By (CIDOC CRM)", "order": 16},
    "crm:P7_took_place_at": {"human": "Took Place At (CIDOC CRM)", "order": 17},
    "crm:P120_occurs_before": {"human": "Occurs Before (CIDOC CRM)", "order": 18},
    "schema:character": {"human": "Featured Character (Schema.org)", "order": 20},
    "schema:contentLocation": {"human": "Setting / Location (Schema.org)", "order": 22},
    "schema:containedInPlace": {"human": "Contained In Place (Schema.org)", "order": 24},
    "schema:spouse": {"human": "Spouse (Schema.org)", "order": 26},
    "schema:workLocation": {"human": "Work Location (Schema.org)", "order": 28},
    "tir:hasGift": {"human": "Bestowed Gift (Tiresias Ontology)", "order": 30},
    "tir:isPreconditionedBy": {"human": "Preconditioned By (Tiresias Ontology)", "order": 32},
    "tir:resultsIn": {"human": "Results In (Tiresias Ontology)", "order": 34},
    "tir:prophesiedAbout": {"human": "Prophesied About (Tiresias Ontology)", "order": 36},
    "tir:illustrates": {"human": "Illustrates (Tiresias Ontology)", "order": 38},
}

ITEM_METADATA = {
    "tiresias": {
        "title": "Tiresias",
        "alt_title": "Τειρεσίας · Blind Prophet of Apollo",
        "badge": "Central Entity // Item 001",
        "category": "dbo:MythologicalFigure",
        "image": "tiresias.jpg",
        "caption": "Tiresias, the renowned blind seer of Apollo in Thebes.",
        "credit": "Wikimedia Commons / Public Domain",
        "desc": "The central mythological figure of the project. A blind seer of Apollo in Thebes, famous for clairvoyance and for having lived seven years as a woman. Tiresias participated fully across seven generations in Thebes as advisor to Cadmus and King Oedipus, and connects the project's literary works, deities, and places."
    },
    "hera": {
        "title": "Hera",
        "alt_title": "Queen of the Olympian Gods",
        "badge": "Olympian Deity // Item 002",
        "category": "dbo:Deity",
        "image": "hera.jpg",
        "caption": "Roman marble bust of Hera (Barberini Hera), Vatican Museums.",
        "credit": "Wikimedia Commons / CC BY-SA 3.0",
        "desc": "Queen of the Olympian deities and consort of Zeus. In the mythical dispute over whether men or women feel greater pleasure in love, Tiresias' judgment infuriated Hera, who struck him with blindness. In Kraus's 1690 engraving, she is represented as the deity who transforms him into a woman."
    },
    "zeus": {
        "title": "Zeus",
        "alt_title": "King of the Olympian Gods",
        "badge": "Olympian Deity // Item 003",
        "category": "dbo:Deity",
        "image": "zeus.jpg",
        "caption": "Classical bust of Zeus of Otricoli, Vatican Museums.",
        "credit": "Wikimedia Commons / Public Domain",
        "desc": "King of the Olympian gods. Following the celestial dispute over love's pleasure, Zeus compensates Tiresias for the blindness inflicted by Hera by bestowing upon him the divine gift of prophecy and a lifespan of seven generations."
    },
    "narcissus": {
        "title": "Narcissus",
        "alt_title": "Mythological Youth of Thespiae",
        "badge": "Mythological Figure // Item 004",
        "category": "dbo:MythologicalFigure",
        "image": "narcisus.jpg",
        "caption": "Narcissus, oil on canvas by Caravaggio (c. 1597–1599), Galleria Nazionale d'Arte Antica, Rome.",
        "credit": "Wikimedia Commons / Public Domain",
        "desc": "The legendary youth of exceptional beauty. In Book III of Ovid's Metamorphoses, his mother Liriope consulted Tiresias regarding the boy's future; the seer issued his renowned gnomic prophecy: that Narcissus would live a long life only if he never came to know himself."
    },
    "mount_cyllene": {
        "title": "Mount Cyllene",
        "alt_title": "Mount Kyllini · Peloponnese, Greece",
        "badge": "Geographic Place // Item 005",
        "category": "dbo:Mountain",
        "image": "mount-kyllini.jpg",
        "caption": "View of Mount Cyllene (Kyllini) in Corinthia, Peloponnese, Greece.",
        "credit": "Wikimedia Commons / CC BY-SA 4.0",
        "desc": "A mountain located in the north-eastern Peloponnese, Greece. According to classical mythology recorded in Ovid's Metamorphoses, Mount Cyllene is the location where Tiresias struck two copulating serpents with a staff and was transformed into a woman."
    },
    "thebes": {
        "title": "Thebes",
        "alt_title": "Ancient City in Boeotia, Greece",
        "badge": "Geographic Place // Item 006",
        "category": "schema:Place",
        "image": "thebes.webp",
        "caption": "Archaeological landscape of ancient Thebes (Boeotia, Greece).",
        "credit": "Wikimedia Commons / CC BY-SA 3.0",
        "desc": "The historic Greek city in Boeotia. Thebes is the primary civic setting of Tiresias' prophetic activity, counsel to Cadmus and Creon, and the dramatic setting for Sophocles' tragedy Oedipus Rex."
    },
    "metamorphoses": {
        "title": "Metamorphoses",
        "alt_title": "Narrative Epic by Ovid (c. 8 AD)",
        "badge": "Literary Source // Item 007",
        "category": "dbo:WrittenWork",
        "image": "metamorphoses.jpg",
        "caption": "Illustrated title page from an early edition of Ovid's Metamorphoses.",
        "credit": "Wikimedia Commons / Public Domain",
        "desc": "Latin narrative poem in fifteen books composed by Ovid, completed c. 8 AD. Book III provides the foundational literary narrative connecting Tiresias' metamorphosis on Mount Cyllene, the divine dispute between Zeus and Hera, and the tragic fate of Narcissus."
    },
    "oedipus_rex": {
        "title": "Oedipus Rex",
        "alt_title": "Greek Tragedy by Sophocles (c. 429 BC)",
        "badge": "Dramatic Work // Item 008",
        "category": "dbo:Play",
        "image": "oedipus_rex.jpg",
        "caption": "Scene depicting Oedipus and Tiresias in Sophocles' Oedipus Rex.",
        "credit": "Wikimedia Commons / Public Domain",
        "desc": "The Athenian tragedy by Sophocles, staged in the 5th century BC. Set in plague-stricken Thebes, King Oedipus summons Tiresias seeking the cause of the contamination; Tiresias reluctantly reveals that Oedipus himself is the murderer of Laius."
    },
    "the_waste_land": {
        "title": "The Waste Land",
        "alt_title": "Modernist Landmark Poem by T. S. Eliot (1922)",
        "badge": "Literary Source // Item 009",
        "category": "dbo:WrittenWork",
        "image": "waste_land.jpg",
        "caption": "First edition cover of T. S. Eliot's The Waste Land, Boni & Liveright (1922).",
        "credit": "Wikimedia Commons / Public Domain",
        "desc": "Landmark modernist poem by T. S. Eliot published in 1922. In Part III ('The Fire Sermon'), Tiresias serves as the central unifying consciousness of the poem, uniting all personages, past and present, having 'foresuffered all'."
    },
    "kraus_engraving": {
        "title": "Kraus Engraving",
        "alt_title": "Tiresias strikes two snakes and is transformed by Hera",
        "badge": "Visual Artwork // Item 010",
        "category": "schema:VisualArtwork",
        "image": "kraus_engraving.jpg",
        "caption": "Johann Ulrich Kraus, copperplate engraving c. 1690, from Die Verwandlungen des Ovidii.",
        "credit": "Augsburg, c. 1690 / Public Domain",
        "desc": "17th-century copperplate engraving by Johann Ulrich Kraus (Augsburg, c. 1690) illustrating Ovid's Metamorphoses. Uniquely depicts Hera descending from the heavens to enact the transformation of Tiresias after striking the serpents."
    },
    "della_vecchia_painting": {
        "title": "Della Vecchia Painting",
        "alt_title": "Tiresias Transformed into a Woman (17th c.)",
        "badge": "Visual Artwork // Item 011",
        "category": "schema:VisualArtwork",
        "image": "della_vecchia_painting.jpg",
        "caption": "Pietro della Vecchia, Tiresias Transformed into a Woman, 17th century oil on canvas.",
        "credit": "Museo Correr, Venice / Public Domain",
        "desc": "Venetian Baroque oil painting by Pietro della Vecchia (17th century), dramatically capturing the moment Tiresias strikes the serpents with his staff and experiences his physical metamorphosis."
    },
    "prophecy": {
        "title": "Prophecy",
        "alt_title": "Supernatural Faculty · Foresight",
        "badge": "Conceptual Entity // Item 012",
        "category": "skos:Concept",
        "image": None,  # Missing image, intentionally blank as instructed
        "caption": "Visual representation currently not available.",
        "credit": "Conceptual entity (SKOS)",
        "desc": "The supernatural gift of divine foresight granted to Tiresias by Zeus in recompense for the blindness inflicted upon him by Hera. In the project's semantic model, prophecy connects Tiresias with Oedipus Rex and Narcissus."
    },
    "sex_change": {
        "title": "Sex Change of Tiresias",
        "alt_title": "Transformation of Tiresias into a woman",
        "badge": "Mythological Event // Item 013",
        "category": "crm:E7_Activity",
        "image": None,
        "caption": "Visual representation not depicted.",
        "credit": "CIDOC CRM Activity",
        "desc": "The mythological transformation of Tiresias from man to woman on Mount Cyllene after striking two copulating snakes. Lasting seven years, this experience served as the essential precondition for judging the dispute between Zeus and Hera."
    },
    "zeus_hera_dispute": {
        "title": "Dispute Between Zeus and Hera",
        "alt_title": "Celestial debate judged by Tiresias",
        "badge": "Mythological Event // Item 014",
        "category": "crm:E5_Event",
        "image": None,
        "caption": "Visual representation not depicted.",
        "credit": "CIDOC CRM Event",
        "desc": "The divine dispute between Zeus and Hera over whether men or women feel greater pleasure in love. Having lived as both sexes, Tiresias judged that women feel nine parts out of ten; this provoked Hera's wrath and Zeus's gift of prophecy."
    },
    # Supporting Creators
    "ovid": {
        "title": "Ovid",
        "alt_title": "Publius Ovidius Naso (43 BC – 17/18 AD)",
        "badge": "Supporting Author",
        "category": "schema:Person",
        "image": None,
        "caption": "Classical Roman poet.",
        "credit": "Authority reference",
        "desc": "Roman poet who wrote during the reign of Augustus. Author of the Metamorphoses, which preserves the foundational literary account of Tiresias."
    },
    "sophocles": {
        "title": "Sophocles",
        "alt_title": "Athenian Tragedian (c. 497/6 – 406/5 BC)",
        "badge": "Supporting Author",
        "category": "schema:Person",
        "image": None,
        "caption": "Classical Athenian dramatist.",
        "credit": "Authority reference",
        "desc": "One of Classical Athens' three great tragedians, author of Oedipus Rex and Antigone, in both of which Tiresias plays a pivotal dramatic role."
    },
    "ts_eliot": {
        "title": "T. S. Eliot",
        "alt_title": "Thomas Stearns Eliot (1888–1965)",
        "badge": "Supporting Author",
        "category": "schema:Person",
        "image": None,
        "caption": "Modernist poet, Nobel Laureate.",
        "credit": "Authority reference",
        "desc": "American-English modernist poet, essayist, and critic. In The Waste Land (1922), Eliot positioned Tiresias as the unifying consciousness uniting the entire poem."
    },
    "johann_ulrich_kraus": {
        "title": "Johann Ulrich Kraus",
        "alt_title": "Augsburg Engraver and Illustrator (1655–1719)",
        "badge": "Supporting Artist",
        "category": "schema:Person",
        "image": None,
        "caption": "17th-century German engraver.",
        "credit": "Authority reference",
        "desc": "Prominent German illustrator and publisher in Augsburg, who created the copperplate engraving series Die Verwandlungen des Ovidii (c. 1690)."
    },
    "pietro_della_vecchia": {
        "title": "Pietro della Vecchia",
        "alt_title": "Venetian Baroque Painter (1603–1678)",
        "badge": "Supporting Artist",
        "category": "schema:Person",
        "image": None,
        "caption": "Venetian painter.",
        "credit": "Authority reference",
        "desc": "Venetian painter of the Baroque period, known for dramatic mythological subjects and allegories of transformation."
    }
}

CORE_ITEM_ORDER = [
    "tiresias",
    "hera",
    "zeus",
    "narcissus",
    "mount_cyllene",
    "thebes",
    "metamorphoses",
    "oedipus_rex",
    "the_waste_land",
    "kraus_engraving",
    "della_vecchia_painting",
    "prophecy",
    "sex_change",
    "zeus_hera_dispute"
]


def uri_to_curie(uri_str: str) -> tuple[str, str]:
    prefixes = {
        BASE_URI: "tir:",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf:",
        "http://www.w3.org/2000/01/rdf-schema#": "rdfs:",
        "http://www.w3.org/2002/07/owl#": "owl:",
        "http://purl.org/dc/terms/": "dcterms:",
        "http://www.cidoc-crm.org/cidoc-crm/": "crm:",
        "https://schema.org/": "schema:",
        "http://dbpedia.org/ontology/": "dbo:",
        "http://dbpedia.org/resource/": "dbr:",
        "http://www.w3.org/2004/02/skos/core#": "skos:",
    }
    for ns_uri, prefix in prefixes.items():
        if uri_str.startswith(ns_uri):
            local = uri_str[len(ns_uri):]
            return prefix + local, local
    return uri_str, uri_str


def get_item_label(key: str) -> str:
    if key in ITEM_METADATA:
        return ITEM_METADATA[key]["title"]
    return key.replace("_", " ").title()


def format_object_value(obj, all_local_keys: set) -> str:
    if isinstance(obj, URIRef):
        obj_str = str(obj)
        if obj_str.startswith(BASE_URI):
            local_key = obj_str[len(BASE_URI):]
            label = get_item_label(local_key)
            return f'<a href="{local_key}.html" class="item-link"><strong>{label}</strong> <span class="ext-arrow">→</span></a>'
        
        if "wikidata.org" in obj_str:
            qid = obj_str.rstrip("/").split("/")[-1]
            return f'<a href="{obj_str}" target="_blank" rel="noopener" class="authority-link">Wikidata {qid} <span class="ext-arrow">↗</span></a>'
        if "dbpedia.org/resource/" in obj_str:
            res = obj_str.split("/")[-1]
            return f'<a href="{obj_str}" target="_blank" rel="noopener" class="authority-link">dbr:{res} <span class="ext-arrow">↗</span></a>'
        
        curie, _ = uri_to_curie(obj_str)
        return f'<span class="type-badge">{curie}</span>'
        
    elif isinstance(obj, Literal):
        lang = f' <span style="font-size:0.75rem; color:#888;">@{obj.language}</span>' if obj.language else ''
        return f'<span>"{obj}"{lang}</span>'
    return str(obj)


def generate_item_page(key: str, graph: Graph, prev_key: str, next_key: str, all_local_keys: set):
    meta = ITEM_METADATA.get(key, {
        "title": key.replace("_", " ").title(),
        "alt_title": "",
        "badge": "Entity Dossier",
        "category": "Resource",
        "image": None,
        "caption": "",
        "credit": "",
        "desc": "Information Science and Cultural Heritage Linked Data representation."
    })
    
    subject_uri = URIRef(BASE_URI + key)
    
    # 1. Direct predicates attached to this subject
    po_pairs = list(graph.predicate_objects(subject_uri))
    pred_groups = {}
    for p, o in po_pairs:
        curie, _ = uri_to_curie(str(p))
        if curie == "rdfs:label":
            continue
        if curie not in pred_groups:
            pred_groups[curie] = []
        pred_groups[curie].append(o)
    
    def pred_sort_key(curie):
        if curie in PREDICATE_CONFIG:
            return PREDICATE_CONFIG[curie]["order"]
        return 50
    
    sorted_curies = sorted(pred_groups.keys(), key=pred_sort_key)
    
    rows_html = []
    for curie in sorted_curies:
        objs = pred_groups[curie]
        human_name = PREDICATE_CONFIG.get(curie, {}).get("human", curie)
        
        formatted_objs = [format_object_value(o, all_local_keys) for o in objs]
        if len(formatted_objs) == 1:
            val_html = formatted_objs[0]
        else:
            items_list = "".join(f'<li>{fo}</li>' for fo in formatted_objs)
            val_html = f'<ul style="margin:0; padding-left:1.2rem; list-style-type:square;">{items_list}</ul>'
            
        row = f"""
            <tr>
              <td class="metadata-label">
                <span class="pred-name">{curie}</span>
                <span class="pred-human">{human_name}</span>
              </td>
              <td class="metadata-value">
                {val_html}
              </td>
            </tr>
        """
        rows_html.append(row)
    
    metadata_table_html = "\n".join(rows_html)

    # 2. Inbound / Inverse Relations
    inbound_pairs = list(graph.subject_predicates(subject_uri))
    inbound_rows = []
    if inbound_pairs:
        inbound_groups = {}
        for s, p in inbound_pairs:
            curie, _ = uri_to_curie(str(p))
            if curie not in inbound_groups:
                inbound_groups[curie] = []
            inbound_groups[curie].append(s)
            
        for curie in sorted(inbound_groups.keys(), key=pred_sort_key):
            sources = inbound_groups[curie]
            human_name = PREDICATE_CONFIG.get(curie, {}).get("human", curie)
            formatted_sources = [format_object_value(s, all_local_keys) for s in sources]
            if len(formatted_sources) == 1:
                src_html = formatted_sources[0]
            else:
                slist = "".join(f'<li>{fs}</li>' for fs in formatted_sources)
                src_html = f'<ul style="margin:0; padding-left:1.2rem; list-style-type:square;">{slist}</ul>'
                
            inbound_rows.append(f"""
            <tr>
              <td class="metadata-label">
                <span class="pred-name">← {curie}</span>
                <span class="pred-human">Referenced by ({human_name})</span>
              </td>
              <td class="metadata-value">
                {src_html}
              </td>
            </tr>
            """)
            
    inbound_table_html = "\n".join(inbound_rows)
    inbound_section_html = ""
    if inbound_table_html:
        inbound_section_html = f"""
        <div style="margin-top: 1.5rem;">
          <h2 class="dossier-section-heading">Connected By (Incoming Relations)</h2>
          <table class="metadata-table">
            <tbody>
              {inbound_table_html}
            </tbody>
          </table>
        </div>
        """
    
    # 3. Raw RDF Turtle Snippet
    sub_graph = Graph()
    sub_graph.bind("", Namespace(BASE_URI))
    sub_graph.bind("crm", Namespace("http://www.cidoc-crm.org/cidoc-crm/"))
    sub_graph.bind("dbo", Namespace("http://dbpedia.org/ontology/"))
    sub_graph.bind("dbr", Namespace("http://dbpedia.org/resource/"))
    sub_graph.bind("dcterms", Namespace("http://purl.org/dc/terms/"))
    sub_graph.bind("schema", Namespace("https://schema.org/"))
    sub_graph.bind("skos", Namespace("http://www.w3.org/2004/02/skos/core#"))
    sub_graph.bind("owl", Namespace("http://www.w3.org/2002/07/owl#"))
    
    for p, o in po_pairs:
        sub_graph.add((subject_uri, p, o))
        
    ttl_snippet = sub_graph.serialize(format="turtle").strip()
    
    # Media HTML: Image or Blank Placeholder
    image_filename = meta.get("image")
    if image_filename:
        media_html = f"""
            <figure class="dossier-figure">
              <img src="../../assets/images/{image_filename}" 
                   onerror="if(!this.dataset.retry){{this.dataset.retry=1;this.src='../assets/images/{image_filename}';}}else if(this.dataset.retry==1){{this.dataset.retry=2;this.src='../../image/{image_filename}';}}else{{this.src='../image/{image_filename}';}}"
                   alt="{meta['title']}" 
                   loading="lazy">
              <figcaption class="figure-caption">
                {meta['caption']}
                <div class="figure-credit">{meta['credit']}</div>
              </figcaption>
            </figure>
        """
    else:
        # User requested: "For prophecy, an image is missing. Leave it blank for now."
        media_html = f"""
            <div class="media-placeholder">
              <div class="media-placeholder-icon">❖</div>
              <div class="media-placeholder-text">Image not depicted</div>
              <div class="media-placeholder-note">[Visual representation unassigned · {meta.get('category', 'Concept')}]</div>
            </div>
            <figcaption class="figure-caption" style="text-align: center; margin-top: 0.75rem;">
              <em>{meta.get('caption', 'Non-visual conceptual or event entity')}</em>
            </figcaption>
        """
    
    # Navigation Links
    prev_link = f'<a href="{prev_key}.html" class="pagination-btn">← Previous: {get_item_label(prev_key)}</a>' if prev_key else '<span></span>'
    next_link = f'<a href="{next_key}.html" class="pagination-btn">Next: {get_item_label(next_key)} →</a>' if next_key else '<span></span>'
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta['title']} · Tiresias Linked Open Data</title>
  <link rel="stylesheet" href="../css/tufte-sep.css">
</head>
<body>

  <!-- Stanford Encyclopedia of Philosophy Style Top Header -->
  <header class="sep-banner">
    <div class="sep-banner-inner">
      <a href="../knowledge-representation.html" class="sep-site-title">
        Tiresias LOD <span>Licence to Prophesy</span>
      </a>
      <nav class="sep-nav-links">
        <a href="../knowledge-representation.html">Project Presentation</a>
        <a href="../xml_to_html.html">TEI Edition</a>
        <a href="index.html" class="active">Items Catalog</a>
        <a href="../../ttl/tiresias_graph.ttl" target="_blank">TTL Graph</a>
        <a href="../../ttl/TiresiasOntology.ttl" target="_blank">Ontology</a>
      </nav>
    </div>
  </header>

  <!-- Breadcrumb Sub-bar -->
  <div class="sep-subnav">
    <div class="sep-subnav-inner">
      <a href="../knowledge-representation.html">Home</a>
      <span class="separator">›</span>
      <a href="index.html">Selected Items</a>
      <span class="separator">›</span>
      <span class="current">{meta['title']}</span>
    </div>
  </div>

  <!-- Main Content Container -->
  <main class="page-container">
    <article class="dossier-card">
      
      <!-- Dossier Heading -->
      <header class="dossier-header">
        <div class="dossier-meta-badge">{meta['badge']}</div>
        <h1 class="dossier-title">{meta['title']}</h1>
        <p class="dossier-subtitle">{meta['alt_title']}</p>
      </header>

      <!-- Two-Column Dossier Grid -->
      <div class="dossier-grid">
        
        <!-- Left: Image / Visual Media -->
        <div class="dossier-media">
          {media_html}
        </div>

        <!-- Right: Text Description & Attached Predicates -->
        <div class="dossier-content">
          <p class="dossier-description">
            {meta['desc']}
          </p>

          <div>
            <h2 class="dossier-section-heading">Attached Predicates &amp; Semantic Relations</h2>
            <table class="metadata-table">
              <tbody>
                {metadata_table_html}
              </tbody>
            </table>
          </div>

          {inbound_section_html}

          <!-- Raw RDF Turtle Representation -->
          <div class="rdf-code-box">
            <div class="rdf-code-header">RDF Graph Fragment (Turtle)</div>
            <pre><code>{ttl_snippet}</code></pre>
          </div>

        </div>
      </div>

      <!-- Pagination Footer -->
      <footer class="item-pagination">
        {prev_link}
        <a href="index.html" class="pagination-btn center">Catalog Index</a>
        {next_link}
      </footer>

    </article>
  </main>

  <!-- Stanford Encyclopedia of Philosophy Style Academic Footer -->
  <footer class="sep-footer">
    <div class="sep-footer-inner">
      <div class="sep-footer-col">
        <strong>Tiresias: A Linked Open Data Exploration</strong><br>
        Information Science and Cultural Heritage (DHDK) · A.Y. 2025/2026<br>
        Alma Mater Studiorum – Università di Bologna
      </div>
      <div class="sep-footer-col" style="text-align: right;">
        Project by <strong>Silvia Lusenti</strong><br>
        Encoded with TEI P5, RDFLib, CIDOC CRM &amp; Schema.org
      </div>
    </div>
  </footer>

</body>
</html>
"""
    output_file = OUTPUT_DIR / f"{key}.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated: {output_file.name}")


def generate_catalog_index(all_items: list, graph: Graph):
    cards_html = []
    
    for key in all_items:
        meta = ITEM_METADATA.get(key, {})
        title = meta.get("title", key.replace("_", " ").title())
        alt_title = meta.get("alt_title", "")
        badge = meta.get("badge", "Item")
        category = meta.get("category", "")
        desc = meta.get("desc", "")
        img = meta.get("image")
        
        sub_uri = URIRef(BASE_URI + key)
        pred_count = len(list(graph.predicate_objects(sub_uri)))
        
        if img:
            thumb_html = f'<img src="../../assets/images/{img}" onerror="this.onerror=null; this.src=\'../assets/images/{img}\';" alt="{title}" loading="lazy">'
        else:
            thumb_html = f'<div style="font-family:var(--font-serif); font-style:italic; color:var(--ink-muted); text-align:center; padding:1rem;">❖<br>[No Image Attached]</div>'
            
        card = f"""
        <article class="catalog-card">
          <div class="catalog-card-thumb">
            {thumb_html}
          </div>
          <div class="catalog-card-body">
            <span class="catalog-card-type">{category}</span>
            <h3 class="catalog-card-name"><a href="{key}.html">{title}</a></h3>
            <p class="catalog-card-desc">{desc[:140]}...</p>
            <div class="catalog-card-footer">
              <span>{pred_count} Triples</span>
              <a href="{key}.html">Open Dossier →</a>
            </div>
          </div>
        </article>
        """
        cards_html.append(card)
        
    grid_html = "\n".join(cards_html)
    
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Selected Items Catalog · Tiresias LOD</title>
  <link rel="stylesheet" href="../css/tufte-sep.css">
</head>
<body>

  <!-- Stanford Encyclopedia of Philosophy Style Top Header -->
  <header class="sep-banner">
    <div class="sep-banner-inner">
      <a href="../knowledge-representation.html" class="sep-site-title">
        Tiresias LOD <span>Licence to Prophesy</span>
      </a>
      <nav class="sep-nav-links">
        <a href="../knowledge-representation.html">Project Presentation</a>
        <a href="../xml_to_html.html">TEI Edition</a>
        <a href="index.html" class="active">Items Catalog</a>
        <a href="../../ttl/tiresias_graph.ttl" target="_blank">TTL Graph</a>
        <a href="../../ttl/TiresiasOntology.ttl" target="_blank">Ontology</a>
      </nav>
    </div>
  </header>

  <!-- Breadcrumbs -->
  <div class="sep-subnav">
    <div class="sep-subnav-inner">
      <a href="../knowledge-representation.html">Home</a>
      <span class="separator">›</span>
      <span class="current">Selected Items Catalog</span>
    </div>
  </div>

  <main class="page-container">
    <header class="catalog-header">
      <div class="dossier-meta-badge">Knowledge Organization // Dossiers</div>
      <h1 class="catalog-title">Selected Items of Tiresias LOD</h1>
      <p class="catalog-desc">
        Each item dossier presents the visual representation, semantic classifications,
        authority reconciliation, and linked predicates extracted from <code>tiresias_graph.ttl</code>.
      </p>
    </header>

    <div class="catalog-grid">
      {grid_html}
    </div>
  </main>

  <footer class="sep-footer">
    <div class="sep-footer-inner">
      <div class="sep-footer-col">
        <strong>Tiresias: A Linked Open Data Exploration</strong><br>
        Information Science and Cultural Heritage (DHDK) · A.Y. 2025/2026<br>
        Alma Mater Studiorum – Università di Bologna
      </div>
      <div class="sep-footer-col" style="text-align: right;">
        Project by <strong>Silvia Lusenti</strong>
      </div>
    </div>
  </footer>

</body>
</html>
"""
    catalog_path = OUTPUT_DIR / "index.html"
    with open(catalog_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"Generated Catalog Index: {catalog_path.name}")


def main():
    print(f"Reading graph from: {TTL_PATH}")
    g = Graph()
    g.parse(str(TTL_PATH), format="turtle")
    
    all_local_keys = set()
    for s in g.subjects():
        s_str = str(s)
        if s_str.startswith(BASE_URI):
            all_local_keys.add(s_str[len(BASE_URI):])
            
    print(f"Found {len(all_local_keys)} local entities in graph.")
    
    # Core items
    for i, key in enumerate(CORE_ITEM_ORDER):
        prev_key = CORE_ITEM_ORDER[i - 1] if i > 0 else None
        next_key = CORE_ITEM_ORDER[i + 1] if i < len(CORE_ITEM_ORDER) - 1 else None
        generate_item_page(key, g, prev_key, next_key, all_local_keys)
        
    # Supporting creators
    supporting = [k for k in all_local_keys if k not in CORE_ITEM_ORDER and k != "tiresias_wikipedia_page"]
    for key in supporting:
        generate_item_page(key, g, None, None, all_local_keys)
        
    generate_catalog_index(CORE_ITEM_ORDER, g)
    print("All item files successfully created!")


if __name__ == "__main__":
    main()
