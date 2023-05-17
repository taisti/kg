import io
import json
from more_itertools import pairwise
from typing import List, Dict
import pandas as pd


class Preprocessing:
    Columns = [
        "title",
        "ingredients",
        "directions",
        "link",
        "source",
        "NER",
        "ingredients_entities",
    ]

    def __init__(self, data_input: str):
        self.input = data_input

    def run(self):
        df = self.parse_input(self.input)
        entities = self.keep_important_entities(df["ingredients_entities"])
        entities = self.pair_merge_entities(entities)
        entities = self.entities_to_string(entities)
        return df, entities

    @staticmethod
    def parse_input(data_input: str) -> pd.DataFrame:
        """
        Convert input csv string with columns

        `title,ingredients,directions,link,source,NER,ingredients_entities`

        into a DataFrame

        Args:
            data_input (str): csv string

        Returns:
            pd.DataFrame: parsed csv
        """
        text = io.StringIO(data_input)
        df = pd.read_csv(
            text,
            sep=",",
            converters={k: json.loads for k in ('NER', 'ingredients_entities')}
        )
        return df

    @staticmethod
    def keep_important_entities(recipes: pd.Series) -> pd.Series:
        """
        Keep entities if not **QUANTITY** or **UNIT** entity type

        Args:
            recipes (pd.Series): list of entities with QUANTITY and UNITS entities per recipe

        Returns:
            pd.Series: list of entities without QUANTITY and UNIT entities per recipe
        """

        def for_each_row(row: List[Dict]):
            important_entities = list(filter(lambda ent: ent["type"] not in ["QUANTITY", "UNIT"], row))
            return important_entities

        results = recipes.apply(for_each_row)
        return results

    @staticmethod
    def pair_merge_entities(recipes: pd.Series) -> pd.Series:
        """
        Merge entities when first entity type is **COLOR, PHYSICAL_QUALITY, PROCESS** and second is **FOOD**

        Args:
            recipes (pd.Series): list of entities per recipe

        Returns:
            pd.Series: list of entities with merged entities format per recipe
        """

        def for_each_row(row: List[Dict]):
            connected_entities = [
                {
                    **e2,
                    'entity': f"{e1['entity']} {e2['entity']}"
                }
                if e1['type'] in ['COLOR', 'PHYSICAL_QUALITY', 'PROCESS'] and e2['type'] is 'FOOD'
                else
                e1
                for e1, e2 in pairwise(row)
            ]
            return connected_entities

        results = recipes.apply(for_each_row)
        return results

    @staticmethod
    def entities_to_string(recipes: pd.Series) -> pd.Series:
        """
        Get entities string representation

        Args:
            recipes (pd.Series): list of entities per recipe

        Returns:
            pd.Series: list of entities in string format per recipe
        """

        def for_each_row(row: List[Dict]):
            text_entities = [e['entity'] for e in row]
            return text_entities

        results = recipes.apply(for_each_row)
        return results
