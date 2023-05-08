import unittest
import json
from src.create_graph_lib.IngredientsConverter import IngredientsConverter
from typing import List
import owlready2 as owl
import rdflib.term
class InitialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = IngredientsConverter()
        return super().setUpClass()
    def test_entities_in_loaded_ontologies(self):
        """
        This test checks whether key entites from Foodon ontology have been loaded into the world.
        """
        ingredient_set_obo_id = "FOODON_00004082"
        ingredient_specification_obo_id = "FOODON_00004085"
        data_item_obo_id = "IAO_0000027"
        is_about_obo_id = "IAO_0000136"
        food_recipe_obo_id = "FOODON_00004081"
        self.assertIn("ingredient set", self.converter.world[f"{self.converter.BASE_OBO_IRI}{ingredient_set_obo_id}"].label)
        self.assertIn("ingredient specification", self.converter.world[f"{self.converter.BASE_OBO_IRI}{ingredient_specification_obo_id}"].label)
        self.assertIn("data item", self.converter.world[f"{self.converter.BASE_OBO_IRI}{data_item_obo_id}"].label)
        self.assertIn("is about", self.converter.world[f"{self.converter.BASE_OBO_IRI}{is_about_obo_id}"].label)
        self.assertIn("food recipe", self.converter.world[f"{self.converter.BASE_OBO_IRI}{food_recipe_obo_id}"].label)
    def test_creating_new_recipe(self):
        """
        This test adds a test reciepe twice to the world.
        Runs a SPARQL query, which is supposed to find a recipe, with butter as an ingredient (test recipe has it).
        Checks the IRI of the first result.
        Checks the number of found reciepes.
        Keep in mind, that this test will work only if you didn't add a recipe with butter in other tests (#TODO redisgn the assertions, the test shouldn't rely on having no other recipes with butter in other tests).
        """
        with open("scripts/lexmpr/prod/app/src/create_graph_lib/tests/test_input") as file:
            data = json.load(file)
        title = data["title"]
        lexmapr_links = []
        for item in data['ingredientSet']:
            if isinstance(item['oboId'],list) and isinstance(item['sentence'], list):
                for i in range(len(item['oboId'])):
                    lexmapr_links.append((item['oboId'][i],item['sentence'][i]))
            else:
                lexmapr_links.append((item['oboId'],item['sentence']))
                
        self.converter.create_recipe_from_lexmapr(title,lexmapr_links)
        self.converter.create_recipe_from_lexmapr(title,lexmapr_links)

        graph = self.converter.world.as_rdflib_graph()
        butter = self.converter.world.search(label="butter")[0]
        is_about = self.converter.world.search(label="is about")[0]
        has_component = self.converter.world.search(label="has component")[0]

        query = f" SELECT ?food_reciepe {{ \
                ?food_reciepe <{has_component.iri}> ?ingredient_set .\
                ?ingredient_set <{has_component.iri}> ?ingredient_specification .\
                ?ingredient_specification <{is_about.iri}> <{butter.iri}> . \
            }}"
        result = list(graph.query(query))
        food_reciepe = result[0][0]
        self.assertIn("http://purl.obolibrary.org/obo/TAISTI_",str(food_reciepe))
        self.assertEqual(2,len(result))

        
        # if you want to review the created file, save it here and open it in Protege or text editor
        # path = path_to_file
        # self.converter.world.save('test.owl')

if __name__ == "__main__":
    unittest.main()
        