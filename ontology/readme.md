The current version of the ontology is in the io_prototype.rdf file. Current name, and the namespace are created ad-hoc and subject to a change.

The ontology file is comprised of parts of the following, existing ontologies:

 - PATO[1] - the Phenotype And Trait Ontology. An ontology of phenotypic qualities (properties, attributes or characteristics).
 - OBI[2] - The Ontology for Biomedical Investigations is build in a collaborative, international effort and will serve as a resource for annotating biomedical investigations, including the study design, protocols and instrumentation used, the data generated and the types of analysis performed on the data.
 - FoodON[3] - a consortium-driven project to build a comprehensive and easily accessible global farm-to-fork ontology about food, that accurately and consistently describes foods commonly known in cultures from around the world.
 - IAO [4] - an ontology of information entities, originally driven by work by the OBI digital entity and realizable information entity branch.
 - BFO [5] - The Basic Formal Ontology (BFO) is a small, upper level ontology that is designed for use in supporting information retrieval, analysis and integration in scientific and other domains. BFO is a genuine upper ontology. Thus it does not contain physical, chemical, biological or other terms which would properly fall within the coverage domains of the special sciences. BFO is used by more than 250 ontology-driven endeavors throughout the world.
 - UO [6] - Units Ontology - Metrical units for use in conjunction with PATO
 - RO [7] - Relation Ontology
 - COB[8] - Core Ontology for Biology and Biomedicine

 It is not a full merge of all ontologies, as the size of a fully merged file is rather inconvenient. Instead, just the crucial concepts(the concepts which are required to explain proposed concepts) are imported into the file.

 The concepts required to create a graph of reciepe ingredients (classes, data and object properties, and instances) are derived from the "Food Process Ontology Requirements"[9]. In fact the source ontologies already explain the proposed classes already exist, often with an "requires discussion" annotation. The existing classes and data properties have the following IRIs

classes:
 - Ingredient set: http://purl.obolibrary.org/obo/FOODON_00004082
 - Instruction set: http://purl.obolibrary.org/obo/FOODON_00004084
 - Device set: http://purl.obolibrary.org/obo/FOODON_00004084
 - Food reciepe: http://purl.obolibrary.org/obo/FOODON_00004081
 - Ingredient specification: http://purl.obolibrary.org/obo/FOODON_00004085

object properties
 - 'is about' : http://purl.obolibrary.org/obo/IAO_0000136
 - 'has member' : http://purl.obolibrary.org/obo/RO_0002351

data properties:
 - 'has quantity' : http://purl.obolibrary.org/obo/COB_0000511

the following object properties do not exist in the source ontologies (at least I didn't find them yet):
 
 - 'component of'
 - 'is quality measure of' 
 - 'has unit' - although the object property 'has measurement unit label' exists in the IAO under IRI http://purl.obolibrary.org/obo/IAO_0000039 (yes, it is an object, not a data property, it seems odd).

The ontology file, contains our implementation (very similar to the one in a source, with an exception of alternative definitions of those concepts, which might prove to be redundant) of the above concepts. Additionally, the ontology file contains Instances, which cover a sample 'Ingredient Set' for a sample 'Food reciepe'.

Note that the file is under construction.


 [1] https://github.com/pato-ontology/pato
 [2] https://github.com/obi-ontology/obi
 [3] https://github.com/FoodOntology/foodon
 [4] https://github.com/information-artifact-ontology/IAO
 [5] https://github.com/BFO-ontology
 [6] https://github.com/bio-ontology-research-group/unit-ontology
 [7] https://obofoundry.org/ontology/ro.html
 [8] https://obofoundry.org/ontology/cob.html
 [9] https://www.semantic-web-journal.net/content/food-process-ontology-requirements