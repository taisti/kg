import ast
import pandas as pd
from typing import Dict, Union, List
from dataclasses import dataclass


class Postprocessing:
    # @dataclass
    # class Linking:
    #     name: Union[str, List[str]]
    #     oboId: Union[str, List[str]]
    #     match: str

    # @dataclass
    # class Response:
    #     title: str
    #     link: str
    #     ingredients_set: List["Postprocessing.Linking"]

    def __init__(
        self, request_input: pd.DataFrame, lexmapr_output: List[pd.DataFrame]
    ):
        self.request_input = request_input
        self.lexmapr_output = lexmapr_output

    def run(self):
        out = self.postprocess(self.request_input, self.lexmapr_output)
        return out

    def postprocess(
        self, request_input: pd.DataFrame, lexmapr_output: List[pd.DataFrame]
    ):
        """
        Create requests output JSON

        Returns:
            LexMaprOutput: requests output
        """

        def for_each_row(row: pd.DataFrame):
            match = row["Match_Status(Macro Level)"]
            if match == "No Match":
                return None

            match_components = ast.literal_eval(row["Matched_Components"])
            name = [txt.split(":")[0] for txt in match_components]
            oboId = [txt.split(":")[1] for txt in match_components]

            if len(name) == 1:
                name = name[0]
                oboId = oboId[0]

            ingredients_set = {"name": name, "oboId": oboId, "match": match}
            return ingredients_set
        body = [
            {
                "title": input_body["title"],
                "link": input_body["link"],
                "ingredientSet": [
                    {"name" : entity[1]["Matched_Components"].split(":")[0].strip("[\[']"),
                     "oboId": entity[1]["Matched_Components"].split(":")[1].strip("[\[']"),
                     "match" : entity[1]["Match_Status(Macro Level)"] } 
                     for entity in lxmpr_out.iterrows() if entity[1]["Match_Status(Macro Level)"] != "No Match"
                ],
            }
            for (_, input_body), lxmpr_out in zip(
                request_input.iterrows(), lexmapr_output
            )
        ]

        return body
