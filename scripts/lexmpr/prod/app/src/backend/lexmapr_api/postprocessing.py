import ast
import pprint

import pandas as pd
from typing import List, Dict


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

        # remove None values from ingredientSet
        body = [{
            'title': recipe['title'],
            'link': recipe['link'],
            'ingredientSet': [
                entity
                for entity in recipe['ingredientSet']
                if entity
            ]
        }
         for recipe in body
        ]

        return body
