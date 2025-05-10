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
    OntologySerializer(ROBOT convert):::javaProcess --[output]-->ontology-file.json
    OntologySerializer --[output]-->ontology-file.ttl
    OntologySerializer --[output]-->ontology-file.owl

    ontology-file.json:::file --[downloadable on] --> OntologyCatalog
    ontology-file.ttl:::file --[downloadable on] --> OntologyCatalog
    ontology-file.owl:::file --[downloadable on] --> OntologyCatalog

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

    classDef page fill:#112211,stroke:#333,stroke-width:4px;
    classDef file fill:#001122,stroke:#333,stroke-width:4px;
    classDef object fill:#002211,stroke:#333,stroke-width:4px;
    classDef pyProcess fill:#221100,stroke:#333,stroke-width:1px;
    classDef javaProcess fill:#112200,stroke:#333,stroke-width:1px;