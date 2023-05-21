import ast
import re
from operator import truth

from more_itertools import pairwise
from thefuzz import fuzz
from thefuzz.process import extractOne

import pandas as pd
from typing import List, Dict, Optional


class Postprocessing:
    def __init__(
        self, request_input: pd.DataFrame, lexmapr_output: List[pd.DataFrame]
    ):
        self.request_input = request_input
        self.lexmapr_output = lexmapr_output

    def run(self):
        body = self.postprocess(self.request_input, self.lexmapr_output)
        body = self.pair_merge_entities(self.request_input, body)
        out = self.add_closest_sentences(body, self.request_input)
        return out

    @staticmethod
    def postprocess(request_input: pd.DataFrame, lexmapr_output: List[pd.DataFrame]):
        """
        Create requests output JSON

        Args:
            request_input (pd.DataFrame): input recipes table
            lexmapr_output (List[pd.DataFrame]): list of analysed recipes by LexMapr

        Returns:
            LexMaprOutput: [{
                "title": str,
                "link": str,
                "ingredientSet": list[{
                    "match": "No Match" | "Full Term Match",
                    "name": list[str],
                    "oboId": list[str]
                }]
            }]
        """

        def for_each_row(row: pd.Series):
            match = row["Match_Status(Macro Level)"]
            if match == "No Match":
                return None

            match_components = ast.literal_eval(row["Matched_Components"])
            name = [txt.split(":")[0].strip(r"[\[']") for txt in match_components]
            obo_id = [txt.split(":")[1].strip(r"[\[']") for txt in match_components]

            if len(name) == 1:
                name = name[0]
                obo_id = obo_id[0]

            ingredients_set = {"name": name, "oboId": obo_id, "match": match}
            return ingredients_set

        body = [
            {
                "title": recipe_info["title"],
                "link": recipe_info["link"],
                "ingredientSet": list(filter(truth, [
                    for_each_row(row)
                    for _, row in recipe_ingredients.iterrows()
                ]))
            }
            for (_, recipe_info), recipe_ingredients in zip(
                request_input.iterrows(), lexmapr_output
            )
        ]

        return body

    @staticmethod
    def pair_merge_entities(request_input: pd.DataFrame, body: List[Dict]) -> List[Dict]:
        """
        Merge LexMapr entities when first NER entity type is **COLOR, PHYSICAL_QUALITY, PROCESS** and second is a
        NER type **FOOD**

        Args:
            request_input (pd.DataFrame): input recipes table
            body (List[Dict]):  LexMaprOutput: [{
                "title": str,
                "link": str,
                "ingredientSet": list[{
                    "match": "No Match" | "Full Term Match",
                    "name": list[str],
                    "oboId": list[str]
                }]
            }]

        Returns:
            List[Dict]: list of entities with merged entities format per recipe
        """

        def for_each_row(lexmapr_ent: List[Dict], row_ner: List[Dict]):
            # lexmapr_ent -> List[{"name": str, "oboId": list[str], "match": str}]
            # row_ner -> List[{"start": int, "end": int, "type": str, "entity": str]}

            useless_ner_entities = [
                ent['entity']
                for ent in row_ner
                if ent['type'] in ['COLOR', 'PHYSICAL_QUALITY', 'PROCESS']
            ]
            food_ner_entities = [
                ent['entity']
                for ent in row_ner
                if ent['type'] == 'FOOD'
            ]

            connected_lexmapr_entities = []
            pairs = pairwise(lexmapr_ent)
            for e1, e2 in pairs:
                if all([
                    e1['name'] in useless_ner_entities,
                    e2['name'] in food_ner_entities
                ]):
                    connected_lexmapr_entities.append({
                        **e2,
                        'name': f"{e1['name']} {e2['name']}"
                    })
                    next(pairs, None)  # disable exception
                else:
                    connected_lexmapr_entities.append(e1)

            return connected_lexmapr_entities

        body = [
            {
                **recipe,
                'ingredientSet': for_each_row(recipe['ingredientSet'], ner_entities)
            }
            for recipe, ner_entities in zip(body, request_input.ingredients_entities)
        ]

        return body

    @staticmethod
    def add_closest_sentences(body: List[dict], request_input: pd.DataFrame):
        """
            Find the closest sentence for an entities

            Returns:
                LexMaprOutput: json output with the closest sentences
        """

        # remove None values from ingredientSet and add numer of sentence
        sentences = [
            {
                sent_no: new_line_sen
                for sent_no, new_line_sen in enumerate(s.split('\n'))
            }
            for s in request_input['ingredients']
        ]

        def get_score_above(text: str, choices: Dict[int, str]) -> Optional[int]:
            min_value: float = 0.5
            # we have to remove extra info attached by LexMapr inside brackets
            text = re.sub(r'\(.+\)', '', text).strip()

            best_match, score = extractOne(text, choices.values(), scorer=fuzz.partial_token_sort_ratio)
            if score > min_value:
                for sent_no, val in choices.items():
                    if val == best_match:
                        return sent_no
            else:
                return None

        body = [{
            'title': recipe['title'],
            'link': recipe['link'],
            'sentences_with_ingredients': s,
            'ingredientSet': [{
                **entity,
                'sentence': get_score_above(entity['name'], s)
                if isinstance(entity['name'], str) else
                [get_score_above(n, s) for n in entity['name']]
            }
                for entity in recipe['ingredientSet']
                if entity
            ]
        }
            for s, recipe in zip(sentences, body)
        ]
        return body
