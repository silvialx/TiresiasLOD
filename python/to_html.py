from pathlib import Path
import lxml.etree as ET

tei = Path("../xml/tiresias.xml")
xslt = Path("../xml/transformation.xsl")
html = "../html/xml_to_html.html"


# Read the TEI/XML file
doc = ET.parse(tei)

# Read the XSLT file
xslt = ET.parse(xslt)

# create an instance of the class XSLT
transform = ET.XSLT(xslt)

# Perform the transformation
newdoc = transform(doc)

# Write the result in an HTML file
with open(html, 'wb') as f:
    f.write(ET.tostring(newdoc, pretty_print=True))