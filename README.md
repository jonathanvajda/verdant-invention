# Ontology View

## Logic



```mermaid
graph TB
    OntologyFile(Ontology File n):::file --[input in]--> TaxonomyBuilder
    TaxonomyBuilder(Common Taxonomy Grafter):::pyProcess --[output]-->harmonized-taxonomy.json

    OntologyFile --[input in]--> OntologyAnnotationParser
    OntologyAnnotationParser(Ontology Metadata Scraper):::pyProcess --[output]--> ontology-metadata.json

    OntologyFile --[input in]--> RobotMeasure
    RobotMeasure(ROBOT measure):::javaProcess --[output]-->ontology-metrics.json

    OntologyFile --[input in]--> OntologyElementParser
    OntologyElementParser(Ontology Element Parser):::pyProcess --[output]--> ontology-elements-combined.json

    OntologyFile --[input in]--> OntologySerializer
    OntologySerializer(ROBOT convert):::javaProcess --[output]-->ontology-file-n.json
    OntologySerializer --[output]-->ontology-file-n.ttl
    OntologySerializer --[output]-->ontology-file-n.owl

    ontology-file-n.json:::file --[downloadable on] --> OntologyCatalog
    ontology-file-n.ttl:::file --[downloadable on] --> OntologyCatalog
    ontology-file-n.owl:::file --[downloadable on] --> OntologyCatalog

    harmonized-taxonomy.json:::file --[populates card] --> OntologyTaxonomy 
    ontology-metrics.json:::file --[populates card] --> OntologyMetaData
    ontology-elements-combined.json:::file --[populates div block on]--> ElementPage
    ontology-metadata.json:::file --[populates card] --> OntologyMetaData


    OntologyTaxonomy:::object --[populates div block on]--> OntologyPage
    OntologyTaxonomy:::object --[populates div block on]--> ElementPage
    OntologyMetaData(Ontology Information Card):::object --[populates div block on]--> OntologyPage

    OntologyPage(Ontology Page):::page --[hyperlinks to]--> ElementPage
    ElementPage(Element Page):::page
    OntologyCatalog(Catalog Main Page):::page --[hyperlinks to]--> OntologyPage

    classDef page fill:#11C,stroke:#111,stroke-width:1px;
    classDef object fill:#33F,stroke:#111,stroke-width:1px;
    classDef file fill:#333,stroke:#111,stroke-width:1px;
    classDef pyProcess fill:#331100,stroke:#111,stroke-width:1px;
    classDef javaProcess fill:#113300,stroke:#111,stroke-width:1px;