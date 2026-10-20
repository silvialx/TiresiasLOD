<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
                exclude-result-prefixes="tei">
  
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <!-- Index of every element with an xml:id, so that @ref="#tiresias" can be
       resolved to its entry in the teiHeader (and to its @sameAs URI). -->
  <xsl:key name="entity" match="tei:*[@xml:id]" use="concat('#', @xml:id)"/>
  
  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        
        <title>
          <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
        </title>
        
        <style>
        * {
          box-sizing: border-box;
          }
          
:root{
--paper: #F6F2E9;
--paper-raised: #FBF9F3;
--ink: #201C16;
--ink-soft: #4A453C;
--note: #6B655A;
--rule: #C7BFA9;
--rule-strong: #A79C82;
--accent: #7A2E2E;
--event-tint: #EDE5D0;
--accent-soft: #9C5B4A;
--link: #9c2507;
--serif: 'Newsreader', 'Iowan Old Style', 'Palatino Linotype', Georgia, serif;
--mono: 'IBM Plex Mono', 'SFMono-Regular', Consolas, monospace;
--nav-h: 3.4rem;
--measure: 640px;
}

*{ box-sizing: border-box; }

html{
scroll-behavior: smooth;
scroll-padding-top: calc(var(--nav-h) + 0.5rem);
}

