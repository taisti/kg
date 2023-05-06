from typing import List, Tuple
import owlready2 as owl
import itertools
class IngredientsConverter:
    """
    Converter incorportates food reciepes into Foodon ontology. IRIs for the newly created entity start with the TAISTI prefix. 
    It follows a food recipe model proposed by Foodon.
    Current version creates a food recipe, an ingredient set and for each ingredient in the list, an ingredient specification. 
    The specification is currently limitted to the is_about relation. 
    """
    #used to create full IRIs based on OBO IDs
    base_obo_iri = "http://purl.obolibrary.org/obo/"

    #classes required to build a model
    imported_classes = {
        "food recipe" : f"{base_obo_iri}FOODON_00004081",
        "ingredient set" : f"{base_obo_iri}FOODON_00004082",
        "ingredient specification" : f"{base_obo_iri}FOODON_00004085",
        "food material" : f"{base_obo_iri}FOODON_00002403"
    }

    #id counter - used to create IRIs of new entities
    prefix = "TAISTI"
    id_counter = itertools.count()
    def get_next_id(self) -> str:
        """
            output: the next ID of an entity in a current graph [str]

            The id conforms the standard with a suffix and 8 digits, padded to the left with 0s
            Example:
            TAISTI_00001234

            :returntype str
        """
        return f"{self.prefix}_{str(next(self.id_counter)).rjust(8,'0')}"

    def __init__(self):
        """
            initialier creates a world and loads the foodon ontology
        """
        self.world = owl.World()
        self.foodon = self.world.get_ontology("https://raw.githubusercontent.com/FoodOntology/foodon/master/foodon.owl").load()

        
    def create_recipe_from_lexmapr(self,title : str, entities_lexmapr : List[Tuple[str, int]]) -> None:
        """
            input: 
                @param1: recipe name [str]
                @param2: list of obo ids returned by the lexmapr and line numbers in which the entity was found [list[tuple[str,int]]]
            output:
                None

            This method incorporates a food recipe into current world. 
            
        """
        #create a new recipe
        recipe, ingredient_set = self.create_recipe(title)
        #convert the input format of entities
        # [
        #    (entity1, line_number1 )
        #    (entity2, line_number2 )
        #    (entity3, line_number2 )
        #    (entity4, line_number3 )
        # ]
        #into a dictionary
        # {
        #   line_number1 : [entity1]
        #   line_number2 : [entity2, entity3]
        #   line_number3 : [entity4]
        # }
        entities_per_line = {}
        for entity, line_number in entities_lexmapr:
            if line_number not in entities_per_line:
                entities_per_line[line_number] = [entity]
            else:
                entities_per_line[line_number].append(entity)
        #for each line in the ingredient set
        for entity_set in entities_per_line:
            #create a new ingredient specification
            ingredient_specification = self.world[self.imported_classes['ingredient specification']](f"{self.get_next_id()}")
            #for each entity in the list
            found_first_ingredient = False
            for oboid in entities_per_line[entity_set]:
                #find the entity in the ontology
                entity = self.world[f"{self.base_obo_iri}{oboid}"] 
                #if it is the first food material in this line
                if not found_first_ingredient and self.world[self.imported_classes["food material"]] in entity.ancestors():
                    #create a relation is_about between ingredient specification and found entity
                    ingredient_specification.IAO_0000136.append(entity)
                    found_first_ingredient = True
            #add the ingredient specification to the ingredient set (use has component relation)
            ingredient_set.RO_0002180.append(ingredient_specification)
    def create_recipe(self, label : str) -> Tuple[owl.NamedIndividual, owl.NamedIndividual]:
        """
            input:
                @param1: reciepe name [str]
            output:
                @output1: recipe entity [owlready2.NamedIndividual], ingredient set entity [owlready2.NamedIndividual]
            
            This methods creates a new recipe and an ingredient set. It links created entities with the `has component` relation 
            
            :returntype Tuple[owl.NamedIndividual, owl.NamedIndividual]
        """
        #create a new recipe
        recipe = self.world[self.imported_classes['food recipe']](f"{self.get_next_id()}")
        #create a new ingredient set
        ingredient_set = self.world[self.imported_classes['ingredient set']](f"{self.get_next_id()}")
        #link the entities
        recipe.RO_0002180.append(ingredient_set)
        #label the recipe
        recipe.label = label
        return (recipe, ingredient_set)
        
