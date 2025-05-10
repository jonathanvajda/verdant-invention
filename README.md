# Ontology View

The basic setup of the ontology viewing service is as follows
- Catalog
  - This displays ontologies in a list, with the ontology's description.
  - Displays simple metrics (errors, warnings, etc.)
  - Each file format provided
- Ontology page
  - This displays the particular ontology, with the ontology's fill annotations.
  - Displays the metrics
  - Displays the taxonomy 

## Logic

```mermaid
graph TB
    OntologyFile(Ontology File n):::file --[input in]--> OntologySerializer
    OntologySerializer(ROBOT convert):::javaProcess --[output]-->ontology-file-n.json
    OntologySerializer --[output]-->ontology-file-n.ttl
    OntologySerializer --[output]-->ontology-file-n.owl

    OntologyFile --[input in]--> RobotMeasure
    RobotMeasure(ROBOT measure):::javaProcess --[output]-->ontology-metrics.json

    OntologyFile --[input in]--> queryBattery
    queryBattery(Annotation Checks):::pyProcess --[output]-->ontology-metrics.json

    ontology-file-n.json:::file --[downloadable on] --> OntologyCard
    ontology-file-n.ttl:::file --[downloadable on] --> OntologyCard
    ontology-file-n.owl:::file --[downloadable on] --> OntologyCard

    OntologyFile --[input in]--> OntologyAnnotationParser
    OntologyAnnotationParser(Ontology Metadata Scraper):::pyProcess --[output]--> ontology-metadata.json

    OntologyFile --[input in]--> TaxonomyBuilder
    TaxonomyBuilder(Common Taxonomy Grafter):::pyProcess --[output]-->harmonized-taxonomy.json


    OntologyFile --[input in]--> OntologyElementParser
    OntologyElementParser(Ontology Element Parser):::pyProcess --[output]--> ontology-elements-n.json

    OntologyCard(Ontology Summary Card):::card --[populates div] --> OntologyCatalog

    harmonized-taxonomy.json:::file --[populates card] --> OntologyTaxonomy 
    ontology-metrics.json:::file --[populates card] --> OntologyCard
    ontology-metrics.json:::file --[populates card] --> OntologyMetaData
    ontology-elements-n.json:::file --[populates div block on]--> ElementPage
    ontology-metadata.json:::file --[populates card] --> OntologyCard
    ontology-metadata.json --[populates card] --> OntologyMetaData


    OntologyTaxonomy:::card --[populates div block on]--> OntologyPage
    OntologyTaxonomy:::card --[populates div block on]--> ElementPage
    OntologyMetaData(Ontology Expanded Info Card):::card --[populates div block on]--> OntologyPage

    OntologyPage(Ontology Page):::page --[hyperlinks to]--> ElementPage
    ElementPage(Element Page):::page
    OntologyCard --[hyperlinks to]--> OntologyPage
    OntologyCatalog:::page 

    classDef page fill:#11C,stroke:#111,stroke-width:1px;
    classDef card fill:#33F,stroke:#111,stroke-width:1px;
    classDef file fill:#333,stroke:#111,stroke-width:1px;
    classDef pyProcess fill:#331100,stroke:#111,stroke-width:1px;
    classDef javaProcess fill:#113300,stroke:#111,stroke-width:1px;