@media (prefers-reduced-motion: reduce){
html{ scroll-behavior: auto; }
*{ animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}

body{
margin: 0;
background: var(--paper);
color: var(--ink);
font-family: var(--serif);
font-size: 18px;
line-height: 1.55;
-webkit-font-smoothing: antialiased;
}

.page {
max-width: 960px;
margin: 0 auto;
padding: 2.5rem 2rem 4rem;
}

header {
margin-bottom: 2rem;
}


h1, h2 {
    font-size: clamp(2rem, 3vw, 2.1rem);
    font-weight: 600;
    margin: 0 0 1.6rem;
    letter-spacing: -0.005em;
}

h1 {
margin: 0;
padding-bottom: 0.25rem;
border-bottom: 1px solid #a2a9b1;
font-size: 2.25rem;
}

.encoding-title {
margin: 0.65rem 0 0;
color: #54595d;
font-size: 0.95rem;
}

.source {
margin: 0.35rem 0 0;
color: #54595d;
font-size: 0.9rem;
}

h2 {
margin: 2.25rem 0 0.75rem;
padding-bottom: 0.2rem;
border-bottom: 1px solid #a2a9b1;
font-size: 1.55rem;
}

h3 {
margin: 1.75rem 0 0.6rem;
color: #202122;
font-size: 1.1rem;
font-weight: 600;
line-height: 1.4;
}

p {
margin: 0.75rem 0;
}

a {
color: var(--accent);
text-decoration: none;
}

a:hover {
text-decoration: underline;
}

.entity {
color: var(--accent);
}

.work {
font-style: italic;
}

.quotation {
font-style: italic;
}

.gap {
margin: 1.5rem 0;
color: #72777d;
font-size: 0.9rem;
text-align: center;
}

@media (max-width: 700px) {
.page {
padding: 1.5rem 1rem 3rem;
}

h1 {
font-size: 1.9rem;
}

h2 {
font-size: 1.4rem;
}
}

.figdesc {
  display: block;
  margin-top: 0.4rem;
  font-size: 0.95rem;
  line-height: 1.35;
  font-style: italic;
  color: var(--ink-soft);
}

.rs.event {
    font-style: italic;
  background: var(--event-tint);
  padding: 0.05em 0.15em;
  border-radius: 2px;
  -webkit-box-decoration-break: clone;
  box-decoration-break: clone;
}

/* Linked entities: same red as plain entities, underline only on hover */
a.entity, a.work {
  color: var(--accent);
  text-decoration: none;
}
a.entity:hover, a.work:hover,
a.entity:focus-visible, a.work:focus-visible {
  text-decoration: underline;
  text-underline-offset: 0.15em;
}
.work { color: inherit; }
a.work { color: var(--accent); }

/* Dates */
.date { font-weight: 700; }

/* Footnote markers in the running text */
.note-ref {
  font-size: 0.7em;
  line-height: 0;
  vertical-align: super;
  font-style: normal;
  font-weight: 600;
}
.note-ref a { color: var(--accent); }

/* Footnotes at the bottom of the text */
.footnotes {
  margin-top: 3.5rem;
  font-size: 0.9rem;
  line-height: 1.45;
  color: var(--ink-soft);
}
.footnotes hr {
  width: 30%;
  margin: 0 0 1rem;
  border: 0;
  border-top: 1px solid var(--rule-strong);
}
.footnotes h2 {
  margin: 0 0 0.75rem;
  border: 0;
  font-size: 1.05rem;
  color: var(--ink);
}
.footnotes ol { list-style: none; margin: 0; padding: 0; }
.footnotes li { display: flex; gap: 0.5em; margin: 0 0 0.5rem; }
.footnotes .note-num { color: var(--accent); font-weight: 600; min-width: 1.4em; }
.footnotes .backref { margin-left: 0.3em; color: var(--accent); }
.footnotes li:target { background: var(--event-tint); }

figure { margin: 2rem 0; }
figure img { display: block; max-width: 100%; max-height: 55vh; height: auto; }
figcaption { margin-top: 0.5rem; font-size: 0.95rem; line-height: 1.4; color: var(--ink-soft); }

        </style>
      </head>
      
      <body>
        <div class="page">
          <header>
            
            <!-- The title & subtitle -->
            <h1>
              <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:title"/>
            </h1>            
            <p class="encoding-title">
              <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
            </p>
            
            <p class="source">
              <xsl:text>Source: </xsl:text>
              
              <a href="{tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:ptr/@target}">
                <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:title"/>
              </a>
              
              <xsl:text>, accessed </xsl:text>
              <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:date[@type='accessed']"/>
            </p>
          </header>
          
          <main>
            <xsl:apply-templates select="tei:TEI/tei:text/tei:body/node()"/>
          </main>

          <!-- Notes collected at the bottom, as in a book or paper -->
          <xsl:if test="tei:TEI/tei:text//tei:note">
            <section class="footnotes" id="notes">
              <hr/>
              <h2>Notes</h2>
              <ol>
                <xsl:for-each select="tei:TEI/tei:text//tei:note">
                  <xsl:variable name="n">
                    <xsl:call-template name="note-number"/>
                  </xsl:variable>
                  <li id="note-{$n}">
                    <span class="note-num"><xsl:value-of select="$n"/>.</span>
                    <span>
                      <xsl:apply-templates/>
                      <a class="backref" href="#noteref-{$n}" title="Back to text">&#8617;</a>
                    </span>
                  </li>
                </xsl:for-each>
              </ol>
            </section>
          </xsl:if>
        </div>
      </body>
    </html>
  </xsl:template>
  
  <xsl:template match="tei:div">
    <section>
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
          <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </section>
  </xsl:template>
  
  
  <!-- Section and subsection headings are rendered at different HTML heading levels. -->
  <xsl:template match="tei:head">
    <xsl:choose>
      <xsl:when test="parent::tei:div[@type='subsection']">
        <h3><xsl:apply-templates/></h3>
      </xsl:when>
      <xsl:otherwise>
        <h2><xsl:apply-templates/></h2>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>
  
  <!-- Inline textual markup. -->
  <xsl:template match="tei:emph">
    <em><xsl:apply-templates/></em>
  </xsl:template>
  
  <xsl:template match="tei:title">
    <xsl:call-template name="linked">
      <xsl:with-param name="class" select="'work'"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tei:persName | tei:placeName | tei:objectName | tei:term | tei:num">
    <xsl:call-template name="linked">
      <xsl:with-param name="class" select="'entity'"/>
    </xsl:call-template>
  </xsl:template>

  <!-- If @ref points to an entity in the header that has a @sameAs
       (Wikidata / DBpedia), render a link; otherwise a plain span.
       Headings are left unlinked. -->
  <xsl:template name="linked">
    <xsl:param name="class"/>
    <xsl:variable name="uri" select="key('entity', @ref)/@sameAs"/>
    <xsl:choose>
      <xsl:when test="string($uri) and not(ancestor::tei:head)">
        <a class="{$class}" href="{$uri}" target="_blank" rel="noopener">
          <xsl:attribute name="title">
            <xsl:choose>
              <xsl:when test="contains($uri, 'wikidata')">Wikidata: </xsl:when>
              <xsl:when test="contains($uri, 'dbpedia')">DBpedia: </xsl:when>
            </xsl:choose>
            <xsl:value-of select="$uri"/>
          </xsl:attribute>
          <xsl:apply-templates/>
        </a>
      </xsl:when>
      <xsl:otherwise>
        <span class="{$class}"><xsl:apply-templates/></span>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Dates in bold -->
  <xsl:template match="tei:date | tei:origDate">
    <strong class="date"><xsl:apply-templates/></strong>
  </xsl:template>

  <!-- Notes: only a numbered marker stays in the text; the content goes to the
       Notes section at the bottom. -->
  <xsl:template match="tei:note">
    <xsl:variable name="n">
      <xsl:call-template name="note-number"/>
    </xsl:variable>
    <sup class="note-ref">
      <a id="noteref-{$n}" href="#note-{$n}" title="Note {$n}">
        <xsl:value-of select="$n"/>
      </a>
    </sup>
  </xsl:template>

  <!-- Uses @n when present (keeps the original Wikipedia numbering),
       otherwise counts the notes in the text. -->
  <xsl:template name="note-number">
    <xsl:choose>
      <xsl:when test="@n"><xsl:value-of select="@n"/></xsl:when>
      <xsl:otherwise>
        <xsl:number level="any" count="tei:note" from="tei:text"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <xsl:template match="tei:q">
    <span class="quotation"><xsl:apply-templates/></span>
  </xsl:template>
  

<xsl:template match="tei:figure">
  <figure>
    <xsl:apply-templates select="tei:graphic"/>
    <figcaption>
      <xsl:apply-templates select="tei:figDesc"/>
    </figcaption>
  </figure>
</xsl:template>

<xsl:template match="tei:graphic">
  <img src="{@url}"/>
</xsl:template>


  <!-- Sampling omissions are made visible in the HTML output. -->
  <xsl:template match="tei:gap[@reason='sampling']">
    <p class="gap">--- omitted from the selected sample ---</p>
  </xsl:template>
  

  
  <xsl:template match="tei:rs">
  <span class="rs {@type}" title="{@type}: {substring-after(@ref, '#')}">
    <xsl:apply-templates/>
  </span>
</xsl:template>






  
</xsl:stylesheet>
