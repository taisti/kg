from typing import List, Tuple, Final
import owlready2 as owl
import itertools
from collections import defaultdict
class IngredientsConverter:
    """
    Converter incorportates food reciepes into Foodon ontology. IRIs for the newly created entity start with the TAISTI prefix. 
    It follows a food recipe model proposed by Foodon.
    Current version creates a food recipe, an ingredient set and for each ingredient in the list, an ingredient specification. 
    The specification is currently limitted to the is_about relation. 
    """
    #used to create full IRIs based on OBO IDs
    BASE_OBO_IRI: Final[str] = "http://purl.obolibrary.org/obo/"

    #classes required to build a model
    imported_classes = {
        "food recipe" : f"{BASE_OBO_IRI}FOODON_00004081",
        "ingredient set" : f"{BASE_OBO_IRI}FOODON_00004082",
        "ingredient specification" : f"{BASE_OBO_IRI}FOODON_00004085",
        "food material" : f"{BASE_OBO_IRI}FOODON_00002403"
    }

    #id counter - used to create IRIs of new entities
    prefix = "TAISTI"
    def get_next_id(self) -> str:
        """
            output: the next ID of an entity in a current graph [str]

            The id conforms the standard with a suffix and 8 digits, padded to the left with 0s
            Example:
            TAISTI_00001234

            :returntype str
        """
        for id_counter in itertools.count():
            taisti_id = str(id_counter).rjust(8,'0')
            full_id = f"{self.prefix}_{taisti_id}"
            yield full_id
    def __init__(self):
        """
            initialier creates a world and loads the foodon ontology
        """
        self.world = owl.World()
        self.foodon = self.world.get_ontology("https://raw.githubusercontent.com/FoodOntology/foodon/master/foodon.owl").load()

    
    def create_recipe_from_lexmapr(self,title : str, entities_lexmapr : List[Tuple[str, int]]):
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
        def default_value():
            return []
        entities_per_line = defaultdict(default_value)
        
        for entity, line_number in entities_lexmapr:
                entities_per_line[line_number].append(entity)
        #for each line in the ingredient set
        for entity_set in entities_per_line:
            #create a new ingredient specification
            ingredient_specification = self.create_ingredient_specification()
            #for each entity in the list
            found_first_ingredient = False
            for oboid in entities_per_line[entity_set]:
                #find the entity in the ontology
                entity = self.world[f"{self.BASE_OBO_IRI}{oboid}"] 
                #if it is the first food material in this line
                if not found_first_ingredient and self.is_food_material(entity):
                    #create a relation is_about between ingredient specification and found entity
                    #same as ingredient_specification.is_about.append(entity)
                    ingredient_specification.IAO_0000136.append(entity)
                    found_first_ingredient = True
            #add the ingredient specification to the ingredient set (use has component relation)
            #same as ingredient_set.has_component.append(ingredient_specification)
            ingredient_set.RO_0002180.append(ingredient_specification)
    def create_ingredient_specification(self):
        ingredient_specification = self.imported_classes['ingredient specification']
        onto_class = self.world[ingredient_specification]
        onto_object = onto_class(self.get_next_id())
        return onto_object
    def find_entity_in_ontology(self, oboid):
        entity_id = f"{self.BASE_OBO_IRI}{oboid}"
        entity = self.world[entity_id]
        return entity
    def is_food_material(self,entity):
        food_class_id = self.imported_classes["food material"]
        food_class = self.world[food_class_id]
        is_food = food_class in entity.ancestors()
        return is_food
    
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
        #same as recipe.has_component.append(ingredient_set)
        recipe.RO_0002180.append(ingredient_set)
        #label the recipe
        recipe.label = label
        return (recipe, ingredient_set)
        
