import owlready2 as owl


def processUnitClass(unitTypeClass, search_text):
    picked_classes = []
    for unitClass in unitTypeClass.subclasses():
        subUnits = list(unitClass.subclasses())
        if(len(subUnits) == 0): 
            if search_text in unitClass.hasExactSynonym + unitClass.label:
                picked_classes += unitClass.label
        else:
            for subUnit in subUnits:
                if search_text in subUnit.hasExactSynonym + subUnit.label:
                    picked_classes += subUnit.label
                    
    return picked_classes
def get_unit_type(input):
    onto : owl.Ontology = owl.get_ontology('ontologies/io_prototype.rdf').load()
    unit : owl.ClassConstruct = owl.IRIS['http://purl.obolibrary.org/obo/UO_0000000']
    picked = []
    for unitTypeClass in unit.subclasses():
        if 'mass unit' in unitTypeClass.label:
            picked += ('mass', processUnitClass(unitTypeClass,input))
        if 'volume unit' in unitTypeClass.label:
            picked += ('volume',processUnitClass(unitTypeClass,input))
    return picked

print(get_unit_type('cup'))
print(get_unit_type('gallon'))
print(get_unit_type('kg'))
print(get_unit_type('teaspoon'))
print(get_unit_type('tsp'))
print(get_unit_type('tbsp'))

#lemmatization requires
print(get_unit_type('teaspoons'))
