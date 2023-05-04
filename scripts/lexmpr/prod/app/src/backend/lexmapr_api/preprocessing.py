import io
import json
from typing import List
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
        entities = self.merge_important_entities(df["ingredients_entities"])
        csv_text = self.convert_entities_to_lexmapr_input(entities)
        return df, csv_text

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
        df = pd.read_csv(text, sep=",")
        return df

    @staticmethod
    def merge_important_entities(recipes: pd.Series) -> pd.Series:
        """
        Connect entities into string if not QUANTITY or UNIT entity type

        Args:
            recipes (pd.Series): text with QUANTITY and UNITS entities

        Returns:
            pd.Series: text without QUANTITY and UNIT entities
        """

        def for_each_row(row: str):
            entities = json.loads(row)
            text = [
                ent["entity"]
                for ent in entities
                if ent["type"] not in ["QUANTITY", "UNIT"]
            ]
            return text

        merged_entities = recipes.apply(for_each_row)
        return merged_entities

    @staticmethod
    def convert_entities_to_lexmapr_input(recipes: pd.Series) -> pd.Series:
        """
        Converts entities to csv input format

        Args:
            recipes (pd.Series): entities without QUANTITY and UNIT

        Returns:
            pd.Series: csv string
        """

        def for_each_row(entities: List[str]):
            ids = list(range(len(entities)))
            df = pd.DataFrame({"Id": ids, "Text": entities})
            s = io.StringIO()
            df.to_csv(s, index=False)
            data_for_lexmapr = s.getvalue()
            return data_for_lexmapr

        csv_text = recipes.apply(for_each_row)
        return csv_text
