import ast

from nltk import sent_tokenize
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
        out = self.postprocess(self.request_input, self.lexmapr_output)
        return out

    @staticmethod
    def postprocess(request_input: pd.DataFrame, lexmapr_output: List[pd.DataFrame]):
        """
        Create requests output JSON

        Returns:
            LexMaprOutput: requests output
        """
        def for_each_row(row: Dict):
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
                "ingredientSet": [
                    for_each_row(entity)
                    for _, entity in recipe_ingredients.iterrows()
                    if len(entity)
                ],
            }
            for (_, recipe_info), recipe_ingredients in zip(
                request_input.iterrows(), lexmapr_output
            )
        ]

        # remove None values from ingredientSet and add numer of sentence
        sentences = [
            {
                sent_no: tokenized_sent
                for new_line_sen in s.split('\n')
                for sent_no, tokenized_sent in enumerate(sent_tokenize(new_line_sen))
            }
            for s in request_input['ingredients']
        ]

        def get_score_above(text: str, choices: Dict[int, str]) -> Optional[int]:
            min_value: float = 0.5
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
